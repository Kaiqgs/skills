Redirect

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
* Redirect
On this page
Redirect
========
HTTPS Redirect[​](#https-redirect "Direct link to HTTPS Redirect")
------------------------------------------------------------------
HTTPS redirect middleware redirects http requests to https.
For example, <http://labstack.com> will be redirected to <https://labstack.com>.
### Usage[​](#usage "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.HTTPSRedirect())
```
HTTPS WWW Redirect[​](#https-www-redirect "Direct link to HTTPS WWW Redirect")
------------------------------------------------------------------------------
HTTPS WWW redirect redirects http requests to www https.
For example, <http://labstack.com> will be redirected to <https://www.labstack.com>.
Usage[​](#usage-1 "Direct link to Usage")
-----------------------------------------
```
e := echo.New()  
e.Pre(middleware.HTTPSWWWRedirect())
```
HTTPS NonWWW Redirect[​](#https-nonwww-redirect "Direct link to HTTPS NonWWW Redirect")
---------------------------------------------------------------------------------------
HTTPS NonWWW redirect redirects http requests to https non [www](http://www).
For example, <http://www.labstack.com> will be redirect to <https://labstack.com>.
### Usage[​](#usage-2 "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.HTTPSNonWWWRedirect())
```
WWW Redirect[​](#www-redirect "Direct link to WWW Redirect")
------------------------------------------------------------
WWW redirect redirects non www requests to [www](http://www).
For example, <http://labstack.com> will be redirected to <http://www.labstack.com>.
### Usage[​](#usage-3 "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.WWWRedirect())
```
NonWWW Redirect[​](#nonwww-redirect "Direct link to NonWWW Redirect")
---------------------------------------------------------------------
NonWWW redirect redirects www requests to non [www](http://www).
For example, <http://www.labstack.com> will be redirected to <http://labstack.com>.
### Usage[​](#usage-4 "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.NonWWWRedirect())
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-5 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.HTTPSRedirectWithConfig(middleware.RedirectConfig{  
  Code: http.StatusTemporaryRedirect,  
}))
```
Example above will redirect the request HTTP to HTTPS with status code `307 - StatusTemporaryRedirect`.
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
RedirectConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Status code to be used when redirecting the request.  
  // Optional. Default value http.StatusMovedPermanently.  
  Code int `json:"code"`  
}
```
### Default Configuration\*[​](#default-configuration "Direct link to Default Configuration*")
```
DefaultRedirectConfig = RedirectConfig{  
  Skipper: DefaultSkipper,  
  Code:    http.StatusMovedPermanently,  
}
```