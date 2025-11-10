JWT

* [Introduction](/docs)
* [Guide](/docs/category/guide)
* [Middleware](/docs/category/middleware)
* [Cookbook](/docs/category/cookbook)
  + [Auto TLS](/docs/cookbook/auto-tls)
  + [CORS](/docs/cookbook/cors)
  + [CRUD](/docs/cookbook/crud)
  + [Embed Resources](/docs/cookbook/embed-resources)
  + [File Download](/docs/cookbook/file-download)
  + [File Upload](/docs/cookbook/file-upload)
  + [Google App Engine](/docs/cookbook/google-app-engine)
  + [Graceful Shutdown](/docs/cookbook/graceful-shutdown)
  + [Hello World](/docs/cookbook/hello-world)
  + [HTTP/2 Server Push](/docs/cookbook/http2-server-push)
  + [HTTP/2 Server](/docs/cookbook/http2)
  + [JSONP](/docs/cookbook/jsonp)
  + [JWT](/docs/cookbook/jwt)
  + [Load Balancing](/docs/cookbook/load-balancing)
  + [Middleware](/docs/cookbook/middleware)
  + [Reverse Proxy](/docs/cookbook/reverse-proxy)
  + [Server-Sent-Events (SSE)](/docs/cookbook/sse)
  + [Streaming Response](/docs/cookbook/streaming-response)
  + [Subdomain](/docs/cookbook/subdomain)
  + [Timeout](/docs/cookbook/timeout)
  + [Twitter Like API](/docs/cookbook/twitter)
  + [WebSocket](/docs/cookbook/websocket)
* [Cookbook](/docs/category/cookbook)
* JWT
On this page
JWT
===
[JWT middleware](/docs/middleware/jwt) configuration can be found [here](/docs/middleware/jwt#configuration).
This is cookbook for:
* JWT authentication using HS256 algorithm.
* JWT is retrieved from `Authorization` request header.
Server[​](#server "Direct link to Server")
------------------------------------------
### Using custom claims[​](#using-custom-claims "Direct link to Using custom claims")
cookbook/jwt/custom-claims/server.go
```
package main  
  
import (  
	"github.com/golang-jwt/jwt/v5"  
	echojwt "github.com/labstack/echo-jwt/v4"  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"net/http"  
	"time"  
)  
  
// jwtCustomClaims are custom claims extending default ones.  
// See https://github.com/golang-jwt/jwt for more examples  
type jwtCustomClaims struct {  
	Name  string `json:"name"`  
	Admin bool   `json:"admin"`  
	jwt.RegisteredClaims  
}  
  
func login(c echo.Context) error {  
	username := c.FormValue("username")  
	password := c.FormValue("password")  
  
	// Throws unauthorized error  
	if username != "jon" || password != "shhh!" {  
		return echo.ErrUnauthorized  
	}  
  
	// Set custom claims  
	claims := &jwtCustomClaims{  
		"Jon Snow",  
		true,  
		jwt.RegisteredClaims{  
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(time.Hour * 72)),  
		},  
	}  
  
	// Create token with claims  
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)  
  
	// Generate encoded token and send it as response.  
	t, err := token.SignedString([]byte("secret"))  
	if err != nil {  
		return err  
	}  
  
	return c.JSON(http.StatusOK, echo.Map{  
		"token": t,  
	})  
}  
  
func accessible(c echo.Context) error {  
	return c.String(http.StatusOK, "Accessible")  
}  
  
func restricted(c echo.Context) error {  
	user := c.Get("user").(*jwt.Token)  
	claims := user.Claims.(*jwtCustomClaims)  
	name := claims.Name  
	return c.String(http.StatusOK, "Welcome "+name+"!")  
}  
  
func main() {  
	e := echo.New()  
  
	// Middleware  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// Login route  
	e.POST("/login", login)  
  
	// Unauthenticated route  
	e.GET("/", accessible)  
  
	// Restricted group  
	r := e.Group("/restricted")  
  
	// Configure middleware with the custom claims type  
	config := echojwt.Config{  
		NewClaimsFunc: func(c echo.Context) jwt.Claims {  
			return new(jwtCustomClaims)  
		},  
		SigningKey: []byte("secret"),  
	}  
	r.Use(echojwt.WithConfig(config))  
	r.GET("", restricted)  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
### Using a user-defined KeyFunc[​](#using-a-user-defined-keyfunc "Direct link to Using a user-defined KeyFunc")
cookbook/jwt/user-defined-keyfunc/server.go
```
package main  
  
import (  
	"context"  
	"errors"  
	"fmt"  
	echojwt "github.com/labstack/echo-jwt/v4"  
	"net/http"  
  
	"github.com/golang-jwt/jwt/v5"  
	"github.com/labstack/echo/v4"  
	"github.com/labstack/echo/v4/middleware"  
	"github.com/lestrrat-go/jwx/v3/jwk"  
)  
  
func getKey(token *jwt.Token) (interface{}, error) {  
  
	// For a demonstration purpose, Google Sign-in is used.  
	// https://developers.google.com/identity/sign-in/web/backend-auth  
	//  
	// This user-defined KeyFunc verifies tokens issued by Google Sign-In.  
	//  
	// Note: In this example, it downloads the keyset every time the restricted route is accessed.  
	keySet, err := jwk.Fetch(context.Background(), "https://www.googleapis.com/oauth2/v3/certs")  
	if err != nil {  
		return nil, err  
	}  
  
	keyID, ok := token.Header["kid"].(string)  
	if !ok {  
		return nil, errors.New("expecting JWT header to have a key ID in the kid field")  
	}  
  
	key, found := keySet.LookupKeyID(keyID)  
  
	if !found {  
		return nil, fmt.Errorf("unable to find key %q", keyID)  
	}  
  
	return key.PublicKey()  
}  
  
func accessible(c echo.Context) error {  
	return c.String(http.StatusOK, "Accessible")  
}  
  
func restricted(c echo.Context) error {  
	user := c.Get("user").(*jwt.Token)  
	claims := user.Claims.(jwt.MapClaims)  
	name := claims["name"].(string)  
	return c.String(http.StatusOK, "Welcome "+name+"!")  
}  
  
func main() {  
	e := echo.New()  
  
	// Middleware  
	e.Use(middleware.Logger())  
	e.Use(middleware.Recover())  
  
	// Unauthenticated route  
	e.GET("/", accessible)  
  
	// Restricted group  
	r := e.Group("/restricted")  
	{  
		config := echojwt.Config{  
			KeyFunc: getKey,  
		}  
		r.Use(echojwt.WithConfig(config))  
		r.GET("", restricted)  
	}  
  
	e.Logger.Fatal(e.Start(":1323"))  
}
```
Client[​](#client "Direct link to Client")
------------------------------------------
### Login[​](#login "Direct link to Login")
Login using username and password to retrieve a token.
```
curl -X POST -d 'username=jon' -d 'password=shhh!' localhost:1323/login
```
### Response[​](#response "Direct link to Response")
```
{  
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0NjE5NTcxMzZ9.RB3arc4-OyzASAaUhC2W3ReWaXAt_z2Fd3BN4aWTgEY"  
}
```
### Request[​](#request "Direct link to Request")
Request a restricted resource using the token in `Authorization` request header.
```
curl localhost:1323/restricted -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE0NjE5NTcxMzZ9.RB3arc4-OyzASAaUhC2W3ReWaXAt_z2Fd3BN4aWTgEY"
```
### Response[​](#response-1 "Direct link to Response")
```
Welcome Jon Snow!
```