---
name: echo-labstack-com-docs
description: This skill should be used when developing Go web applications with the Echo framework, including tasks such as setting up routes, implementing middleware, handling requests/responses, configuring servers, managing authentication, implementing CORS, working with WebSockets, or troubleshooting Echo-specific issues.
---

# Echo Framework Documentation

This skill provides comprehensive guidance for building web applications using the Echo framework in Go, covering routing, middleware, request/response handling, authentication, and deployment patterns.

## Getting Started

For initial setup and basic usage patterns, consult `references/echo-labstack-com-docs.md` for framework overview and `references/echo-labstack-com-docs-quick-start.md` for immediate implementation steps.

## Core Framework Concepts

### Routing and Request Handling

When implementing routes and handlers:

- Review `references/echo-labstack-com-docs-routing.md` for route definition patterns, path parameters, wildcards, and route groups
- Consult `references/echo-labstack-com-docs-request.md` for extracting path parameters, query strings, form data, and request validation
- Reference `references/echo-labstack-com-docs-response.md` for sending JSON, XML, HTML, files, streams, and custom responses
- Check `references/echo-labstack-com-docs-context.md` for context operations and lifecycle management

### Server Configuration

When configuring server startup and behavior:

- Use `references/echo-labstack-com-docs-start-server.md` for standard HTTP/HTTPS server startup patterns
- Reference `references/echo-labstack-com-docs-customization.md` for timeouts, error handlers, validators, and custom configuration
- Consult `references/echo-labstack-com-docs-ip-address.md` for reliable client IP extraction and security considerations

### Data Binding and Validation

When binding request data to structs:

- Review `references/echo-labstack-com-docs-binding.md` for binding JSON, XML, form data, query parameters, and custom binders
- Implement struct tags for data source specification and validation rules

### Error Handling

When implementing error handling:

- Consult `references/echo-labstack-com-docs-error-handling.md` for HTTP error handling patterns and custom error handlers
- Implement centralized error handling for consistent responses

### Static Resources and Templates

When serving static files or rendering templates:

- Use `references/echo-labstack-com-docs-static-files.md` for serving static assets
- Reference `references/echo-labstack-com-docs-templates.md` for HTML template rendering with custom renderers

### Cookies and Sessions

When managing cookies or sessions:

- Consult `references/echo-labstack-com-docs-cookies.md` for cookie operations and security attributes

### Testing

When writing tests for Echo applications:

- Review `references/echo-labstack-com-docs-testing.md` for testing handlers and middleware with httptest

## Middleware Implementation

### Authentication and Authorization

When implementing authentication:

- Use `references/echo-labstack-com-docs-middleware-basic-auth.md` for HTTP Basic Authentication
- Reference `references/echo-labstack-com-docs-middleware-jwt.md` for JWT token validation and configuration
- Consult `references/echo-labstack-com-docs-middleware-key-auth.md` for API key authentication
- Check `references/echo-labstack-com-docs-middleware-casbin-auth.md` for role-based access control

**Search patterns for JWT middleware**: Use `grep -i "jwt\|token\|claims\|signing"` to find JWT-specific configuration options.

### Cross-Origin Resource Sharing (CORS)

When configuring CORS:

- Review `references/echo-labstack-com-docs-middleware-cors.md` for allowed origins, methods, headers, and credentials handling

### Security Middleware

When implementing security features:

- Use `references/echo-labstack-com-docs-middleware-csrf.md` for CSRF protection with token validation
- Reference `references/echo-labstack-com-docs-middleware-secure.md` for security headers (XSS, content type sniffing, frame options)

### Request/Response Processing

When processing requests and responses:

- Use `references/echo-labstack-com-docs-middleware-logger.md` for request logging with custom formats and output
- Reference `references/echo-labstack-com-docs-middleware-body-dump.md` for capturing request/response bodies
- Consult `references/echo-labstack-com-docs-middleware-body-limit.md` for limiting request body size
- Check `references/echo-labstack-com-docs-middleware-decompress.md` for decompressing request bodies
- Review `references/echo-labstack-com-docs-middleware-gzip.md` for compressing responses

**Search patterns for logger middleware**: Use `grep -i "logvalues\|format\|output\|custom"` to find logging configuration details.

### Request Modification

When modifying requests:

- Use `references/echo-labstack-com-docs-middleware-method-override.md` for HTTP method override via headers
- Reference `references/echo-labstack-com-docs-middleware-rewrite.md` for URL rewriting rules
- Consult `references/echo-labstack-com-docs-middleware-redirect.md` for HTTP to HTTPS redirects
- Check `references/echo-labstack-com-docs-middleware-trailing-slash.md` for normalizing URL trailing slashes

### Rate Limiting and Timeouts

When implementing rate limiting or timeouts:

- Use `references/echo-labstack-com-docs-middleware-rate-limiter.md` for request rate limiting with stores
- Reference `references/echo-labstack-com-docs-middleware-context-timeout.md` for per-request timeout enforcement

### Error Recovery and Monitoring

When implementing resilience and monitoring:

- Use `references/echo-labstack-com-docs-middleware-recover.md` for panic recovery
- Reference `references/echo-labstack-com-docs-middleware-prometheus.md` for Prometheus metrics collection
- Consult `references/echo-labstack-com-docs-middleware-jaeger.md` for distributed tracing

**Search patterns for Prometheus middleware**: Use `grep -i "metrics\|histogram\|counter\|namespace"` to find metrics configuration.

### Proxy and Load Balancing

When implementing proxies or load balancing:

- Use `references/echo-labstack-com-docs-middleware-proxy.md` for reverse proxy and load balancing configuration

### Request Tracking

When tracking requests:

- Use `references/echo-labstack-com-docs-middleware-request-id.md` for generating and propagating request IDs

### Session Management

When managing sessions:

- Use `references/echo-labstack-com-docs-middleware-session.md` for session stores and cookie-based sessions

### Static File Serving

When serving static files via middleware:

- Use `references/echo-labstack-com-docs-middleware-static.md` for static file middleware with directory browsing options

### Middleware Overview

For middleware categories and organization:

- Review `references/echo-labstack-com-docs-category-middleware.md` for middleware classification and overview

## Cookbook Recipes

### HTTPS and TLS

When configuring HTTPS:

- Use `references/echo-labstack-com-docs-cookbook-auto-tls.md` for automatic Let's Encrypt certificates
- Reference `references/echo-labstack-com-docs-cookbook-http2.md` for HTTP/2 server configuration
- Consult `references/echo-labstack-com-docs-cookbook-http2-server-push.md` for server push implementation

### CRUD Operations

When implementing CRUD APIs:

- Use `references/echo-labstack-com-docs-cookbook-crud.md` for RESTful CRUD patterns with in-memory storage

### CORS Configuration

When configuring CORS in practice:

- Use `references/echo-labstack-com-docs-cookbook-cors.md` for CORS recipe examples with wildcards and allowed origins

### File Operations

When handling file uploads or downloads:

- Use `references/echo-labstack-com-docs-cookbook-file-upload.md` for single and multiple file upload handling
- Reference `references/echo-labstack-com-docs-cookbook-file-download.md` for serving file downloads with inline/attachment options
- Consult `references/echo-labstack-com-docs-cookbook-embed-resources.md` for embedding static resources in binaries

### Real-time Communication

When implementing real-time features:

- Use `references/echo-labstack-com-docs-cookbook-websocket.md` for WebSocket implementation patterns
- Reference `references/echo-labstack-com-docs-cookbook-sse.md` for Server-Sent Events streaming
- Consult `references/echo-labstack-com-docs-cookbook-streaming-response.md` for streaming JSON responses

### API Patterns

When implementing specific API patterns:

- Use `references/echo-labstack-com-docs-cookbook-jsonp.md` for JSONP responses
- Reference `references/echo-labstack-com-docs-cookbook-jwt.md` for JWT authentication recipes

### Infrastructure

When deploying or configuring infrastructure:

- Use `references/echo-labstack-com-docs-cookbook-google-app-engine.md` for Google App Engine deployment
- Reference `references/echo-labstack-com-docs-cookbook-graceful-shutdown.md` for graceful server shutdown patterns
- Consult `references/echo-labstack-com-docs-cookbook-timeout.md` for request timeout implementation
- Check `references/echo-labstack-com-docs-cookbook-subdomain.md` for subdomain routing

**Search patterns for Google App Engine**: Use `grep -i "app.yaml\|standard\|flexible\|dispatch"` to find deployment configuration details.

### Proxy and Load Balancing Recipes

When implementing proxies:

- Use `references/echo-labstack-com-docs-cookbook-reverse-proxy.md` for reverse proxy implementation
- Reference `references/echo-labstack-com-docs-cookbook-load-balancing.md` for load balancing strategies

### Custom Middleware

When creating custom middleware:

- Use `references/echo-labstack-com-docs-cookbook-middleware.md` for middleware creation patterns

### Example Applications

When building complete applications:

- Use `references/echo-labstack-com-docs-cookbook-hello-world.md` for minimal examples
- Reference `references/echo-labstack-com-docs-cookbook-twitter.md` for a complete Twitter-like API with authentication

**Search patterns for Twitter cookbook**: Use `grep -i "user\|post\|follow\|jwt\|mongo"` to find specific API endpoint implementations.

### Cookbook Overview

For cookbook organization:

- Review `references/echo-labstack-com-docs-category-cookbook.md` for recipe classification and overview

## Guide Overview

For comprehensive guide structure:

- Review `references/echo-labstack-com-docs-category-guide.md` for guide topics and organization

## Common Workflows

### Creating a New Echo Application

1. Review `references/echo-labstack-com-docs-quick-start.md` for initialization
2. Consult `references/echo-labstack-com-docs-routing.md` for route setup
3. Reference `references/echo-labstack-com-docs-middleware-logger.md` and `references/echo-labstack-com-docs-middleware-recover.md` for essential middleware
4. Use `references/echo-labstack-com-docs-start-server.md` for server startup

### Implementing API Authentication

1. Choose authentication method from JWT, Basic Auth, or Key Auth references
2. Review `references/echo-labstack-com-docs-middleware-jwt.md` for token-based auth
3. Consult `references/echo-labstack-com-docs-cookbook-jwt.md` for implementation examples
4. Reference `references/echo-labstack-com-docs-middleware-cors.md` if serving cross-origin requests

### Building RESTful APIs

1. Start with `references/echo-labstack-com-docs-cookbook-crud.md` for patterns
2. Use `references/echo-labstack-com-docs-routing.md` for route groups and parameters
3. Reference `references/echo-labstack-com-docs-binding.md` for request data binding
4. Consult `references/echo-labstack-com-docs-response.md` for JSON responses
5. Review `references/echo-labstack-com-docs-error-handling.md` for error responses

### Deploying Production Applications

1. Review `references/echo-labstack-com-docs-customization.md` for production settings (timeouts, limits)
2. Consult `references/echo-labstack-com-docs-cookbook-graceful-shutdown.md` for shutdown handling
3. Reference `references/echo-labstack-com-docs-cookbook-auto-tls.md` for HTTPS configuration
4. Use `references/echo-labstack-com-docs-middleware-prometheus.md` for monitoring
5. Check `references/echo-labstack-com-docs-middleware-rate-limiter.md` for rate limiting

### Implementing Real-time Features

1. Choose between WebSocket (`references/echo-labstack-com-docs-cookbook-websocket.md`) or SSE (`references/echo-labstack-com-docs-cookbook-sse.md`)
2. Review connection upgrade patterns and message handling
3. Implement authentication if needed using JWT middleware

## Reference File Organization

All documentation files are organized in the `references/` directory:

- **Core concepts**: Introduction, quick start, routing, context, request, response
- **Middleware**: 25+ middleware implementations for authentication, security, logging, compression, and more
- **Cookbook**: 19 practical recipes for common implementation patterns
- **Category files**: High-level overviews of guide sections, middleware, and cookbook

When a topic requires deep configuration or has multiple options, load the corresponding reference file into context. For large files (>1500 lines), use grep patterns provided above to locate specific sections efficiently.