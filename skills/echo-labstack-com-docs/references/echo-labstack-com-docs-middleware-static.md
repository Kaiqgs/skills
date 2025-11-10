Static

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
* Static
On this page
Static
======
Static middleware can be used to serve static files from the provided root directory.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
e := echo.New()  
e.Use(middleware.Static("/static"))
```
This serves static files from `static` directory. For example, a request to `/js/main.js`
will fetch and serve `static/js/main.js` file.
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
### Usage[​](#usage-1 "Direct link to Usage")
```
e := echo.New()  
e.Use(middleware.StaticWithConfig(middleware.StaticConfig{  
  Root:   "static",  
  Browse: true,  
}))
```
This serves static files from `static` directory and enables directory browsing.
Default behavior when using with non root URL paths is to append the URL path to the filesystem path.
#### Example 1[​](#example-1 "Direct link to Example 1")
```
group := root.Group("somepath")  
group.Use(middleware.Static(filepath.Join("filesystempath")))  
// When an incoming request comes for `/somepath` the actual filesystem request goes to `filesystempath/somepath` instead of only `filesystempath`.
```
tip
To turn off this behavior set the `IgnoreBase` config param to `true`.
#### Example 2[​](#example-2 "Direct link to Example 2")
Serve SPA assets from embedded filesystem
```
//go:embed web  
var webAssets embed.FS  
  
func main() {  
	e := echo.New()  
  
	e.Use(middleware.StaticWithConfig(middleware.StaticConfig{  
		HTML5:      true,  
		Root:       "web", // because files are located in `web` directory in `webAssets` fs  
		Filesystem: http.FS(webAssets),  
	}))  
	api := e.Group("/api")  
	api.GET("/users", func(c echo.Context) error {  
		return c.String(http.StatusOK, "users")  
	})  
  
	if err := e.Start(":8080"); err != nil && !errors.Is(err, http.ErrServerClosed) {  
		log.Fatal(err)  
	}  
}
```
Configuration[​](#configuration "Direct link to Configuration")
---------------------------------------------------------------
```
StaticConfig struct {  
  // Skipper defines a function to skip middleware.  
  Skipper Skipper  
  
  // Root directory from where the static content is served.  
  // Required.  
  Root string `json:"root"`  
  
  // Index file for serving a directory.  
  // Optional. Default value "index.html".  
  Index string `json:"index"`  
  
  // Enable HTML5 mode by forwarding all not-found requests to root so that  
  // SPA (single-page application) can handle the routing.  
  // Optional. Default value false.  
  HTML5 bool `json:"html5"`  
  
  // Enable directory browsing.  
  // Optional. Default value false.  
  Browse bool `json:"browse"`  
    
  // Enable ignoring of the base of the URL path.  
  // Example: when assigning a static middleware to a non root path group,  
  // the filesystem path is not doubled  
  // Optional. Default value false.  
  IgnoreBase bool `yaml:"ignoreBase"`  
  
  // Filesystem provides access to the static content.  
  // Optional. Defaults to http.Dir(config.Root)  
  Filesystem http.FileSystem `yaml:"-"`  
}
```
### Default Configuration[​](#default-configuration "Direct link to Default Configuration")
```
DefaultStaticConfig = StaticConfig{  
  Skipper: DefaultSkipper,  
  Index:   "index.html",  
}
```