Trailing Slash

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
* Trailing Slash
On this page
Trailing Slash
==============
Add Trailing Slash[​](#add-trailing-slash "Direct link to Add Trailing Slash")
------------------------------------------------------------------------------
Add trailing slash middleware adds a trailing slash to the request URI.
### Usage[​](#usage "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.AddTrailingSlash())
```
Remove Trailing Slash[​](#remove-trailing-slash "Direct link to Remove Trailing Slash")
---------------------------------------------------------------------------------------
Remove trailing slash middleware removes a trailing slash from the request URI.
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.RemoveTrailingSlash())
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-2 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.AddTrailingSlashWithConfig(middleware.TrailingSlashConfig{  
  RedirectCode: http.StatusMovedPermanently,  
}))
```
Example above will add a trailing slash to the request URI and redirect with `301 - StatusMovedPermanently`.
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
TrailingSlashConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Status code to be used when redirecting the request.  
  // Optional, but when provided the request is redirected using this code.  
  RedirectCode int `json:"redirect_code"`  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultTrailingSlashConfig = TrailingSlashConfig{  
  Skipper: DefaultSkipper,  
}
```