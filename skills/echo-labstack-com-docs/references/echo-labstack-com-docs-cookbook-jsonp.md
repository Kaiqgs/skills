JSONP

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
* JSONP
On this page
JSONP
=====
JSONP is a method that allows cross-domain server calls. You can read more about it at the JSON versus JSONP Tutorial.
Server[​](#server "Direct link to Server")
------------------------------------------
cookbook/jsonp/server.go
```
package main  
  
import (  
	"math/rand"  
	"net/http"  
	"time"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
func main() {  
	e := echo.New()  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	e.Static("/", "public")  
  
	// JSONP  
	e.GET("/jsonp", func(c echo.Context) error {  
		callback := c.QueryParam("callback")  
		var content struct {  
			Response  string    `json:"response"`  
			Timestamp time.Time `json:"timestamp"`  
			Random    int       `json:"random"`  
		}  
		content.Response = "Sent via JSONP"  
		content.Timestamp = time.Now().UTC()  
		content.Random = rand.Intn(1000)  
		return c.JSONP(http.StatusOK, callback, &content)  
	})  
  
	// Start server  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Client[​](#client "Direct link to Client")
------------------------------------------
cookbook/jsonp/public/index.html
```
<!DOCTYPE html>  
<html>  
  
<head>  
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />  
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">  
    <title>JSONP</title>  
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>  
    <script type="text/javascript">  
        var host_prefix = 'http://localhost:1323';  
        $(document).ready(function() {  
            // JSONP version - add 'callback=?' to the URL - fetch the JSONP response to the request  
            $("#jsonp-button").click(function(e) {  
                e.preventDefault();  
                // The only difference on the client end is the addition of 'callback=?' to the URL  
                var url = host_prefix + '/jsonp?callback=?';  
                $.getJSON(url, function(jsonp) {  
                    console.log(jsonp);  
                    $("#jsonp-response").html(JSON.stringify(jsonp, null, 2));  
                });  
            });  
        });  
    </script>  
  
</head>  
  
<body>  
    <div class="container" style="margin-top: 50px;">  
        <input type="button" class="btn btn-primary btn-lg" id="jsonp-button" value="Get JSONP response">  
        <p>  
            <pre id="jsonp-response"></pre>  
        </p>  
    </div>  
</body>  
  
</html>
```