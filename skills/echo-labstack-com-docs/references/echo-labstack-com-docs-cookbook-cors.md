CORS

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
* CORS
On this page
CORS
====
Server using a list of allowed origins[​](#server-using-a-list-of-allowed-origins "Direct link to Server using a list of allowed origins")
------------------------------------------------------------------------------------------------------------------------------------------
cookbook/cors/origin-list/server.go
```
package main  
  
import (  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
var (  
	users = []string{"Joe", "Veer", "Zion"}  
)  
  
func getUsers(c echo.Context) error {  
	return c.JSON(http.StatusOK, users)  
}  
  
func main() {  
	e := echo.New()  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// CORS default  
	// Allows requests from any origin wth GET, HEAD, PUT, POST or DELETE method.  
	// e.Use(middleware.CORS())  
  
	// CORS restricted  
	// Allows requests from any `https://labstack.com` or `https://labstack.net` origin  
	// wth GET, PUT, POST or DELETE method.  
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{  
		AllowOrigins: []string{"https://labstack.com", "https://labstack.net"},  
		AllowMethods: []string{http.MethodGet, http.MethodPut, http.MethodPost, http.MethodDelete},  
	}))  
  
	e.GET("/api/users", getUsers)  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Server using a custom function to allow origins[​](#server-using-a-custom-function-to-allow-origins "Direct link to Server using a custom function to allow origins")
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
cookbook/cors/origin-func/server.go
```
package main  
  
import (  
	"net/http"  
	"regexp"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
var (  
	users = []string{"Joe", "Veer", "Zion"}  
)  
  
func getUsers(c echo.Context) error {  
	return c.JSON(http.StatusOK, users)  
}  
  
// allowOrigin takes the origin as an argument and returns true if the origin  
// is allowed or false otherwise.  
func allowOrigin(origin string) (bool, error) {  
	// In this example we use a regular expression but we can imagine various  
	// kind of custom logic. For example, an external datasource could be used  
	// to maintain the list of allowed origins.  
	return regexp.MatchString(`^https:\/\/labstack\.(net|com)$`, origin)  
}  
  
func main() {  
	e := echo.New()  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// CORS restricted with a custom function to allow origins  
	// and with the GET, PUT, POST or DELETE methods allowed.  
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{  
		AllowOriginFunc: allowOrigin,  
		AllowMethods:    []string{http.MethodGet, http.MethodPut, http.MethodPost, http.MethodDelete},  
	}))  
  
	e.GET("/api/users", getUsers)  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```