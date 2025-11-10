Subdomain

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
* Subdomain
On this page
Subdomain
=========
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/subdomain/server.go
```
package main  
  
import (  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
type (  
	Host struct {  
		Echo *echo.Echo  
	}  
)  
  
func main() {  
	// Hosts  
	hosts := map[string]*Host{}  
  
	//-----  
	// API  
	//-----  
  
	api := echo.New()  
	api.Use(middleware.Logger())  
	api.Use(middleware.Recover())  
  
	hosts["api.localhost:1323"] = &Host{api}  
  
	api.GET("/", func(c echo.Context) error {  
		return c.String(http.StatusOK, "API")  
	})  
  
	//------  
	// Blog  
	//------  
  
	blog := echo.New()  
	blog.Use(middleware.Logger())  
	blog.Use(middleware.Recover())  
  
	hosts["blog.localhost:1323"] = &Host{blog}  
  
	blog.GET("/", func(c echo.Context) error {  
		return c.String(http.StatusOK, "Blog")  
	})  
  
	//---------  
	// Website  
	//---------  
  
	site := echo.New()  
	site.Use(middleware.Logger())  
	site.Use(middleware.Recover())  
  
	hosts["localhost:1323"] = &Host{site}  
  
	site.GET("/", func(c echo.Context) error {  
		return c.String(http.StatusOK, "Website")  
	})  
  
	// Server  
	e := echo.New()  
	e.Any("/*", func(c echo.Context) (err error) {  
		req := c.Request()  
		res := c.Response()  
		host := hosts[req.Host]  
  
		if host == nil {  
			err = echo.ErrNotFound  
		} else {  
			host.Echo.ServeHTTP(res, req)  
		}  
  
		return  
	})  
	e.Logger.Fatal(e.Start(":1323"))  
}
```