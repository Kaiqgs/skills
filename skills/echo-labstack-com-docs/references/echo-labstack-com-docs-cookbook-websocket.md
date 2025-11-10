WebSocket

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
* WebSocket
On this page
WebSocket
=========
Using net WebSocket[​](#using-net-websocket "Direct link to Using net WebSocket")
---------------------------------------------------------------------------------
### Server[​](#server "Direct link to Server")
cookbook/websocket/net/server.go
```
package main  
  
import (  
	"fmt"  
  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"golang.org/x/net/websocket"  
)  
  
func hello(c echo.Context) error {  
	websocket.Handler(func(ws *websocket.Conn) {  
		defer ws.Close()  
		for {  
			// Write  
			err := websocket.Message.Send(ws, "Hello, Client!")  
			if err != nil {  
				c.Logger().Error(err)  
			}  
  
			// Read  
			msg := ""  
			err = websocket.Message.Receive(ws, &msg)  
			if err != nil {  
				c.Logger().Error(err)  
			}  
			fmt.Printf("%s\n", msg)  
		}  
	}).ServeHTTP(c.Response(), c.Request())  
	return nil  
}  
  
func main() {  
	e := echo.New()  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
	e.Static("/", "../public")  
	e.GET("/ws", hello)  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Using gorilla WebSocket[​](#using-gorilla-websocket "Direct link to Using gorilla WebSocket")
---------------------------------------------------------------------------------------------
### Server[​](#server-1 "Direct link to Server")
cookbook/websocket/gorilla/server.go
```
package main  
  
import (  
	"fmt"  
  
	"github.com/gorilla/websocket"  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
)  
  
var (  
	upgrader = websocket.Upgrader{}  
)  
  
func hello(c echo.Context) error {  
	ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)  
	if err != nil {  
		return err  
	}  
	defer ws.Close()  
  
	for {  
		// Write  
		err := ws.WriteMessage(websocket.TextMessage, []byte("Hello, Client!"))  
		if err != nil {  
			c.Logger().Error(err)  
		}  
  
		// Read  
		_, msg, err := ws.ReadMessage()  
		if err != nil {  
			c.Logger().Error(err)  
		}  
		fmt.Printf("%s\n", msg)  
	}  
}  
  
func main() {  
	e := echo.New()  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
	e.Static("/", "../public")  
	e.GET("/ws", hello)  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Client[​](#client "Direct link to Client")
------------------------------------------
cookbook/websocket/public/index.html
```
<!doctype html>  
<html lang="en">  
  
<head>  
  <meta charset="utf-8">  
  <title>WebSocket</title>  
</head>  
  
<body>  
  <p id="output"></p>  
  
  <script>  
    var loc = window.location;  
    var uri = 'ws:';  
  
    if (loc.protocol === 'https:') {  
      uri = 'wss:';  
    }  
    uri += '//' + loc.host;  
    uri += loc.pathname + 'ws';  
  
    ws = new WebSocket(uri)  
  
    ws.onopen = function() {  
      console.log('Connected')  
    }  
  
    ws.onmessage = function(evt) {  
      var out = document.getElementById('output');  
      out.innerHTML += evt.data + '<br>';  
    }  
  
    setInterval(function() {  
      ws.send('Hello, Server!');  
    }, 1000);  
  </script>  
</body>  
  
</html>
```
Output[​](#output "Direct link to Output")
------------------------------------------
```
Hello, Client!  
Hello, Client!  
Hello, Client!  
Hello, Client!  
Hello, Client!
```
```
Hello, Server!  
Hello, Server!  
Hello, Server!  
Hello, Server!  
Hello, Server!
```
[Previous
Twitter Like API](/docs/cookbook/twitter)