Key Auth

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
* Key Auth
On this page
Key Auth
========
Key auth middleware provides a key based authentication.
* For valid key it calls the next handler.
* For invalid key, it sends "401 - Unauthorized" response.
* For missing key, it sends "400 - Bad Request" response.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Use(middleware.KeyAuth(func(key string, c echo.Context) (bool, error) {  
  return key == "valid-key", nil  
}))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.KeyAuthWithConfig(middleware.KeyAuthConfig{  
  KeyLookup: "query:api-key",  
  Validator: func(key string, c echo.Context) (bool, error) {  
			return key == "valid-key", nil  
		},  
}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
KeyAuthConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // KeyLookup is a string in the form of "<source>:<name>" that is used  
  // to extract key from the request.  
  // Optional. Default value "header:Authorization".  
  // Possible values:  
  // - "header:<name>"  
  // - "query:<name>"  
  // - "cookie:<name>"  
  // - "form:<name>"  
  KeyLookup string `yaml:"key_lookup"`  
  
  // AuthScheme to be used in the Authorization header.  
  // Optional. Default value "Bearer".  
  AuthScheme string  
  
  // Validator is a function to validate key.  
  // Required.  
  Validator KeyAuthValidator  
  
  // ErrorHandler defines a function which is executed for an invalid key.  
  // It may be used to define a custom error.  
  ErrorHandler KeyAuthErrorHandler  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultKeyAuthConfig = KeyAuthConfig{  
  Skipper:    DefaultSkipper,  
  KeyLookup:  "header:" + echo.HeaderAuthorization,  
  AuthScheme: "Bearer",  
}
```