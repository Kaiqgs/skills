Proxy

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
* Proxy
On this page
Proxy
=====
Proxy provides an HTTP/WebSocket reverse proxy middleware. It forwards a request
to upstream server using a configured load balancing technique.
### Usage[​](#usage "Direct link to Usage")
```
url1, err := url.Parse("http://localhost:8081")  
if err != nil {  
  e.Logger.Fatal(err)  
}  
url2, err := url.Parse("http://localhost:8082")  
if err != nil {  
  e.Logger.Fatal(err)  
}  
e.Use(middleware.Proxy(middleware.NewRoundRobinBalancer([]*middleware.ProxyTarget{  
  {  
    URL: url1,  
  },  
  {  
    URL: url2,  
  },  
})))
```
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.ProxyWithConfig(middleware.ProxyConfig{}))
```
### Configuration[​](#configuration "Direct link to Configuration")
```
// ProxyConfig defines the config for Proxy middleware.  
  ProxyConfig struct {  
    // Skipper defines a function to skip middleware.  
    Skipper Skipper  
  
    // Balancer defines a load balancing technique.  
    // Required.  
    Balancer ProxyBalancer  
  
    // Rewrite defines URL path rewrite rules. The values captured in asterisk can be  
    // retrieved by index e.g. $1, $2 and so on.  
    Rewrite map[string]string  
  
    // RegexRewrite defines rewrite rules using regexp.Rexexp with captures  
    // Every capture group in the values can be retrieved by index e.g. $1, $2 and so on.  
    RegexRewrite map[*regexp.Regexp]string  
  
    // Context key to store selected ProxyTarget into context.  
    // Optional. Default value "target".  
    ContextKey string  
  
    // To customize the transport to remote.  
    // Examples: If custom TLS certificates are required.  
    Transport http.RoundTripper  
  
    // ModifyResponse defines function to modify response from ProxyTarget.  
    ModifyResponse func(*http.Response) error
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
| Name | Value |
| --- | --- |
| Skipper | DefaultSkipper |
| ContextKey | `target` |
### Regex-based Rules[​](#regex-based-rules "Direct link to Regex-based Rules")
For advanced rewriting of proxy requests rules may also be defined using
regular expression. Normal capture groups can be defined using `()` and referenced by index (`$1`, `$2`, ...) for the rewritten path.
`RegexRules` and normal `Rules` can be combined.
```
  e.Use(ProxyWithConfig(ProxyConfig{  
    Balancer: rrb,  
    Rewrite: map[string]string{  
      "^/v1/*":     "/v2/$1",  
    },  
    RegexRewrite: map[*regexp.Regexp]string{  
      regexp.MustCompile("^/foo/([0-9].*)"):  "/num/$1",  
      regexp.MustCompile("^/bar/(.+?)/(.*)"): "/baz/$2/$1",  
    },  
  }))
```
[Example](/docs/cookbook/reverse-proxy)[​](#example "Direct link to example")
-----------------------------------------------------------------------------