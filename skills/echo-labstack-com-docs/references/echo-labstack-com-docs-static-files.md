Static Files

* [Introduction](/docs)
* [Guide](/docs/category/guide)
  + [Quick Start](/docs/quick-start)
  + [Customization](/docs/customization)
  + [Binding](/docs/binding)
  + [Context](/docs/context)
  + [Cookies](/docs/cookies)
  + [Error Handling](/docs/error-handling)
  + [Start Server](/docs/start-server)
  + [IP Address](/docs/ip-address)
  + [Request](/docs/request)
  + [Response](/docs/response)
  + [Routing](/docs/routing)
  + [Static Files](/docs/static-files)
  + [Templates](/docs/templates)
  + [Testing](/docs/testing)
* [Middleware](/docs/category/middleware)
* [Cookbook](/docs/category/cookbook)
* [Guide](/docs/category/guide)
* Static Files
On this page
Static Files
============
Images, JavaScript, CSS, PDF, Fonts and so on...
Using Static Middleware[​](#using-static-middleware "Direct link to Using Static Middleware")
---------------------------------------------------------------------------------------------
[See](/docs/middleware/static)
Using Echo#Static()[​](#using-echostatic "Direct link to Using Echo#Static()")
------------------------------------------------------------------------------
`Echo#Static(prefix, root string)` registers a new route with path prefix to serve
static files from the provided root directory.
*Usage 1*
```
e := echo.New()  
e.Static("/static", "assets")
```
Example above will serve any file from the assets directory for path `/static/*`. For example,
a request to `/static/js/main.js` will fetch and serve `assets/js/main.js` file.
*Usage 2*
```
e := echo.New()  
e.Static("/", "assets")
```
Example above will serve any file from the assets directory for path `/*`. For example,
a request to `/js/main.js` will fetch and serve `assets/js/main.js` file.
Using Echo#File()[​](#using-echofile "Direct link to Using Echo#File()")
------------------------------------------------------------------------
`Echo#File(path, file string)` registers a new route with path to serve a static
file.
*Usage 1*
Serving an index page from `public/index.html`
```
e.File("/", "public/index.html")
```
*Usage 2*
Serving a favicon from `images/favicon.ico`
```
e.File("/favicon.ico", "images/favicon.ico")
```