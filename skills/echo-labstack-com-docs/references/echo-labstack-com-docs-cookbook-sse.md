Server-Sent-Events (SSE)

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
* Server-Sent-Events (SSE)
On this page
Server-Sent-Events (SSE)
========================
[Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format) can be
used in different ways. This example here is per connection - per handler SSE. If your requirements need more complex
broadcasting logic see <https://github.com/r3labs/sse> library.
Using SSE[​](#using-sse "Direct link to Using SSE")
---------------------------------------------------
### Server[​](#server "Direct link to Server")
cookbook/sse/simple/server.go
```
package main  
  
import (  
	"errors"  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"log"  
	"net/http"  
	"time"  
)  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
	e.File("/", "./index.html")  
  
	e.GET("/sse", func(c echo.Context) error {  
		log.Printf("SSE client connected, ip: %v", c.RealIP())  
  
		w := c.Response()  
		w.Header().Set("Content-Type", "text/event-stream")  
		w.Header().Set("Cache-Control", "no-cache")  
		w.Header().Set("Connection", "keep-alive")  
  
		ticker := time.NewTicker(1 * time.Second)  
		defer ticker.Stop()  
		for {  
			select {  
			case <-c.Request().Context().Done():  
				log.Printf("SSE client disconnected, ip: %v", c.RealIP())  
				return nil  
			case <-ticker.C:  
				event := Event{  
					Data: []byte("time: " + time.Now().Format(time.RFC3339Nano)),  
				}  
				if err := event.MarshalTo(w); err != nil {  
					return err  
				}  
				w.Flush()  
			}  
		}  
	})  
  
	if err := e.Start(":8080"); err != nil && !errors.Is(err, http.ErrServerClosed) {  
		log.Fatal(err)  
	}  
}
```
### Event structure and Marshal method[​](#event-structure-and-marshal-method "Direct link to Event structure and Marshal method")
cookbook/sse/simple/serversentevent.go
```
package main  
  
import (  
	"bytes"  
	"fmt"  
	"io"  
)  
  
// Event represents Server-Sent Event.  
// SSE explanation: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format  
type Event struct {  
	// ID is used to set the EventSource object's last event ID value.  
	ID []byte  
	// Data field is for the message. When the EventSource receives multiple consecutive lines  
	// that begin with data:, it concatenates them, inserting a newline character between each one.  
	// Trailing newlines are removed.  
	Data []byte  
	// Event is a string identifying the type of event described. If this is specified, an event  
	// will be dispatched on the browser to the listener for the specified event name; the website  
	// source code should use addEventListener() to listen for named events. The onmessage handler  
	// is called if no event name is specified for a message.  
	Event []byte  
	// Retry is the reconnection time. If the connection to the server is lost, the browser will  
	// wait for the specified time before attempting to reconnect. This must be an integer, specifying  
	// the reconnection time in milliseconds. If a non-integer value is specified, the field is ignored.  
	Retry []byte  
	// Comment line can be used to prevent connections from timing out; a server can send a comment  
	// periodically to keep the connection alive.  
	Comment []byte  
}  
  
// MarshalTo marshals Event to given Writer  
func (ev *Event) MarshalTo(w io.Writer) error {  
	// Marshalling part is taken from: https://github.com/r3labs/sse/blob/c6d5381ee3ca63828b321c16baa008fd6c0b4564/http.go#L16  
	if len(ev.Data) == 0 && len(ev.Comment) == 0 {  
		return nil  
	}  
  
	if len(ev.Data) > 0 {  
		if _, err := fmt.Fprintf(w, "id: %s\n", ev.ID); err != nil {  
			return err  
		}  
  
		sd := bytes.Split(ev.Data, []byte("\n"))  
		for i := range sd {  
			if _, err := fmt.Fprintf(w, "data: %s\n", sd[i]); err != nil {  
				return err  
			}  
		}  
  
		if len(ev.Event) > 0 {  
			if _, err := fmt.Fprintf(w, "event: %s\n", ev.Event); err != nil {  
				return err  
			}  
		}  
  
		if len(ev.Retry) > 0 {  
			if _, err := fmt.Fprintf(w, "retry: %s\n", ev.Retry); err != nil {  
				return err  
			}  
		}  
	}  
  
	if len(ev.Comment) > 0 {  
		if _, err := fmt.Fprintf(w, ": %s\n", ev.Comment); err != nil {  
			return err  
		}  
	}  
  
	if _, err := fmt.Fprint(w, "\n"); err != nil {  
		return err  
	}  
  
	return nil  
}
```
### HTML serving SSE[​](#html-serving-sse "Direct link to HTML serving SSE")
cookbook/sse/simple/index.html
```
<!DOCTYPE html>  
<html>  
<body>  
  
<h1>Getting server-sent updates</h1>  
<div id="result"></div>  
  
<script>  
    // Example taken from: https://www.w3schools.com/html/html5_serversentevents.asp  
    if (typeof (EventSource) !== "undefined") {  
        const source = new EventSource("/sse");  
        source.onmessage = function (event) {  
            document.getElementById("result").innerHTML += event.data + "<br>";  
        };  
    } else {  
        document.getElementById("result").innerHTML = "Sorry, your browser does not support server-sent events...";  
    }  
</script>  
  
</body>  
</html>
```
Using 3rd party library [r3labs/sse](https://github.com/r3labs/sse) to broadcast events[​](#using-3rd-party-library-r3labssse-to-broadcast-events "Direct link to using-3rd-party-library-r3labssse-to-broadcast-events")
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
### Server[​](#server-1 "Direct link to Server")
cookbook/sse/broadcast/server.go
```
package main  
  
import (  
	"errors"  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"github.com/r3labs/sse/v2"  
	"log"  
	"net/http"  
	"time"  
)  
  
func main() {  
	e := echo.New()  
  
	server := sse.New()             // create SSE broadcaster server  
	server.AutoReplay = false       // do not replay messages for each new subscriber that connects  
	_ = server.CreateStream("time") // EventSource in "index.html" connecting to stream named "time"  
  
	go func(s *sse.Server) {  
		ticker := time.NewTicker(1 * time.Second)  
		defer ticker.Stop()  
  
		for {  
			select {  
			case <-ticker.C:  
				s.Publish("time", &sse.Event{  
					Data: []byte("time: " + time.Now().Format(time.RFC3339Nano)),  
				})  
			}  
		}  
	}(server)  
  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
	e.File("/", "./index.html")  
  
	//e.GET("/sse", echo.WrapHandler(server))  
  
	e.GET("/sse", func(c echo.Context) error { // longer variant with disconnect logic  
		log.Printf("The client is connected: %v\n", c.RealIP())  
		go func() {  
			<-c.Request().Context().Done() // Received Browser Disconnection  
			log.Printf("The client is disconnected: %v\n", c.RealIP())  
			return  
		}()  
  
		server.ServeHTTP(c.Response(), c.Request())  
		return nil  
	})  
  
	if err := e.Start(":8080"); err != nil && !errors.Is(err, http.ErrServerClosed) {  
		log.Fatal(err)  
	}  
}
```
### HTML serving SSE[​](#html-serving-sse-1 "Direct link to HTML serving SSE")
cookbook/sse/broadcast/index.html
```
<!DOCTYPE html>  
<html>  
<body>  
  
<h1>Getting server-sent updates</h1>  
<div id="result"></div>  
  
<script>  
    // Example taken from: https://www.w3schools.com/html/html5_serversentevents.asp  
    if (typeof (EventSource) !== "undefined") {  
        const source = new EventSource("/sse?stream=time");  
        source.onmessage = function (event) {  
            document.getElementById("result").innerHTML += event.data + "<br>";  
        };  
    } else {  
        document.getElementById("result").innerHTML = "Sorry, your browser does not support server-sent events...";  
    }  
</script>  
  
</body>  
</html>
```