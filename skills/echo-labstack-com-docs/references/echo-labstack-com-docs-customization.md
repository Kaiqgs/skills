Customization

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
* Customization
On this page
Customization
=============
Debug[​](#debug "Direct link to Debug")
---------------------------------------
`Echo#Debug` can be used to enable / disable debug mode. Debug mode sets the log level
to `DEBUG`.
Logging[​](#logging "Direct link to Logging")
---------------------------------------------
The default format for logging is JSON, which can be changed by modifying the header.
### Log Header[​](#log-header "Direct link to Log Header")
`Echo#Logger.SetHeader(string)` can be used to set the header for
the logger. Default value:
```
{"time":"${time_rfc3339_nano}","level":"${level}","prefix":"${prefix}","file":"${short_file}","line":"${line}"}
```
*Example*
```
import "github.com/labstack/gommon/log"  
  
/* ... */  
  
if l, ok := e.Logger.(*log.Logger); ok {  
  l.SetHeader("${time_rfc3339} ${level}")  
}
```
```
2018-05-08T20:30:06-07:00 INFO info
```
#### Available Tags[​](#available-tags "Direct link to Available Tags")
* `time_rfc3339`
* `time_rfc3339_nano`
* `level`
* `prefix`
* `long_file`
* `short_file`
* `line`
### Log Output[​](#log-output "Direct link to Log Output")
`Echo#Logger.SetOutput(io.Writer)` can be used to set the output destination for
the logger. Default value is `os.Stdout`
To completely disable logs use `Echo#Logger.SetOutput(io.Discard)` or `Echo#Logger.SetLevel(log.OFF)`
### Log Level[​](#log-level "Direct link to Log Level")
`Echo#Logger.SetLevel(log.Lvl)` can be used to set the log level for the logger.
Default value is `ERROR`. Possible values:
* `DEBUG`
* `INFO`
* `WARN`
* `ERROR`
* `OFF`
### Custom Logger[​](#custom-logger "Direct link to Custom Logger")
Logging is implemented using `echo.Logger` interface which allows you to register
a custom logger using `Echo#Logger`.
Startup Banner[​](#startup-banner "Direct link to Startup Banner")
------------------------------------------------------------------
`Echo#HideBanner` can be used to hide the startup banner.
Listener Port[​](#listener-port "Direct link to Listener Port")
---------------------------------------------------------------
`Echo#HidePort` can be used to hide the listener port message.
Custom Listener[​](#custom-listener "Direct link to Custom Listener")
---------------------------------------------------------------------
`Echo#*Listener` can be used to run a custom listener.
*Example*
```
l, err := net.Listen("tcp", ":1323")  
if err != nil {  
  e.Logger.Fatal(err)  
}  
e.Listener = l  
e.Logger.Fatal(e.Start(""))
```
Disable HTTP/2[​](#disable-http2 "Direct link to Disable HTTP/2")
-----------------------------------------------------------------
`Echo#DisableHTTP2` can be used to disable HTTP/2 protocol.
Read Timeout[​](#read-timeout "Direct link to Read Timeout")
------------------------------------------------------------
`Echo#*Server#ReadTimeout` can be used to set the maximum duration before timing out read
of the request.
Write Timeout[​](#write-timeout "Direct link to Write Timeout")
---------------------------------------------------------------
`Echo#*Server#WriteTimeout` can be used to set the maximum duration before timing out write
of the response.
Validator[​](#validator "Direct link to Validator")
---------------------------------------------------
`Echo#Validator` can be used to register a validator for performing data validation
on request payload.
[Learn more](/docs/request#validate-data)
Custom Binder[​](#custom-binder "Direct link to Custom Binder")
---------------------------------------------------------------
`Echo#Binder` can be used to register a custom binder for binding request payload.
[Learn more](/docs/binding#custom-binding)
Custom JSON Serializer[​](#custom-json-serializer "Direct link to Custom JSON Serializer")
------------------------------------------------------------------------------------------
`Echo#JSONSerializer` can be used to register a custom JSON serializer.
Have a look at `DefaultJSONSerializer` on [json.go](https://github.com/labstack/echo/blob/master/json.go).
Renderer[​](#renderer "Direct link to Renderer")
------------------------------------------------
`Echo#Renderer` can be used to register a renderer for template rendering.
[Learn more](/docs/templates)
HTTP Error Handler[​](#http-error-handler "Direct link to HTTP Error Handler")
------------------------------------------------------------------------------
`Echo#HTTPErrorHandler` can be used to register a custom http error handler.
[Learn more](/docs/error-handling)