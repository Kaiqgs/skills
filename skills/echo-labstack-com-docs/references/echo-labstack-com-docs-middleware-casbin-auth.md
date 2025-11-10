Casbin Auth

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
* Casbin Auth
On this page
Casbin Auth
===========
note
Echo community contribution
[Casbin](https://github.com/casbin/casbin) is a powerful and efficient open-source access control library for Go. It provides support for enforcing authorization based on various models. So far, the access control models supported by Casbin are:
* ACL (Access Control List)
* ACL with superuser
* ACL without users: especially useful for systems that don't have authentication or user log-ins.
* ACL without resources: some scenarios may target for a type of resources instead of an individual resource by using permissions like write-article, read-log. It doesn't control the access to a specific article or log.
* RBAC (Role-Based Access Control)
* RBAC with resource roles: both users and resources can have roles (or groups) at the same time.
* RBAC with domains/tenants: users can have different role sets for different domains/tenants.
* ABAC (Attribute-Based Access Control)
* RESTful
* Deny-override: both allow and deny authorizations are supported, deny overrides the allow.
info
Currently, only HTTP basic authentication is supported.
Dependencies[​](#dependencies "Direct link to Dependencies")
------------------------------------------------------------
```
import (  
  "github.com/casbin/casbin"  
  casbin_mw "github.com/labstack/echo-contrib/casbin"  
)
```
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e := echo.New()  
enforcer, err := casbin.NewEnforcer("casbin_auth_model.conf", "casbin_auth_policy.csv")  
e.Use(casbin_mw.Middleware(enforcer))
```
For syntax, see: [Syntax for Models](https://casbin.org/docs/syntax-for-models).
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
ce := casbin.NewEnforcer("casbin_auth_model.conf", "")  
ce.AddRoleForUser("alice", "admin")  
ce.AddPolicy(...)  
e.Use(casbin_mw.MiddlewareWithConfig(casbin_mw.Config{  
  Enforcer: ce,  
}))
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
// Config defines the config for CasbinAuth middleware.  
Config struct {  
  // Skipper defines a function to skip middleware.  
  Skipper middleware.Skipper  
  
  // Enforcer CasbinAuth main rule.  
  // Required.  
  Enforcer *casbin.Enforcer  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
// DefaultConfig is the default CasbinAuth middleware config.  
DefaultConfig = Config{  
  Skipper: middleware.DefaultSkipper,  
}
```