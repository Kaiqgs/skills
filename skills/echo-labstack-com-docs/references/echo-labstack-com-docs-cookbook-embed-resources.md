Embed Resources

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
* Embed Resources
On this page
Embed Resources
===============
With go 1.16 embed feature[​](#with-go-116-embed-feature "Direct link to With go 1.16 embed feature")
-----------------------------------------------------------------------------------------------------
cookbook/embed/server.go
```
package main  
  
import (  
	"embed"  
	"io/fs"  
	"log"  
	"net/http"  
	"os"  
  
	"github.com/labstack/echo/v4"  
)  
  
//go:embed app  
var embededFiles embed.FS  
  
func getFileSystem(useOS bool) http.FileSystem {  
	if useOS {  
		log.Print("using live mode")  
		return http.FS(os.DirFS("app"))  
	}  
  
	log.Print("using embed mode")  
	fsys, err := fs.Sub(embededFiles, "app")  
	if err != nil {  
		panic(err)  
	}  
  
	return http.FS(fsys)  
}  
  
func main() {  
	e := echo.New()  
	useOS := len(os.Args) > 1 && os.Args[1] == "live"  
	assetHandler := http.FileServer(getFileSystem(useOS))  
	e.GET("/", echo.WrapHandler(assetHandler))  
	e.GET("/static/*", echo.WrapHandler(http.StripPrefix("/static/", assetHandler)))  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
With go.rice[​](#with-gorice "Direct link to With go.rice")
-----------------------------------------------------------
cookbook/embed-resources/server.go
```
package main  
  
import (  
	"net/http"  
  
	"github.com/GeertJohan/go.rice"  
	"github.com/labstack/echo/v4"  
)  
  
func main() {  
	e := echo.New()  
	// the file server for rice. "app" is the folder where the files come from.  
	assetHandler := http.FileServer(rice.MustFindBox("app").HTTPBox())  
	// serves the index.html from rice  
	e.GET("/", echo.WrapHandler(assetHandler))  
  
	// servers other static files  
	e.GET("/static/*", echo.WrapHandler(http.StripPrefix("/static/", assetHandler)))  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```