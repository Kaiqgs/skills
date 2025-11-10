Body Dump

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
* Body Dump
On this page
Body Dump
=========
Body dump middleware captures the request and response payload and calls the registered handler. Generally used for debugging/logging purpose. Avoid using it if your request/response payload is huge e.g. file upload/download, but if you still need to, add an exception for your endpoints in the skipper function.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e := echo.New()  
e.Use(middleware.BodyDump(func(c echo.Context, reqBody, resBody []byte) {  
}))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.BodyDumpWithConfig(middleware.BodyDumpConfig{}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
BodyDumpConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Handler receives request and response payload.  
  // Required.  
  Handler BodyDumpHandler  
}
```
### Default Configuration\*[​](#default-configuration "Direct link to Default Configuration*")
```
DefaultBodyDumpConfig = BodyDumpConfig{  
  Skipper: DefaultSkipper,  
}
```