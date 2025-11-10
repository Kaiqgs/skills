Decompress

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
* Decompress
On this page
Decompress
==========
Decompress middleware decompresses HTTP request if Content-Encoding header is set to gzip.
note
The body will be decompressed in memory and consume it for the lifetime of the request (and garbage collection).
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Use(middleware.Decompress())
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.DecompressWithConfig(middleware.DecompressConfig{  
  Skipper: Skipper  
}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
DecompressConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultDecompressConfig = DecompressConfig{  
  Skipper: DefaultSkipper,  
}
```