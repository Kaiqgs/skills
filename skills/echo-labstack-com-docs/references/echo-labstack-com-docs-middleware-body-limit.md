Body Limit

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
* Body Limit
On this page
Body Limit
==========
Body limit middleware sets the maximum allowed size for a request body, if the
size exceeds the configured limit, it sends "413 - Request Entity Too Large"
response. The body limit is determined based on both `Content-Length` request
header and actual content read, which makes it super secure.
Limit can be specified as `4x` or `4xB`, where x is one of the multiple from K, M,
G, T or P.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e := echo.New()  
e.Use(middleware.BodyLimit("2M"))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.BodyLimitWithConfig(middleware.BodyLimitConfig{}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
BodyLimitConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Maximum allowed size for a request body, it can be specified  
  // as `4x` or `4xB`, where x is one of the multiple from K, M, G, T or P.  
  Limit string `json:"limit"`  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultBodyLimitConfig = BodyLimitConfig{  
  Skipper: DefaultSkipper,  
}
```