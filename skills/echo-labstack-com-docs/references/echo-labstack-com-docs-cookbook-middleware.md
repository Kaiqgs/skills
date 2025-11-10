Middleware

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
* Middleware
On this page
Middleware
==========
Write a custom middleware[​](#write-a-custom-middleware "Direct link to Write a custom middleware")
---------------------------------------------------------------------------------------------------
* Middleware to collect request count, statuses and uptime.
* Middleware to write custom `Server` header to the response.
### Server[​](#server "Direct link to Server")
cookbook/middleware/server.go
```
package main  
  
import (  
	"net/http"  
	"strconv"  
	"sync"  
	"time"  
  
	"github.com/labstack/echo/v4"  
)  
  
type (  
	Stats struct {  
		Uptime       time.Time      `json:"uptime"`  
		RequestCount uint64         `json:"requestCount"`  
		Statuses     map[string]int `json:"statuses"`  
		mutex        sync.RWMutex  
	}  
)  
  
func NewStats() *Stats {  
	return &Stats{  
		Uptime:   time.Now(),  
		Statuses: map[string]int{},  
	}  
}  
  
// Process is the middleware function.  
func (s *Stats) Process(next echo.HandlerFunc) echo.HandlerFunc {  
	return func(c echo.Context) error {  
		if err := next(c); err != nil {  
			c.Error(err)  
		}  
		s.mutex.Lock()  
		defer s.mutex.Unlock()  
		s.RequestCount++  
		status := strconv.Itoa(c.Response().Status)  
		s.Statuses[status]++  
		return nil  
	}  
}  
  
// Handle is the endpoint to get stats.  
func (s *Stats) Handle(c echo.Context) error {  
	s.mutex.RLock()  
	defer s.mutex.RUnlock()  
	return c.JSON(http.StatusOK, s)  
}  
  
// ServerHeader middleware adds a `Server` header to the response.  
func ServerHeader(next echo.HandlerFunc) echo.HandlerFunc {  
	return func(c echo.Context) error {  
		c.Response().Header().Set(echo.HeaderServer, "Echo/3.0")  
		return next(c)  
	}  
}  
  
func main() {  
	e := echo.New()  
  
	// Debug mode  
	e.Debug = true  
  
	//-------------------  
	// Custom middleware  
	//-------------------  
	// Stats  
	s := NewStats()  
	e.Use(s.Process)  
	e.GET("/stats", s.Handle) // Endpoint to get stats  
  
	// Server header  
	e.Use(ServerHeader)  
  
	// Handler  
	e.GET("/", func(c echo.Context) error {  
		return c.String(http.StatusOK, "Hello, World!")  
	})  
  
	// Start server  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Response[​](#response "Direct link to Response")
#### Headers[​](#headers "Direct link to Headers")
```
Content-Length:122  
Content-Type:application/json; charset=utf-8  
Date:Thu, 14 Apr 2016 20:31:46 GMT  
Server:Echo/3.0
```
#### Body[​](#body "Direct link to Body")
```
{  
  "uptime": "2016-04-14T13:28:48.486548936-07:00",  
  "requestCount": 5,  
  "statuses": {  
    "200": 4,  
    "404": 1  
  }  
}
```