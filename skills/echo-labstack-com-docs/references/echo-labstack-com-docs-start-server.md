Start Server

* [Introduction](/docs)
* [Guide](/docs/category/guide)
  + [Quick Start](/docs/quick-start)
  + [Customization](/docs/customization)
  + [Binding](/docs/binding)
  + [Context](/docs/context)
  + [Cookies](/docs/cookies)
  + [Error Handling](/docs/error-handling)
  + [Start Server](/docs/start-server)
  + [IP Address](/docs/ip-address)
  + [Request](/docs/request)
  + [Response](/docs/response)
  + [Routing](/docs/routing)
  + [Static Files](/docs/static-files)
  + [Templates](/docs/templates)
  + [Testing](/docs/testing)
* [Middleware](/docs/category/middleware)
* [Cookbook](/docs/category/cookbook)
* [Guide](/docs/category/guide)
* Start Server
On this page
Start Server
============
Echo provides following convenience methods to start the server:
* `Echo.Start(address string)`
* `Echo.StartTLS(address string, certFile, keyFile interface{})`
* `Echo.StartAutoTLS(address string)`
* `Echo.StartH2CServer(address string, h2s *http2.Server)`
* `Echo.StartServer(s *http.Server)`
HTTP Server[​](#http-server "Direct link to HTTP Server")
---------------------------------------------------------
`Echo.Start` is convenience method that starts http server with Echo serving requests.
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  if err := e.Start(":8080"); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```
Following is equivalent to `Echo.Start` previous example
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  s := http.Server{  
    Addr:        ":8080",  
    Handler:     e,  
    //ReadTimeout: 30 * time.Second, // customize http.Server timeouts  
  }  
  if err := s.ListenAndServe(); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```
HTTPS Server[​](#https-server "Direct link to HTTPS Server")
------------------------------------------------------------
`Echo.StartTLS` is convenience method that starts HTTPS server with Echo serving requests on given address and uses
`server.crt` and `server.key` as TLS certificate pair.
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  if err := e.StartTLS(":8443", "server.crt", "server.key"); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```
Following is equivalent to `Echo.StartTLS` previous example
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  s := http.Server{  
    Addr:    ":8443",  
    Handler: e, // set Echo as handler  
    TLSConfig: &tls.Config{  
      //MinVersion: 1, // customize TLS configuration  
    },  
    //ReadTimeout: 30 * time.Second, // use custom timeouts  
  }  
  if err := s.ListenAndServeTLS("server.crt", "server.key"); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```
Auto TLS Server with Let’s Encrypt[​](#auto-tls-server-with-lets-encrypt "Direct link to Auto TLS Server with Let’s Encrypt")
-----------------------------------------------------------------------------------------------------------------------------
See [Auto TLS Recipe](/docs/cookbook/auto-tls#server)
HTTP/2 Cleartext Server (HTTP2 over HTTP)[​](#http2-cleartext-server-http2-over-http "Direct link to HTTP/2 Cleartext Server (HTTP2 over HTTP)")
------------------------------------------------------------------------------------------------------------------------------------------------
`Echo.StartH2CServer` is convenience method that starts a custom HTTP/2 cleartext server on given address
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  s := &http2.Server{  
    MaxConcurrentStreams: 250,  
    MaxReadFrameSize:     1048576,  
    IdleTimeout:          10 * time.Second,  
  }  
  if err := e.StartH2CServer(":8080", s); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```
Following is equivalent to `Echo.StartH2CServer` previous example
```
func main() {  
  e := echo.New()  
  // add middleware and routes  
  // ...  
  h2s := &http2.Server{  
    MaxConcurrentStreams: 250,  
    MaxReadFrameSize:     1048576,  
    IdleTimeout:          10 * time.Second,  
  }  
  s := http.Server{  
    Addr:    ":8080",  
    Handler: h2c.NewHandler(e, h2s),  
  }  
  if err := s.ListenAndServe(); err != http.ErrServerClosed {  
    log.Fatal(err)  
  }  
}
```