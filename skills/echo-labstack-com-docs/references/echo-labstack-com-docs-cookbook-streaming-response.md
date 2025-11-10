Streaming Response

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
* Streaming Response
On this page
Streaming Response
==================
* Send data as it is produced
* Streaming JSON response with chunked transfer encoding
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/streaming-response/server.go
```
package main  
  
import (  
	"encoding/json"  
	"net/http"  
	"time"  
  
	"github.com/labstack/echo/v4"  
)  
  
type (  
	Geolocation struct {  
		Altitude  float64  
		Latitude  float64  
		Longitude float64  
	}  
)  
  
var (  
	locations = []Geolocation{  
		{-97, 37.819929, -122.478255},  
		{1899, 39.096849, -120.032351},  
		{2619, 37.865101, -119.538329},  
		{42, 33.812092, -117.918974},  
		{15, 37.77493, -122.419416},  
	}  
)  
  
func main() {  
	e := echo.New()  
	e.GET("/", func(c echo.Context) error {  
		c.Response().Header().Set(echo.HeaderContentType, echo.MIMEApplicationJSON)  
		c.Response().WriteHeader(http.StatusOK)  
  
		enc := json.NewEncoder(c.Response())  
		for _, l := range locations {  
			if err := enc.Encode(l); err != nil {  
				return err  
			}  
			c.Response().Flush()  
			time.Sleep(1 * time.Second)  
		}  
		return nil  
	})  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Client[​](#client "Direct link to Client")
------------------------------------------
```
$ curl localhost:1323
```
### Output[​](#output "Direct link to Output")
```
{"Altitude":-97,"Latitude":37.819929,"Longitude":-122.478255}  
{"Altitude":1899,"Latitude":39.096849,"Longitude":-120.032351}  
{"Altitude":2619,"Latitude":37.865101,"Longitude":-119.538329}  
{"Altitude":42,"Latitude":33.812092,"Longitude":-117.918974}  
{"Altitude":15,"Latitude":37.77493,"Longitude":-122.419416}
```