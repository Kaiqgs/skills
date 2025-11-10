Load Balancing

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
* Load Balancing
On this page
Load Balancing
==============
This recipe demonstrates how you can use Nginx as a reverse proxy server and load balance between multiple Echo servers.
Echo[​](#echo "Direct link to Echo")
------------------------------------
cookbook/load-balancing/upstream/server.go
```
package main  
  
import (  
	"fmt"  
	"net/http"  
	"os"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
var index = `  
	<!DOCTYPE html>  
	<html lang="en">  
	<head>  
		<meta charset="UTF-8">  
		<meta name="viewport" content="width=device-width, initial-scale=1.0">  
		<meta http-equiv="X-UA-Compatible" content="ie=edge">  
		<title>Upstream Server</title>  
		<style>  
			h1, p {  
				font-weight: 300;  
			}  
		</style>  
	</head>  
	<body>  
		<p>  
			Hello from upstream server %s  
		</p>  
	</body>  
	</html>  
`  
  
func main() {  
	name := os.Args[1]  
	port := os.Args[2]  
	e := echo.New()  
	e.Use(middleware.Recover())  
	e.Use(middleware.Logger())  
	e.GET("/", func(c echo.Context) error {  
		return c.HTML(http.StatusOK, fmt.Sprintf(index, name))  
	})  
	e.Logger.Fatal(e.Start(port))  
}
```
### Start servers[​](#start-servers "Direct link to Start servers")
* `cd upstream`
* `go run server.go server1 :8081`
* `go run server.go server2 :8082`
Nginx[​](#nginx "Direct link to Nginx")
---------------------------------------
### 1) Install Nginx[​](#1-install-nginx "Direct link to 1) Install Nginx")
<https://www.nginx.com/resources/wiki/start/topics/tutorials/install>
### 2) Configure Nginx[​](#2-configure-nginx "Direct link to 2) Configure Nginx")
Create a file `/etc/nginx/sites-enabled/localhost` with the following content:
```
https://github.com/labstack/echox/blob/master/cookbook/load-balancing/nginx.conf
```
info
Change listen, server\_name, access\_log per your need.
### 3) Restart Nginx[​](#3-restart-nginx "Direct link to 3) Restart Nginx")
```
service nginx restart
```
Browse to <https://localhost:8080>, and you should see a webpage being served from either "server 1" or "server 2".
```
Hello from upstream server server1
```