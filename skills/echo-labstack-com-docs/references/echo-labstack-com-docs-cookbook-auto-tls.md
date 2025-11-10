Auto TLS

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
* Auto TLS
On this page
Auto TLS
========
This recipe demonstrates how to obtain TLS certificates for a domain automatically from
Let's Encrypt. `Echo#StartAutoTLS` accepts an address which should listen on port `443`.
Browse to `https://<DOMAIN>`. If everything goes fine, you should see a welcome
message with TLS enabled on the website.
tip
* For added security you should specify host policy in auto TLS manager
* Cache certificates to avoid issues with rate limits (<https://letsencrypt.org/docs/rate-limits>)
* To redirect HTTP traffic to HTTPS, you can use [redirect middleware](/docs/middleware/redirect#https-redirect)
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/auto-tls/server.go
```
package main  
  
import (  
	"crypto/tls"  
	"golang.org/x/crypto/acme"  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"golang.org/x/crypto/acme/autocert"  
)  
  
func main() {  
	e := echo.New()  
	// e.AutoTLSManager.HostPolicy = autocert.HostWhitelist("<DOMAIN>")  
	// Cache certificates to avoid issues with rate limits (https://letsencrypt.org/docs/rate-limits)  
	e.AutoTLSManager.Cache = autocert.DirCache("/var/www/.cache")  
	e.Use(middleware.Recover())  
	e.Use(middleware.Logger())  
	e.GET("/", func(c echo.Context) error {  
		return c.HTML(http.StatusOK, `  
			<h1>Welcome to Echo!</h1>  
			<h3>TLS certificates automatically installed from Let's Encrypt :)</h3>  
		`)  
	})  
  
	e.Logger.Fatal(e.StartAutoTLS(":443"))  
}  
  
func customHTTPServer() {  
	e := echo.New()  
	e.Use(middleware.Recover())  
	e.Use(middleware.Logger())  
	e.GET("/", func(c echo.Context) error {  
		return c.HTML(http.StatusOK, `  
			<h1>Welcome to Echo!</h1>  
			<h3>TLS certificates automatically installed from Let's Encrypt :)</h3>  
		`)  
	})  
  
	autoTLSManager := autocert.Manager{  
		Prompt: autocert.AcceptTOS,  
		// Cache certificates to avoid issues with rate limits (https://letsencrypt.org/docs/rate-limits)  
		Cache: autocert.DirCache("/var/www/.cache"),  
		//HostPolicy: autocert.HostWhitelist("<DOMAIN>"),  
	}  
	s := http.Server{  
		Addr:    ":443",  
		Handler: e, // set Echo as handler  
		TLSConfig: &tls.Config{  
			//Certificates: nil, // <-- s.ListenAndServeTLS will populate this field  
			GetCertificate: autoTLSManager.GetCertificate,  
			NextProtos:     []string{acme.ALPNProto},  
		},  
		//ReadTimeout: 30 * time.Second, // use custom timeouts  
	}  
	if err := s.ListenAndServeTLS("", ""); err != http.ErrServerClosed {  
		e.Logger.Fatal(err)  
	}  
}
```