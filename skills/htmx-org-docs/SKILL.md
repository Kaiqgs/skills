---
name: htmx-org-docs
description: This skill should be used when working with htmx, a library for accessing modern browser features directly from HTML. Use this skill when building web applications that need AJAX requests, CSS transitions, WebSockets, or server-sent events without writing JavaScript. Apply when implementing hypermedia-driven applications, enhancing HTML forms and links, or converting traditional JavaScript interactions into declarative HTML attributes.
---

# htmx Documentation

This skill provides comprehensive guidance for working with htmx, a dependency-free JavaScript library that enables modern browser features through HTML attributes rather than JavaScript code.

## Overview

htmx extends HTML to support AJAX requests, CSS transitions, WebSockets, and SSE directly through declarative attributes. The library follows the principle of Hypertext As The Engine Of Application State (HATEOAS), where servers respond with HTML fragments rather than JSON.

## Core Concepts

### Fundamental Pattern

htmx generalizes the hypertext concept beyond traditional anchors and forms:

- Any element can issue HTTP requests (not just `<a>` and `<form>`)
- Any event can trigger requests (not just clicks and submissions)
- Any HTTP verb can be used (GET, POST, PUT, PATCH, DELETE)
- Any element can be the target for updates (not just the whole page)

### Installation Options

Choose from multiple installation methods:

**CDN (fastest setup):**
```html
<script src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js" integrity="sha384-/TgkGk7p307TH7EXJDuUlgG3Ce1UVolAOFopFekQkkXihi5u/6OCvVKyz1W+idaz" crossorigin="anonymous"></script>
```

**npm:**
```bash
npm install htmx.org@2.0.8
```

**Direct download:** Download from jsDelivr and include via script tag.

## Working with htmx

### Reference Documentation

The complete htmx documentation is available in `references/htmx-org-docs.md`. This reference file contains approximately 87,000 characters of detailed documentation covering all aspects of the library.

**To find specific topics in the reference file, use grep patterns:**

```bash
# Find AJAX attribute documentation
grep -A 20 "hx-get\|hx-post\|hx-put\|hx-patch\|hx-delete" references/htmx-org-docs.md

# Find trigger and event information
grep -A 30 "hx-trigger\|trigger modifiers\|trigger filters" references/htmx-org-docs.md

# Find swap and target documentation
grep -A 25 "hx-swap\|hx-target\|swap modifiers" references/htmx-org-docs.md

# Find WebSocket and SSE information
grep -A 20 "websockets\|SSE\|server-sent events" references/htmx-org-docs.md

# Find configuration options
grep -A 50 "htmx.config\|configuring" references/htmx-org-docs.md

# Find security-related content
grep -A 30 "security\|CSRF\|CSP\|Content Security Policy" references/htmx-org-docs.md

# Find animation and transition information
grep -A 25 "animations\|transitions\|View Transitions" references/htmx-org-docs.md

# Find validation and form handling
grep -A 20 "validation\|hx-validate" references/htmx-org-docs.md
```

### Common Implementation Patterns

**Basic AJAX Request:**

Refer to `references/htmx-org-docs.md` for core AJAX attributes (`hx-get`, `hx-post`, `hx-put`, `hx-patch`, `hx-delete`). Each attribute issues the corresponding HTTP request when triggered.

```html
<button hx-post="/clicked" hx-trigger="click" hx-target="#parent-div" hx-swap="outerHTML">
    Click Me!
</button>
```

**Custom Triggers:**

Consult `references/htmx-org-docs.md` for trigger modifiers, filters, and special events. Default triggers are `change` for inputs, `submit` for forms, and `click` for other elements.

**Content Swapping:**

See `references/htmx-org-docs.md` for swap strategies (innerHTML, outerHTML, beforebegin, afterbegin, beforeend, afterend, delete, none) and swap modifiers (transition, swap delay, settle delay, scroll, show).

**Indicators and Loading States:**

Reference `references/htmx-org-docs.md` for the indicator system using `htmx-indicator` class and `hx-indicator` attribute.

**Form Enhancement:**

Check `references/htmx-org-docs.md` for boosting regular links and forms with `hx-boost`, which converts them to AJAX requests while maintaining progressive enhancement.

### Advanced Features

**WebSockets and Server-Sent Events:**

Consult `references/htmx-org-docs.md` for WebSocket and SSE integration patterns using extensions.

**History Management:**

Refer to `references/htmx-org-docs.md` for history support with `hx-push-url` and browser back/forward navigation.

**Out-of-Band Swaps:**

See `references/htmx-org-docs.md` for updating multiple page sections from a single response using `hx-swap-oob`.

**Request Synchronization:**

Check `references/htmx-org-docs.md` for coordinating requests between elements using `hx-sync` to prevent race conditions.

**CSS Transitions and Animations:**

Reference `references/htmx-org-docs.md` for CSS transition support, View Transitions API integration, and animation techniques.

**Extensions:**

Consult `references/htmx-org-docs.md` for available extensions including morphing algorithms (Idiomorph, Morphdom), debug helpers, and custom functionality.

### Events and Scripting

**Event System:**

Refer to `references/htmx-org-docs.md` for the complete event lifecycle, including `htmx:beforeRequest`, `htmx:afterSwap`, `htmx:configRequest`, and other events for intercepting and modifying htmx behavior.

**Inline Scripting:**

See `references/htmx-org-docs.md` for the `hx-on` attribute that enables inline event handlers without separate script tags.

**JavaScript API:**

Check `references/htmx-org-docs.md` for programmatic access to htmx functionality through the `htmx` global object.

### Integration and Security

**Third-Party Integration:**

Consult `references/htmx-org-docs.md` for guidance on integrating with Web Components, Alpine.js, and other frameworks.

**Security Considerations:**

Reference `references/htmx-org-docs.md` for:
- CSRF token handling with `hx-headers`
- Content Security Policy configuration
- Request validation with `htmx:validateUrl` event
- Same-origin policy controls via `htmx.config.selfRequestsOnly`

**Caching:**

See `references/htmx-org-docs.md` for cache control strategies and the `HX-Revalidate` response header.

### Configuration

All configuration options are documented in `references/htmx-org-docs.md`. Access configuration via:

```javascript
htmx.config.defaultSwapStyle = "outerHTML";
```

Or declaratively via meta tag:

```html
<meta name="htmx-config" content='{"defaultSwapStyle":"outerHTML"}'>
```

### Debugging

Refer to `references/htmx-org-docs.md` for debugging techniques, including event logging and development tools.

## Migration Guidance

For projects migrating from htmx 1.x or intercooler.js, consult the migration guides referenced in `references/htmx-org-docs.md`.

## Response Format

When implementing server endpoints for htmx, return HTML fragments rather than JSON. The server response should contain the HTML to be swapped into the target element. Include appropriate headers like `HX-Trigger` for client-side events or `HX-Redirect` for navigation.

## Progressive Enhancement

Design htmx applications with progressive enhancement in mind. Basic functionality should work without JavaScript, with htmx enhancing the experience when available. Use `hx-boost` to upgrade traditional links and forms incrementally.