CSRF

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
* CSRF
On this page
CSRF
====
Cross-site request forgery, also known as one-click attack or session riding and
abbreviated as CSRF (sometimes pronounced sea-surf) or XSRF, is a type of malicious
exploit of a website where unauthorized commands are transmitted from a user that
the website trusts.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Use(middleware.CSRF())
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.CSRFWithConfig(middleware.CSRFConfig{  
  TokenLookup: "header:X-XSRF-TOKEN",  
}))
```
Example above uses `X-XSRF-TOKEN` request header to extract CSRF token.
*Example Configuration that reads token from Cookie*
```
middleware.CSRFWithConfig(middleware.CSRFConfig{  
	TokenLookup:    "cookie:_csrf",  
	CookiePath:     "/",  
	CookieDomain:   "example.com",  
	CookieSecure:   true,  
	CookieHTTPOnly: true,  
	CookieSameSite: http.SameSiteStrictMode,  
})
```
Accessing CSRF Token[​](#accessing-csrf-token "Direct link to Accessing CSRF Token")
------------------------------------------------------------------------------------
### Server-side[​](#server-side "Direct link to Server-side")
CSRF token can be accessed from `Echo#Context` using `ContextKey` and passed to
the client via template.
### Client-side[​](#client-side "Direct link to Client-side")
CSRF token can be accessed from CSRF cookie.
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
CSRFConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // TokenLength is the length of the generated token.  
  TokenLength uint8 `json:"token_length"`  
  // Optional. Default value 32.  
  
  // TokenLookup is a string in the form of "<source>:<key>" that is used  
  // to extract token from the request.  
  // Optional. Default value "header:X-CSRF-Token".  
  // Possible values:  
  // - "header:<name>"  
  // - "form:<name>"  
  // - "query:<name>"  
  // - "cookie:<name>"  
  TokenLookup string `json:"token_lookup"`  
  
  // Context key to store generated CSRF token into context.  
  // Optional. Default value "csrf".  
  ContextKey string `json:"context_key"`  
  
  // Name of the CSRF cookie. This cookie will store CSRF token.  
  // Optional. Default value "_csrf".  
  CookieName string `json:"cookie_name"`  
  
  // Domain of the CSRF cookie.  
  // Optional. Default value none.  
  CookieDomain string `json:"cookie_domain"`  
  
  // Path of the CSRF cookie.  
  // Optional. Default value none.  
  CookiePath string `json:"cookie_path"`  
  
  // Max age (in seconds) of the CSRF cookie.  
  // Optional. Default value 86400 (24hr).  
  CookieMaxAge int `json:"cookie_max_age"`  
  
  // Indicates if CSRF cookie is secure.  
  // Optional. Default value false.  
  CookieSecure bool `json:"cookie_secure"`  
  
  // Indicates if CSRF cookie is HTTP only.  
  // Optional. Default value false.  
  CookieHTTPOnly bool `json:"cookie_http_only"`  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultCSRFConfig = CSRFConfig{  
  Skipper:      DefaultSkipper,  
  TokenLength:  32,  
  TokenLookup:  "header:" + echo.HeaderXCSRFToken,  
  ContextKey:   "csrf",  
  CookieName:   "_csrf",  
  CookieMaxAge: 86400,  
}
```