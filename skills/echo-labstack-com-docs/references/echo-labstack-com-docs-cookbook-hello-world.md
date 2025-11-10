Hello World

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
* Hello World
On this page
Hello World
===========
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/hello-world/server.go
```
package main  
  
import (  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func main() {  
	// Echo instance  
	e := echo.New()  
  
	// Middleware  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// Route => handler  
	e.GET("/", func(c echo.Context) error {  
		return c.String(http.StatusOK, "Hello, World!\n")  
	})  
  
	// Start server  
	e.Logger.Fatal(e.Start(":1323"))  
}
```