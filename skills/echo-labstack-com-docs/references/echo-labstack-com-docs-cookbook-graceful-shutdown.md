Graceful Shutdown

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
* Graceful Shutdown
On this page
Graceful Shutdown
=================
Using [http.Server#Shutdown()](https://golang.org/pkg/net/http/#Server.Shutdown)[​](#using-httpservershutdown "Direct link to using-httpservershutdown")
--------------------------------------------------------------------------------------------------------------------------------------------------------
cookbook/graceful-shutdown/server.go
```
package main  
  
import (  
	"context"  
	"net/http"  
	"os"  
	"os/signal"  
	"time"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/gommon/log"  
)  
  
func main() {  
	// Setup  
	e := echo.New()  
	e.Logger.SetLevel(log.INFO)  
	e.GET("/", func(c echo.Context) error {  
		time.Sleep(5 * time.Second)  
		return c.JSON(http.StatusOK, "OK")  
	})  
  
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)  
	defer stop()  
	// Start server  
	go func() {  
		if err := e.Start(":1323"); err != nil && err != http.ErrServerClosed {  
			e.Logger.Fatal("shutting down the server")  
		}  
	}()  
  
	// Wait for interrupt signal to gracefully shut down the server with a timeout of 10 seconds.  
	<-ctx.Done()  
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)  
	defer cancel()  
	if err := e.Shutdown(ctx); err != nil {  
		e.Logger.Fatal(err)  
	}  
}
```
note
Requires go1.16+