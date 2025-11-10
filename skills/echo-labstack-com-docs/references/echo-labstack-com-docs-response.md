Response

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
* Response
On this page
Response
========
Send String[​](#send-string "Direct link to Send String")
---------------------------------------------------------
`Context#String(code int, s string)` can be used to send plain text response with status
code.
*Example*
```
func(c echo.Context) error {  
  return c.String(http.StatusOK, "Hello, World!")  
}
```
Send HTML (Reference to templates)[​](#send-html-reference-to-templates "Direct link to Send HTML (Reference to templates)")
----------------------------------------------------------------------------------------------------------------------------
`Context#HTML(code int, html string)` can be used to send simple HTML response with
status code. If you are looking to send dynamically generate HTML see [templates](/docs/templates).
*Example*
```
func(c echo.Context) error {  
  return c.HTML(http.StatusOK, "<strong>Hello, World!</strong>")  
}
```
### Send HTML Blob[​](#send-html-blob "Direct link to Send HTML Blob")
`Context#HTMLBlob(code int, b []byte)` can be used to send HTML blob with status
code. You may find it handy using with a template engine which outputs `[]byte`.
Render Template[​](#render-template "Direct link to Render Template")
---------------------------------------------------------------------
[Learn more](/docs/templates)
Send JSON[​](#send-json "Direct link to Send JSON")
---------------------------------------------------
`Context#JSON(code int, i interface{})` can be used to encode a provided Go type into
JSON and send it as response with status code.
*Example*
```
// User  
type User struct {  
  Name  string `json:"name" xml:"name"`  
  Email string `json:"email" xml:"email"`  
}  
  
// Handler  
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "jon@labstack.com",  
  }  
  return c.JSON(http.StatusOK, u)  
}
```
### Stream JSON[​](#stream-json "Direct link to Stream JSON")
`Context#JSON()` internally uses `json.Marshal` which may not be efficient to large JSON,
in that case you can directly stream JSON.
*Example*
```
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "jon@labstack.com",  
  }  
  c.Response().Header().Set(echo.HeaderContentType, echo.MIMEApplicationJSONCharsetUTF8)  
  c.Response().WriteHeader(http.StatusOK)  
  return json.NewEncoder(c.Response()).Encode(u)  
}
```
### JSON Pretty[​](#json-pretty "Direct link to JSON Pretty")
`Context#JSONPretty(code int, i interface{}, indent string)` can be used to a send
a JSON response which is pretty printed based on indent, which could be spaces or tabs.
Example below sends a pretty print JSON indented with spaces:
```
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "joe@labstack.com",  
  }  
  return c.JSONPretty(http.StatusOK, u, "  ")  
}
```
```
{  
  "email": "joe@labstack.com",  
  "name": "Jon"  
}
```
tip
You can also use `Context#JSON()` to output a pretty printed JSON (indented with spaces)
by appending `pretty` in the request URL query string.
*Example*
```
curl http://localhost:1323/users/1?pretty
```
### JSON Blob[​](#json-blob "Direct link to JSON Blob")
`Context#JSONBlob(code int, b []byte)` can be used to send pre-encoded JSON blob directly
from external source, for example, database.
*Example*
```
func(c echo.Context) error {  
  encodedJSON := []byte{} // Encoded JSON from external source  
  return c.JSONBlob(http.StatusOK, encodedJSON)  
}
```
Send JSONP[​](#send-jsonp "Direct link to Send JSONP")
------------------------------------------------------
`Context#JSONP(code int, callback string, i interface{})` can be used to encode a provided
Go type into JSON and send it as JSONP payload constructed using a callback, with
status code.
[*Example*](/docs/cookbook/jsonp)
Send XML[​](#send-xml "Direct link to Send XML")
------------------------------------------------
`Context#XML(code int, i interface{})` can be used to encode a provided Go type into
XML and send it as response with status code.
*Example*
```
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "jon@labstack.com",  
  }  
  return c.XML(http.StatusOK, u)  
}
```
### Stream XML[​](#stream-xml "Direct link to Stream XML")
`Context#XML` internally uses `xml.Marshal` which may not be efficient to large XML,
in that case you can directly stream XML.
*Example*
```
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "jon@labstack.com",  
  }  
  c.Response().Header().Set(echo.HeaderContentType, echo.MIMEApplicationXMLCharsetUTF8)  
  c.Response().WriteHeader(http.StatusOK)  
  return xml.NewEncoder(c.Response()).Encode(u)  
}
```
### XML Pretty[​](#xml-pretty "Direct link to XML Pretty")
`Context#XMLPretty(code int, i interface{}, indent string)` can be used to a send
an XML response which is pretty printed based on indent, which could be spaces or tabs.
Example below sends a pretty print XML indented with spaces:
```
func(c echo.Context) error {  
  u := &User{  
    Name:  "Jon",  
    Email: "joe@labstack.com",  
  }  
  return c.XMLPretty(http.StatusOK, u, "  ")  
}
```
```
<?xml version="1.0" encoding="UTF-8"?>  
<User>  
  <Name>Jon</Name>  
  <Email>joe@labstack.com</Email>  
</User>
```
tip
You can also use `Context#XML()` to output a pretty printed XML (indented with spaces) by appending `pretty` in the request URL query string.
*Example*
```
curl http://localhost:1323/users/1?pretty
```
### XML Blob[​](#xml-blob "Direct link to XML Blob")
`Context#XMLBlob(code int, b []byte)` can be used to send pre-encoded XML blob directly
from external source, for example, database.
*Example*
```
func(c echo.Context) error {  
  encodedXML := []byte{} // Encoded XML from external source  
  return c.XMLBlob(http.StatusOK, encodedXML)  
}
```
Send File[​](#send-file "Direct link to Send File")
---------------------------------------------------
`Context#File(file string)` can be used to send the content of file as response.
It automatically sets the correct content type and handles caching gracefully.
*Example*
```
func(c echo.Context) error {  
  return c.File("<PATH_TO_YOUR_FILE>")  
}
```
Send Attachment[​](#send-attachment "Direct link to Send Attachment")
---------------------------------------------------------------------
`Context#Attachment(file, name string)` is similar to `File()` except that it is
used to send file as `Content-Disposition: attachment` with provided name.
*Example*
```
func(c echo.Context) error {  
  return c.Attachment("<PATH_TO_YOUR_FILE>", "<ATTACHMENT_NAME>")  
}
```
Send Inline[​](#send-inline "Direct link to Send Inline")
---------------------------------------------------------
`Context#Inline(file, name string)` is similar to `File()` except that it is
used to send file as `Content-Disposition: inline` with provided name.
*Example*
```
func(c echo.Context) error {  
  return c.Inline("<PATH_TO_YOUR_FILE>")  
}
```
Send Blob[​](#send-blob "Direct link to Send Blob")
---------------------------------------------------
`Context#Blob(code int, contentType string, b []byte)` can be used to send an arbitrary
data response with provided content type and status code.
*Example*
```
func(c echo.Context) (err error) {  
  data := []byte(`0306703,0035866,NO_ACTION,06/19/2006  
	  0086003,"0005866",UPDATED,06/19/2006`)  
	return c.Blob(http.StatusOK, "text/csv", data)  
}
```
Send Stream[​](#send-stream "Direct link to Send Stream")
---------------------------------------------------------
`Context#Stream(code int, contentType string, r io.Reader)` can be used to send an
arbitrary data stream response with provided content type, `io.Reader` and status
code.
*Example*
```
func(c echo.Context) error {  
  f, err := os.Open("<PATH_TO_IMAGE>")  
  if err != nil {  
    return err  
  }  
  defer f.Close()  
  return c.Stream(http.StatusOK, "image/png", f)  
}
```
Send No Content[​](#send-no-content "Direct link to Send No Content")
---------------------------------------------------------------------
`Context#NoContent(code int)` can be used to send empty body with status code.
*Example*
```
func(c echo.Context) error {  
  return c.NoContent(http.StatusOK)  
}
```
Redirect Request[​](#redirect-request "Direct link to Redirect Request")
------------------------------------------------------------------------
`Context#Redirect(code int, url string)` can be used to redirect the request to
a provided URL with status code.
*Example*
```
func(c echo.Context) error {  
  return c.Redirect(http.StatusMovedPermanently, "<URL>")  
}
```
Hooks[​](#hooks "Direct link to Hooks")
---------------------------------------
### Before Response[​](#before-response "Direct link to Before Response")
`Context#Response#Before(func())` can be used to register a function which is called just before the response is written.
### After Response[​](#after-response "Direct link to After Response")
`Context#Response#After(func())` can be used to register a function which is called just
after the response is written. If the "Content-Length" is unknown, none of the after
function is executed.
*Example*
```
func(c echo.Context) error {  
  c.Response().Before(func() {  
    println("before response")  
  })  
  c.Response().After(func() {  
    println("after response")  
  })  
  return c.NoContent(http.StatusNoContent)  
}
```
tip
It is possible to register multiple Before and After functions.