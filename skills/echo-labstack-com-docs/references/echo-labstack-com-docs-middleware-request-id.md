Request ID

* [Introduction](/docs)
* [Guide](/docs/category/guide)
* [Middleware](/docs/category/middleware)
  + [Basic Auth](/docs/middleware/basic-auth)
  + [Body Dump](/docs/middleware/body-dump)
  + [Body Limit](/docs/middleware/body-limit)
  + [Casbin Auth](/docs/middleware/casbin-auth)
  + [Context Timeout](/docs/middleware/context-timeout)
  + [CORS](/docs/middleware/cors)
  + [CSRF](/docs/middleware/csrf)
  + [Decompress](/docs/middleware/decompress)
  + [Gzip](/docs/middleware/gzip)
  + [Jaeger](/docs/middleware/jaeger)
  + [JWT](/docs/middleware/jwt)
  + [Key Auth](/docs/middleware/key-auth)
  + [Logger](/docs/middleware/logger)
  + [Method Override](/docs/middleware/method-override)
  + [Prometheus](/docs/middleware/prometheus)
  + [Proxy](/docs/middleware/proxy)
  + [Rate Limiter](/docs/middleware/rate-limiter)
  + [Recover](/docs/middleware/recover)
  + [Redirect](/docs/middleware/redirect)
  + [Request ID](/docs/middleware/request-id)
  + [Rewrite](/docs/middleware/rewrite)
  + [Secure](/docs/middleware/secure)
  + [Session](/docs/middleware/session)
  + [Static](/docs/middleware/static)
  + [Trailing Slash](/docs/middleware/trailing-slash)
* [Cookbook](/docs/category/cookbook)
* [Middleware](/docs/category/middleware)
* Request ID
On this page
Request ID
==========
Request ID middleware generates a unique id for a request.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Use(middleware.RequestID())
```
*Example*
```
    e := echo.New()  
  
    e.Use(middleware.RequestID())  
  
    e.GET("/", func(c echo.Context) error {  
        return c.String(http.StatusOK, c.Response().Header().Get(echo.HeaderXRequestID))  
    })  
    e.Logger.Fatal(e.Start(":1323"))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e.Use(middleware.RequestIDWithConfig(middleware.RequestIDConfig{  
  Generator: func() string {  
    return customGenerator()  
  },  
}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
RequestIDConfig struct {  
    // Skipper defines a function to skip middleware.  
    Skipper Skipper  
  
    // Generator defines a function to generate an ID.  
    // Optional. Default value random.String(32).  
    Generator func() string  
  
    // RequestIDHandler defines a function which is executed for a request id.  
    RequestIDHandler func(echo.Context, string)  
  
    // TargetHeader defines what header to look for to populate the id  
    TargetHeader string  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultRequestIDConfig = RequestIDConfig{  
  Skipper:   DefaultSkipper,  
  Generator: generator,  
  TargetHeader: echo.HeaderXRequestID,  
}
```
Set ID[​](#set-id "Direct link to Set ID")
------------------------------------------
You can set the id from the requester with the `X-Request-ID`-Header
### Request[​](#request "Direct link to Request")
```
curl -H "X-Request-ID: 3" --compressed -v "http://localhost:1323/?my=param"
```
### Log[​](#log "Direct link to Log")
```
{"time":"2017-11-13T20:26:28.6438003+01:00","id":"3","remote_ip":"::1","host":"localhost:1323","method":"GET","uri":"/?my=param","my":"param","status":200, "latency":0,"latency_human":"0s","bytes_in":0,"bytes_out":13}
```