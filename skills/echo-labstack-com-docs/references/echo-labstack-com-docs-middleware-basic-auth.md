Basic Auth

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
* Basic Auth
On this page
Basic Auth
==========
Basic auth middleware provides an HTTP basic authentication.
* For valid credentials it calls the next handler.
* For missing or invalid credentials, it sends "401 - Unauthorized" response.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Use(middleware.BasicAuth(func(username, password string, c echo.Context) (bool, error) {  
	// Be careful to use constant time comparison to prevent timing attacks  
	if subtle.ConstantTimeCompare([]byte(username), []byte("joe")) == 1 &&  
		subtle.ConstantTimeCompare([]byte(password), []byte("secret")) == 1 {  
		return true, nil  
	}  
	return false, nil  
}))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e.Use(middleware.BasicAuthWithConfig(middleware.BasicAuthConfig{}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
BasicAuthConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Validator is a function to validate BasicAuth credentials.  
  // Required.  
  Validator BasicAuthValidator  
  
  // Realm is a string to define realm attribute of BasicAuth.  
  // Default value "Restricted".  
  Realm string  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultBasicAuthConfig = BasicAuthConfig{  
	Skipper: DefaultSkipper,  
}
```