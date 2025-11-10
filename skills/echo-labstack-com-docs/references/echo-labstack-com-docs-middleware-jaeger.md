Jaeger

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
* Jaeger
On this page
Jaeger
======
note
Echo community contribution
Trace requests on Echo framework with Jaeger Tracing Middleware.
Usage[​](#usage "Direct link to Usage")
---------------------------------------
```
package main  
import (  
    "github.com/labstack/echo-contrib/jaegertracing"  
    "github.com/labstack/echo/v4"  
)  
func main() {  
    e := echo.New()  
    // Enable tracing middleware  
    c := jaegertracing.New(e, nil)  
    defer c.Close()  
  
    e.Logger.Fatal(e.Start(":1323"))  
}
```
Enabling the tracing middleware creates a tracer and a root tracing span for every request.
Custom Configuration[​](#custom-configuration "Direct link to Custom Configuration")
------------------------------------------------------------------------------------
By default, traces are sent to `localhost` Jaeger agent instance. To configure an external Jaeger, start your application with environment variables.
### Usage[​](#usage-1 "Direct link to Usage")
```
$ JAEGER_AGENT_HOST=192.168.1.10 JAEGER_AGENT_PORT=6831 ./myserver
```
The tracer can be initialized with values coming from environment variables. None of the env vars are required
and all of them can be overridden via direct setting of the property on the configuration object.
| Property | Description |
| --- | --- |
| JAEGER\_SERVICE\_NAME | The service name |
| JAEGER\_AGENT\_HOST | The hostname for communicating with agent via UDP |
| JAEGER\_AGENT\_PORT | The port for communicating with agent via UDP |
| JAEGER\_ENDPOINT | The HTTP endpoint for sending spans directly to a collector, i.e. <http://jaeger-collector:14268/api/traces> |
| JAEGER\_USER | Username to send as part of "Basic" authentication to the collector endpoint |
| JAEGER\_PASSWORD | Password to send as part of "Basic" authentication to the collector endpoint |
| JAEGER\_REPORTER\_LOG\_SPANS | Whether the reporter should also log the spans |
| JAEGER\_REPORTER\_MAX\_QUEUE\_SIZE | The reporter's maximum queue size |
| JAEGER\_REPORTER\_FLUSH\_INTERVAL | The reporter's flush interval, with units, e.g. "500ms" or "2s" ([valid units][timeunits]) |
| JAEGER\_SAMPLER\_TYPE | The sampler type |
| JAEGER\_SAMPLER\_PARAM | The sampler parameter (number) |
| JAEGER\_SAMPLER\_MANAGER\_HOST\_PORT | The HTTP endpoint when using the remote sampler, i.e. <http://jaeger-agent:5778/sampling> |
| JAEGER\_SAMPLER\_MAX\_OPERATIONS | The maximum number of operations that the sampler will keep track of |
| JAEGER\_SAMPLER\_REFRESH\_INTERVAL | How often the remotely controlled sampler will poll jaeger-agent for the appropriate sampling strategy, with units, e.g. "1m" or "30s" ([valid units][timeunits]) |
| JAEGER\_TAGS | A comma separated list of `name = value` tracer level tags, which get added to all reported spans. The value can also refer to an environment variable using the format `${envVarName:default}`, where the `:default` is optional, and identifies a value to be used if the environment variable cannot be found |
| JAEGER\_DISABLED | Whether the tracer is disabled or not. If true, the default `opentracing.NoopTracer` is used. |
| JAEGER\_RPC\_METRICS | Whether to store RPC metrics |
By default, the client sends traces via UDP to the agent at `localhost:6831`. Use `JAEGER_AGENT_HOST` and
`JAEGER_AGENT_PORT` to send UDP traces to a different `host:port`. If `JAEGER_ENDPOINT` is set, the client sends traces
to the endpoint via `HTTP`, making the `JAEGER_AGENT_HOST` and `JAEGER_AGENT_PORT` unused. If `JAEGER_ENDPOINT` is
secured, HTTP basic authentication can be performed by setting the `JAEGER_USER` and `JAEGER_PASSWORD` environment
variables.
### Skipping URL(s)[​](#skipping-urls "Direct link to Skipping URL(s)")
A middleware skipper can be passed to avoid tracing spans to certain URL(s).
*Usage*
```
package main  
import (  
	"strings"  
    "github.com/labstack/echo-contrib/jaegertracing"  
    "github.com/labstack/echo/v4"  
)  
  
// urlSkipper ignores metrics route on some middleware  
func urlSkipper(c echo.Context) bool {  
    if strings.HasPrefix(c.Path(), "/testurl") {  
        return true  
    }  
    return false  
}  
  
func main() {  
    e := echo.New()  
    // Enable tracing middleware  
    c := jaegertracing.New(e, urlSkipper)  
    defer c.Close()  
  
    e.Logger.Fatal(e.Start(":1323"))  
}
```
### TraceFunction[​](#tracefunction "Direct link to TraceFunction")
This is a wrapper function that can be used to seamlessly add a span for
the duration of the invoked function. There is no need to change function arguments.
*Usage*
```
package main  
import (  
    "github.com/labstack/echo-contrib/jaegertracing"  
    "github.com/labstack/echo/v4"  
    "net/http"  
    "time"  
)  
func main() {  
    e := echo.New()  
    // Enable tracing middleware  
    c := jaegertracing.New(e, nil)  
    defer c.Close()  
    e.GET("/", func(c echo.Context) error {  
        // Wrap slowFunc on a new span to trace it's execution passing the function arguments  
		jaegertracing.TraceFunction(c, slowFunc, "Test String")  
        return c.String(http.StatusOK, "Hello, World!")  
    })  
    e.Logger.Fatal(e.Start(":1323"))  
}  
  
// A function to be wrapped. No need to change it's arguments due to tracing  
func slowFunc(s string) {  
	time.Sleep(200 * time.Millisecond)  
	return  
}
```
### CreateChildSpan[​](#createchildspan "Direct link to CreateChildSpan")
For more control over the Span, the function `CreateChildSpan` can be called
giving control on data to be appended to the span like log messages, baggages and tags.
*Usage*
```
package main  
import (  
    "github.com/labstack/echo-contrib/jaegertracing"  
    "github.com/labstack/echo/v4"  
)  
func main() {  
    e := echo.New()  
    // Enable tracing middleware  
    c := jaegertracing.New(e, nil)  
    defer c.Close()  
    e.GET("/", func(c echo.Context) error {  
        // Do something before creating the child span  
        time.Sleep(40 * time.Millisecond)  
        sp := jaegertracing.CreateChildSpan(c, "Child span for additional processing")  
        defer sp.Finish()  
        sp.LogEvent("Test log")  
        sp.SetBaggageItem("Test baggage", "baggage")  
        sp.SetTag("Test tag", "New Tag")  
        time.Sleep(100 * time.Millisecond)  
        return c.String(http.StatusOK, "Hello, World!")  
    })  
    e.Logger.Fatal(e.Start(":1323"))  
}
```
References[​](#references "Direct link to References")
------------------------------------------------------
* [Opentracing Library](https://github.com/opentracing/opentracing-go)
* [Jaeger configuration](https://github.com/jaegertracing/jaeger-client-go#environment-variables)