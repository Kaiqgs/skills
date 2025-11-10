HTTP/2 Server Push

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
* HTTP/2 Server Push
On this page
HTTP/2 Server Push
==================
note
Requires go1.8+
Send web assets using HTTP/2 server push[​](#send-web-assets-using-http2-server-push "Direct link to Send web assets using HTTP/2 server push")
-----------------------------------------------------------------------------------------------------------------------------------------------
### [Generate a self-signed X.509 TLS certificate](/docs/cookbook/http2#step-1-generate-a-self-signed-x-509-tls-certificate)[​](#generate-a-self-signed-x509-tls-certificate "Direct link to generate-a-self-signed-x509-tls-certificate")
### 1) Register a route to serve web assets[​](#1-register-a-route-to-serve-web-assets "Direct link to 1) Register a route to serve web assets")
```
e.Static("/", "static")
```
### 2) Create a handler to serve index.html and push it's dependencies[​](#2-create-a-handler-to-serve-indexhtml-and-push-its-dependencies "Direct link to 2) Create a handler to serve index.html and push it's dependencies")
```
e.GET("/", func(c echo.Context) (err error) {  
  pusher, ok := c.Response().Writer.(http.Pusher)  
  if ok {  
    if err = pusher.Push("/app.css", nil); err != nil {  
      return  
    }  
    if err = pusher.Push("/app.js", nil); err != nil {  
      return  
    }  
    if err = pusher.Push("/echo.png", nil); err != nil {  
      return  
    }  
  }  
  return c.File("index.html")  
})
```
info
If `http.Pusher` is supported, web assets are pushed; otherwise, client makes separate requests to get them.
### 3) Start TLS server using cert.pem and key.pem[​](#3-start-tls-server-using-certpem-and-keypem "Direct link to 3) Start TLS server using cert.pem and key.pem")
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
### 4) Start the server and browse to <https://localhost:1323>[​](#4-start-the-server-and-browse-to-httpslocalhost1323 "Direct link to 4-start-the-server-and-browse-to-httpslocalhost1323")
```
Protocol: HTTP/2.0  
Host: localhost:1323  
Remote Address: [::1]:60288  
Method: GET  
Path: /
```
Source Code[​](#source-code "Direct link to Source Code")
---------------------------------------------------------
cookbook/http2-server-push/index.html
```
<!DOCTYPE html>  
<html lang="en">  
<head>  
  <meta charset="UTF-8">  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  
  <meta http-equiv="X-UA-Compatible" content="ie=edge">  
  <title>HTTP/2 Server Push</title>  
  <link rel="stylesheet" href="/app.css">  
  <script src="/app.js"></script>  
</head>  
<body>  
  <img class="echo" src="/echo.png">  
  <h2>The following static files are served via HTTP/2 server push</h2>  
  <ul>  
    <li><code>/app.css</code></li>  
    <li><code>/app.js</code></li>  
    <li><code>/echo.png</code></li>  
  </ul>  
</body>  
</html>
```
cookbook/http2-server-push/server.go
```
package main  
  
import (  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
)  
  
func main() {  
	e := echo.New()  
	e.Static("/", "static")  
	e.GET("/", func(c echo.Context) (err error) {  
		pusher, ok := c.Response().Writer.(http.Pusher)  
		if ok {  
			if err = pusher.Push("/app.css", nil); err != nil {  
				return  
			}  
			if err = pusher.Push("/app.js", nil); err != nil {  
				return  
			}  
			if err = pusher.Push("/echo.png", nil); err != nil {  
				return  
			}  
		}  
		return c.File("index.html")  
	})  
	e.Logger.Fatal(e.StartTLS(":1323", "cert.pem", "key.pem"))  
}
```