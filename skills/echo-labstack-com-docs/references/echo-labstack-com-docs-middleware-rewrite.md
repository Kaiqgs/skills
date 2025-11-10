Rewrite

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
* Rewrite
On this page
Rewrite
=======
Rewrite middleware allows to rewrite an URL path based on provided rules. It can be helpful for backward compatibility or just creating cleaner and more descriptive links.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e.Pre(middleware.Rewrite(map[string]string{  
  "/old":              "/new",  
  "/api/*":            "/$1",  
  "/js/*":             "/public/javascripts/$1",  
  "/users/*/orders/*": "/user/$1/order/$2",  
}))
```
The values captured in asterisk can be retrieved by index e.g. $1, $2 and so on.
Each asterisk will be non-greedy (translated to a capture group `(.*?)`) and if using
multiple asterisk a trailing `*` will match the "rest" of the path.
caution
Rewrite middleware should be registered via `Echo#Pre()` to get triggered before the router.
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Pre(middleware.RewriteWithConfig(middleware.RewriteConfig{}))
```
### Configuration[​](#configuration "Direct link to Configuration")
```
// RewriteConfig defines the config for Rewrite middleware.  
  RewriteConfig struct {  
    // Skipper defines a function to skip middleware.  
    Skipper Skipper  
  
    // Rules defines the URL path rewrite rules. The values captured in asterisk can be  
    // retrieved by index e.g. $1, $2 and so on.  
    Rules map[string]string `yaml:"rules"`  
  
    // RegexRules defines the URL path rewrite rules using regexp.Rexexp with captures  
    // Every capture group in the values can be retrieved by index e.g. $1, $2 and so on.  
    RegexRules map[*regexp.Regexp]string  
  }
```
Default Configuration:
| Name | Value |
| --- | --- |
| Skipper | DefaultSkipper |
### Regex-based Rules[​](#regex-based-rules "Direct link to Regex-based Rules")
For advanced rewriting of paths rules may also be defined using regular expression.
Normal capture groups can be defined using `()` and referenced by index (`$1`, `$2`, ...) for the rewritten path.
`RegexRules` and normal `Rules` can be combined.
```
  e.Pre(RewriteWithConfig(RewriteConfig{  
    Rules: map[string]string{  
      "^/v1/*": "/v2/$1",  
    },  
    RegexRules: map[*regexp.Regexp]string{  
      regexp.MustCompile("^/foo/([0-9].*)"):  "/num/$1",  
      regexp.MustCompile("^/bar/(.+?)/(.*)"): "/baz/$2/$1",  
    },  
  }))
```