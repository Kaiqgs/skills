File Upload

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
* File Upload
On this page
File Upload
===========
Upload single file with parameters[​](#upload-single-file-with-parameters "Direct link to Upload single file with parameters")
------------------------------------------------------------------------------------------------------------------------------
### Server[​](#server "Direct link to Server")
cookbook/file-upload/single/server.go
```
package main  
  
import (  
	"fmt"  
	"io"  
	"net/http"  
	"os"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func upload(c echo.Context) error {  
	// Read form fields  
	name := c.FormValue("name")  
	email := c.FormValue("email")  
  
	//-----------  
	// Read file  
	//-----------  
  
	// Source  
	file, err := c.FormFile("file")  
	if err != nil {  
		return err  
	}  
	src, err := file.Open()  
	if err != nil {  
		return err  
	}  
	defer src.Close()  
  
	// Destination  
	dst, err := os.Create(file.Filename)  
	if err != nil {  
		return err  
	}  
	defer dst.Close()  
  
	// Copy  
	if _, err = io.Copy(dst, src); err != nil {  
		return err  
	}  
  
	return c.HTML(http.StatusOK, fmt.Sprintf("<p>File %s uploaded successfully with fields name=%s and email=%s.</p>", file.Filename, name, email))  
}  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.Static("/", "public")  
	e.POST("/upload", upload)  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Client[​](#client "Direct link to Client")
cookbook/file-upload/single/public/index.html
```
<!doctype html>  
<html lang="en">  
<head>  
    <meta charset="utf-8">  
    <title>Single file upload</title>  
</head>  
<body>  
<h1>Upload single file with fields</h1>  
  
<form action="/upload" method="post" enctype="multipart/form-data">  
    Name: <input type="text" name="name"><br>  
    Email: <input type="email" name="email"><br>  
    Files: <input type="file" name="file"><br><br>  
    <input type="submit" value="Submit">  
</form>  
</body>  
</html>
```
Upload multiple files with parameters[​](#upload-multiple-files-with-parameters "Direct link to Upload multiple files with parameters")
---------------------------------------------------------------------------------------------------------------------------------------
### Server[​](#server-1 "Direct link to Server")
cookbook/file-upload/multiple/server.go
```
package main  
  
import (  
	"fmt"  
	"io"  
	"net/http"  
	"os"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func upload(c echo.Context) error {  
	// Read form fields  
	name := c.FormValue("name")  
	email := c.FormValue("email")  
  
	//------------  
	// Read files  
	//------------  
  
	// Multipart form  
	form, err := c.MultipartForm()  
	if err != nil {  
		return err  
	}  
	files := form.File["files"]  
  
	for _, file := range files {  
		// Source  
		src, err := file.Open()  
		if err != nil {  
			return err  
		}  
		defer src.Close()  
  
		// Destination  
		dst, err := os.Create(file.Filename)  
		if err != nil {  
			return err  
		}  
		defer dst.Close()  
  
		// Copy  
		if _, err = io.Copy(dst, src); err != nil {  
			return err  
		}  
  
	}  
  
	return c.HTML(http.StatusOK, fmt.Sprintf("<p>Uploaded successfully %d files with fields name=%s and email=%s.</p>", len(files), name, email))  
}  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.Static("/", "public")  
	e.POST("/upload", upload)  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Client[​](#client-1 "Direct link to Client")
cookbook/file-upload/multiple/public/index.html
```
<!doctype html>  
<html lang="en">  
<head>  
    <meta charset="utf-8">  
    <title>Multiple file upload</title>  
</head>  
<body>  
<h1>Upload multiple files with fields</h1>  
  
<form action="/upload" method="post" enctype="multipart/form-data">  
    Name: <input type="text" name="name"><br>  
    Email: <input type="email" name="email"><br>  
    Files: <input type="file" name="files" multiple><br><br>  
    <input type="submit" value="Submit">  
</form>  
</body>  
</html>
```