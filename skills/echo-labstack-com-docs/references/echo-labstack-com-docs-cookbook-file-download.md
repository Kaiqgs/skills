File Download

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
* File Download
On this page
File Download
=============
Download file[​](#download-file "Direct link to Download file")
---------------------------------------------------------------
### Server[​](#server "Direct link to Server")
cookbook/file-download/server.go
```
package main  
  
import (  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.GET("/", func(c echo.Context) error {  
		return c.File("index.html")  
	})  
	e.GET("/file", func(c echo.Context) error {  
		return c.File("echo.svg")  
	})  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Client[​](#client "Direct link to Client")
cookbook/file-download/index.html
```
<!doctype html>  
<html lang="en">  
<head>  
    <meta charset="utf-8">  
    <title>File download</title>  
</head>  
<body>  
  
    <p>  
        <a href="/file">File download</a>  
    </p>  
  
</body>  
</html>
```
Download file as inline[​](#download-file-as-inline "Direct link to Download file as inline")
---------------------------------------------------------------------------------------------
### Server[​](#server-1 "Direct link to Server")
cookbook/file-download/inline/server.go
```
package main  
  
import (  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.GET("/", func(c echo.Context) error {  
		return c.File("index.html")  
	})  
	e.GET("/inline", func(c echo.Context) error {  
		return c.Inline("inline.txt", "inline.txt")  
	})  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Client[​](#client-1 "Direct link to Client")
cookbook/file-download/inline/index.html
```
<!doctype html>  
<html lang="en">  
<head>  
    <meta charset="utf-8">  
    <title>File download</title>  
</head>  
<body>  
  
    <p>  
        <a href="/inline">Inline file download</a>  
    </p>  
  
</body>  
</html>
```
Download file as attachment[​](#download-file-as-attachment "Direct link to Download file as attachment")
---------------------------------------------------------------------------------------------------------
### Server[​](#server-2 "Direct link to Server")
cookbook/file-download/attachment/server.go
```
package main  
  
import (  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.GET("/", func(c echo.Context) error {  
		return c.File("index.html")  
	})  
	e.GET("/attachment", func(c echo.Context) error {  
		return c.Attachment("attachment.txt", "attachment.txt")  
	})  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Client[​](#client-2 "Direct link to Client")
cookbook/file-download/attachment/index.html
```
<!doctype html>  
<html lang="en">  
<head>  
    <meta charset="utf-8">  
    <title>File download</title>  
</head>  
<body>  
  
    <p>  
        <a href="/attachment">Attachment file download</a>  
    </p>  
  
</body>  
</html>
```