Error Handling

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
* Error Handling
On this page
Error Handling
==============
Echo advocates for centralized HTTP error handling by returning error from middleware
and handlers. Centralized error handler allows us to log errors to external services
from a unified location and send a customized HTTP response to the client.
You can return a standard `error` or `echo.*HTTPError`.
For example, when basic auth middleware finds invalid credentials it returns
401 - Unauthorized error, aborting the current HTTP request.
```
e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {  
  return func(c echo.Context) error {  
    // Extract the credentials from HTTP request header and perform a security  
    // check  
  
    // For invalid credentials  
    return echo.NewHTTPError(http.StatusUnauthorized, "Please provide valid credentials")  
  
    // For valid credentials call next  
    // return next(c)  
  }  
})
```
You can also use `echo.NewHTTPError()` without a message, in that case status text is used
as an error message. For example, "Unauthorized".
Default HTTP Error Handler[​](#default-http-error-handler "Direct link to Default HTTP Error Handler")
------------------------------------------------------------------------------------------------------
Echo provides a default HTTP error handler which sends error in a JSON format.
```
{  
  "message": "error connecting to redis"  
}
```
For a standard `error`, response is sent as `500 - Internal Server Error`; however,
if you are running in a debug mode, the original error message is sent. If error
is `*HTTPError`, response is sent with the provided status code and message.
If logging is on, the error message is also logged.
Custom HTTP Error Handler[​](#custom-http-error-handler "Direct link to Custom HTTP Error Handler")
---------------------------------------------------------------------------------------------------
Custom HTTP error handler can be set via `e.HTTPErrorHandler`
For most cases default error HTTP handler should be sufficient; however, a custom HTTP
error handler can come handy if you want to capture different type of errors and
take action accordingly e.g. send notification email or log error to a centralized
system. You can also send customized response to the client e.g. error page or
just a JSON response.
### Error Pages[​](#error-pages "Direct link to Error Pages")
The following custom HTTP error handler shows how to display error pages for different
type of errors and logs the error. The name of the error page should be like `<CODE>.html` e.g. `500.html`. You can look into this project
<https://github.com/AndiDittrich/HttpErrorPages> for pre-built error pages.
```
func customHTTPErrorHandler(err error, c echo.Context) {  
 	if c.Response().Committed {   
 		return   
 	}  
  
	code := http.StatusInternalServerError  
	if he, ok := err.(*echo.HTTPError); ok {  
		code = he.Code  
	}  
	c.Logger().Error(err)  
	errorPage := fmt.Sprintf("%d.html", code)  
	if err := c.File(errorPage); err != nil {  
		c.Logger().Error(err)  
	}  
}  
  
e.HTTPErrorHandler = customHTTPErrorHandler
```
tip
Instead of writing logs to the logger, you can also write them to an external service like Elasticsearch or Splunk.