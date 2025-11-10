CRUD

* [Introduction](/docs)
* [Guide](/docs/category/guide)
* [Middleware](/docs/category/middleware)
* [Cookbook](/docs/category/cookbook)
  + [Auto TLS](/docs/cookbook/auto-tls)
  + [CORS](/docs/cookbook/cors)
  + [CRUD](/docs/cookbook/crud)
  + [Embed Resources](/docs/cookbook/embed-resources)
  + [File Download](/docs/cookbook/file-download)
  + [File Upload](/docs/cookbook/file-upload)
  + [Google App Engine](/docs/cookbook/google-app-engine)
  + [Graceful Shutdown](/docs/cookbook/graceful-shutdown)
  + [Hello World](/docs/cookbook/hello-world)
  + [HTTP/2 Server Push](/docs/cookbook/http2-server-push)
  + [HTTP/2 Server](/docs/cookbook/http2)
  + [JSONP](/docs/cookbook/jsonp)
  + [JWT](/docs/cookbook/jwt)
  + [Load Balancing](/docs/cookbook/load-balancing)
  + [Middleware](/docs/cookbook/middleware)
  + [Reverse Proxy](/docs/cookbook/reverse-proxy)
  + [Server-Sent-Events (SSE)](/docs/cookbook/sse)
  + [Streaming Response](/docs/cookbook/streaming-response)
  + [Subdomain](/docs/cookbook/subdomain)
  + [Timeout](/docs/cookbook/timeout)
  + [Twitter Like API](/docs/cookbook/twitter)
  + [WebSocket](/docs/cookbook/websocket)
* [Cookbook](/docs/category/cookbook)
* CRUD
On this page
CRUD
====
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/crud/server.go
```
package main  
  
import (  
	"net/http"  
	"strconv"  
	"sync"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
type (  
	user struct {  
		ID   int    `json:"id"`  
		Name string `json:"name"`  
	}  
)  
  
var (  
	users = map[int]*user{}  
	seq   = 1  
	lock  = sync.Mutex{}  
)  
  
//----------  
// Handlers  
//----------  
  
func createUser(c echo.Context) error {  
	lock.Lock()  
	defer lock.Unlock()  
	u := &user{  
		ID: seq,  
	}  
	if err := c.Bind(u); err != nil {  
		return err  
	}  
	users[u.ID] = u  
	seq++  
	return c.JSON(http.StatusCreated, u)  
}  
  
func getUser(c echo.Context) error {  
	lock.Lock()  
	defer lock.Unlock()  
	id, _ := strconv.Atoi(c.Param("id"))  
	return c.JSON(http.StatusOK, users[id])  
}  
  
func updateUser(c echo.Context) error {  
	lock.Lock()  
	defer lock.Unlock()  
	u := new(user)  
	if err := c.Bind(u); err != nil {  
		return err  
	}  
	id, _ := strconv.Atoi(c.Param("id"))  
	users[id].Name = u.Name  
	return c.JSON(http.StatusOK, users[id])  
}  
  
func deleteUser(c echo.Context) error {  
	lock.Lock()  
	defer lock.Unlock()  
	id, _ := strconv.Atoi(c.Param("id"))  
	delete(users, id)  
	return c.NoContent(http.StatusNoContent)  
}  
  
func getAllUsers(c echo.Context) error {  
	lock.Lock()  
	defer lock.Unlock()  
	return c.JSON(http.StatusOK, users)  
}  
  
func main() {  
	e := echo.New()  
  
	// Middleware  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// Routes  
	e.GET("/users", getAllUsers)  
	e.POST("/users", createUser)  
	e.GET("/users/:id", getUser)  
	e.PUT("/users/:id", updateUser)  
	e.DELETE("/users/:id", deleteUser)  
  
	// Start server  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Client[​](#client "Direct link to Client")
------------------------------------------
### Create user[​](#create-user "Direct link to Create user")
#### Request[​](#request "Direct link to Request")
```
curl -X POST \  
  -H 'Content-Type: application/json' \  
  -d '{"name":"Joe Smith"}' \  
  localhost:1323/users
```
#### Response[​](#response "Direct link to Response")
```
{  
  "id": 1,  
  "name": "Joe Smith"  
}
```
### Get user[​](#get-user "Direct link to Get user")
#### Request[​](#request-1 "Direct link to Request")
```
curl localhost:1323/users/1
```
#### Response[​](#response-1 "Direct link to Response")
```
{  
  "id": 1,  
  "name": "Joe Smith"  
}
```
### Update user[​](#update-user "Direct link to Update user")
#### Request[​](#request-2 "Direct link to Request")
```
curl -X PUT \  
  -H 'Content-Type: application/json' \  
  -d '{"name":"Joe"}' \  
  localhost:1323/users/1
```
#### Response[​](#response-2 "Direct link to Response")
```
{  
  "id": 1,  
  "name": "Joe"  
}
```
### Delete user[​](#delete-user "Direct link to Delete user")
#### Request[​](#request-3 "Direct link to Request")
```
curl -X DELETE localhost:1323/users/1
```
#### Response[​](#response-3 "Direct link to Response")
`NoContent - 204`