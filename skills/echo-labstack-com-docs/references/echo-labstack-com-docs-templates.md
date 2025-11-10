Templates

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
* Templates
On this page
Templates
=========
Rendering[​](#rendering "Direct link to Rendering")
---------------------------------------------------
`Context#Render(code int, name string, data interface{}) error` renders a template
with data and sends a text/html response with status code. Templates can be registered by setting `Echo.Renderer`, allowing us to use any template engine.
Example below shows how to use Go `html/template`:
1. Implement `echo.Renderer` interface
   ```
   type Template struct {  
       templates *template.Template  
   }  
     
   func (t *Template) Render(w io.Writer, name string, data interface{}, c echo.Context) error {  
   	return t.templates.ExecuteTemplate(w, name, data)  
   }
   ```
2. Pre-compile templates
   `public/views/hello.html`
   ```
   {{define "hello"}}Hello, {{.}}!{{end}}
   ```
   ```
   t := &Template{  
       templates: template.Must(template.ParseGlob("public/views/*.html")),  
   }
   ```
3. Register templates
   ```
   e := echo.New()  
   e.Renderer = t  
   e.GET("/hello", Hello)
   ```
4. Render a template inside your handler
   ```
   func Hello(c echo.Context) error {  
   	return c.Render(http.StatusOK, "hello", "World")  
   }
   ```
Advanced - Calling Echo from templates[​](#advanced---calling-echo-from-templates "Direct link to Advanced - Calling Echo from templates")
------------------------------------------------------------------------------------------------------------------------------------------
In certain situations it might be useful to generate URIs from the templates. In order to do so, you need to call `Echo#Reverse` from the templates itself. Golang's `html/template` package is not the best suited for this job, but this can be done in two ways: by providing a common method on all objects passed to templates or by passing `map[string]interface{}` and augmenting this object in the custom renderer. Given the flexibility of the latter approach, here is a sample program:
`template.html`
```
<html>  
    <body>  
        <h1>Hello {{index . "name"}}</h1>  
  
        <p>{{ with $x := index . "reverse" }}  
           {{ call $x "foobar" }} &lt;-- this will call the $x with parameter "foobar"  
           {{ end }}  
        </p>  
    </body>  
</html>
```
`server.go`
```
package main  
  
import (  
	"html/template"  
	"io"  
	"net/http"  
  
	"github.com/labstack/echo/v4"  
)  
  
// TemplateRenderer is a custom html/template renderer for Echo framework  
type TemplateRenderer struct {  
	templates *template.Template  
}  
  
// Render renders a template document  
func (t *TemplateRenderer) Render(w io.Writer, name string, data interface{}, c echo.Context) error {  
  
	// Add global methods if data is a map  
	if viewContext, isMap := data.(map[string]interface{}); isMap {  
		viewContext["reverse"] = c.Echo().Reverse  
	}  
  
	return t.templates.ExecuteTemplate(w, name, data)  
}  
  
func main() {  
  e := echo.New()  
  renderer := &TemplateRenderer{  
      templates: template.Must(template.ParseGlob("*.html")),  
  }  
  e.Renderer = renderer  
  
  // Named route "foobar"  
  e.GET("/something", func(c echo.Context) error {  
      return c.Render(http.StatusOK, "template.html", map[string]interface{}{  
          "name": "Dolly!",  
      })  
  }).Name = "foobar"  
  
  e.Logger.Fatal(e.Start(":8000"))  
}
```