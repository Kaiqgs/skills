HTTP/2 Server

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
* HTTP/2 Server
On this page
HTTP/2 Server
=============
1) Generate a self-signed X.509 TLS certificate[​](#1-generate-a-self-signed-x509-tls-certificate "Direct link to 1) Generate a self-signed X.509 TLS certificate")
-------------------------------------------------------------------------------------------------------------------------------------------------------------------
Run the following command to generate `cert.pem` and `key.pem` files:
```
go run $GOROOT/src/crypto/tls/generate_cert.go --host localhost
```
note
For demo purpose, we are using a self-signed certificate. Ideally, you should obtain
a certificate from [CA](https://en.wikipedia.org/wiki/Certificate_authority).
2) Create a handler which simply outputs the request information to the client[​](#2-create-a-handler-which-simply-outputs-the-request-information-to-the-client "Direct link to 2) Create a handler which simply outputs the request information to the client")
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
e.GET("/request", func(c echo.Context) error {  
  req := c.Request()  
  format := `  
    <code>  
      Protocol: %s<br>  
      Host: %s<br>  
      Remote Address: %s<br>  
      Method: %s<br>  
      Path: %s<br>  
    </code>  
  `  
  return c.HTML(http.StatusOK, fmt.Sprintf(format, req.Proto, req.Host, req.RemoteAddr, req.Method, req.URL.Path))  
})
```
3) Start TLS server using cert.pem and key.pem[​](#3-start-tls-server-using-certpem-and-keypem "Direct link to 3) Start TLS server using cert.pem and key.pem")
---------------------------------------------------------------------------------------------------------------------------------------------------------------
```
if err := e.StartTLS(":1323", "cert.pem", "key.pem"); err != http.ErrServerClosed {  
  log.Fatal(err)  
}
```
or use customized HTTP server with your own TLSConfig
```
s := http.Server{  
  Addr:    ":8443",  
  Handler: e, // set Echo as handler  
  TLSConfig: &tls.Config{  
    //Certificates: nil, // <-- s.ListenAndServeTLS will populate this field  
  },  
  //ReadTimeout: 30 * time.Second, // use custom timeouts  
}  
if err := s.ListenAndServeTLS("cert.pem", "key.pem"); err != http.ErrServerClosed {  
  log.Fatal(err)  
}
```
4) Start the server and browse to <https://localhost:1323/request> to see the following output[​](#4-start-the-server-and-browse-to-httpslocalhost1323request-to-see-the-following-output "Direct link to 4-start-the-server-and-browse-to-httpslocalhost1323request-to-see-the-following-output")
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```
Protocol: HTTP/2.0  
Host: localhost:1323  
Remote Address: [::1]:60288  
Method: GET  
Path: /
```
Source Code[​](#source-code "Direct link to Source Code")
---------------------------------------------------------
cookbook/http2/server.go
```
package main  
  
import (  
	"fmt"  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
)  
  
func main() {  
	e := echo.New()  
	e.GET("/request", func(c echo.Context) error {  
		req := c.Request()  
		format := `  
			<code>  
				Protocol: %s<br>  
				Host: %s<br>  
				Remote Address: %s<br>  
				Method: %s<br>  
				Path: %s<br>  
			</code>  
		`  
		return c.HTML(http.StatusOK, fmt.Sprintf(format, req.Proto, req.Host, req.RemoteAddr, req.Method, req.URL.Path))  
	})  
	e.Logger.Fatal(e.StartTLS(":1323", "cert.pem", "key.pem"))  
}
```