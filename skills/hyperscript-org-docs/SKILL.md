---
name: hyperscript-org-docs
description: This skill should be used when working with hyperscript, the event-oriented scripting language for front-end web development. Use when writing, debugging, or understanding hyperscript code that handles DOM manipulation, event handling, async operations, AJAX requests, or browser interactions. Also applies when converting JavaScript/jQuery to hyperscript or implementing locality-of-behavior patterns in HTML.
---

# Hyperscript Documentation

This skill provides comprehensive guidance for working with hyperscript, an event-oriented scripting language designed for front-end web development with natural language syntax.

## Overview

Hyperscript is a HyperTalk-inspired scripting language that enables direct embedding of event handling and DOM manipulation logic within HTML elements. The language emphasizes locality of behavior, async transparency, and readable code that resembles natural English.

## Core Documentation

All hyperscript documentation is consolidated in `references/hyperscript-org-docs.md`. This file contains approximately 80,000 characters covering the complete language specification, commands, expressions, and patterns.

### Finding Information in the Reference

The reference file is large, so use grep patterns to locate specific topics efficiently:

- **Installation and setup**: `grep -A 10 "Install & Quick Start" references/hyperscript-org-docs.md`
- **Event handling**: `grep -A 20 "Events & Event Handlers" references/hyperscript-org-docs.md`
- **DOM manipulation**: `grep -A 15 "Working With The DOM" references/hyperscript-org-docs.md`
- **Async operations**: `grep -A 20 "Async Transparency" references/hyperscript-org-docs.md`
- **Variables and scoping**: `grep -A 15 "Variables" references/hyperscript-org-docs.md`
- **Control flow**: `grep -A 10 "Control Flow" references/hyperscript-org-docs.md`
- **AJAX/fetch operations**: `grep -A 15 "Remote Content" references/hyperscript-org-docs.md`
- **Debugging**: `grep -A 20 "Debugging" references/hyperscript-org-docs.md`
- **Security**: `grep -A 10 "Security" references/hyperscript-org-docs.md`
- **Extending hyperscript**: `grep -A 15 "Extending" references/hyperscript-org-docs.md`

## Common Workflows

### Writing Basic Event Handlers

To create event handlers in hyperscript:

1. Load `references/hyperscript-org-docs.md` and locate the "Events & Event Handlers" section
2. Use the `on <event>` syntax directly in HTML attributes using `_` or `data-script`
3. Reference special variables like `me`, `it`, `result`, and `event`
4. Apply event filters, queueing, and destructuring as needed

Example pattern:
```html
<button _="on click toggle .active on me">Click Me</button>
```

### DOM Queries and Manipulation

To work with the DOM:

1. Consult the "Working With The DOM" section in `references/hyperscript-org-docs.md`
2. Use DOM literals with angle brackets: `<div/>`, `<button.class/>`, `<#elementId/>`
3. Apply positional selectors: `first`, `last`, `next`, `previous`
4. Use commands: `put`, `set`, `add`, `remove`, `toggle`, `show`, `hide`

### Async Operations

For handling asynchronous operations:

1. Review the "Async Transparency" section in `references/hyperscript-org-docs.md`
2. Understand that most operations are automatically async-transparent
3. Use `wait` for explicit delays or promises
4. Apply `async` keyword only when necessary for parallel operations

### AJAX and Remote Content

To fetch remote content:

1. Reference the "Remote Content" section in `references/hyperscript-org-docs.md`
2. Use `fetch` command with various options (method, headers, body)
3. Handle responses with `then` or direct variable assignment
4. Use `go` command for navigation

### Debugging Hyperscript

To debug code:

1. Load the "Debugging" section from `references/hyperscript-org-docs.md`
2. Insert `beep!` operator for pass-through expression logging
3. Use `breakpoint` commands with HDB (Hyperscript Debugger)
4. Enable console logging with `log` command

### Converting from JavaScript/jQuery

To migrate JavaScript or jQuery code:

1. Consult the "Using JavaScript" section in `references/hyperscript-org-docs.md`
2. Replace callback patterns with async transparency
3. Convert DOM queries to hyperscript literals
4. Use `js` for inline JavaScript when needed

## Key Language Concepts

### Syntax Characteristics

- Natural language style with verb-first commands
- No parentheses around conditions in `if` statements
- `end` keyword to close blocks (often optional)
- Underscore `_` attribute for inline scripts
- Async transparency by default

### Special Variables and Symbols

Review these in the "Special Names & Symbols" section:

- `me`, `my`, `I` - Reference to current element
- `it`, `its` - Reference to result of previous expression
- `result` - Explicit result reference
- `event`, `detail` - Event-related data
- `target` - Event target

### Command Structure

Commands follow the pattern: `<verb> <expression> <preposition> <target>`

Example: `put "text" into #output`

### Expression Types

Load relevant sections for:

- Comparisons: `is`, `is not`, `matches`, `exists`
- Collections: arrays, element collections
- Properties: dot notation, flat mapping, null safety
- Math operations: standard operators plus natural language
- String operations: templates, interpolation

## Integration Patterns

### With HTMX

Hyperscript integrates seamlessly with HTMX:

- Respond to HTMX events like `htmx:load`, `htmx:afterSwap`
- Access HTMX attributes and configuration
- Complement HTMX's hypermedia exchanges with client-side interactions

### With Standard JavaScript

To interoperate with JavaScript:

1. Call JavaScript functions directly from hyperscript
2. Use `js` expression for inline JavaScript blocks
3. Access global JavaScript objects and APIs
4. Extend hyperscript grammar with custom commands

## Advanced Features

For advanced use cases, reference these sections in `references/hyperscript-org-docs.md`:

- **Behaviors**: Reusable behavior definitions
- **Web Workers**: Background processing support
- **Web Sockets**: Real-time communication
- **Event Source**: Server-sent events
- **Exception Handling**: `catch` and `throw` commands

## Security Considerations

Load the "Security" section when dealing with:

- User-generated content
- CSP policies (hyperscript is interpreted, not eval-based)
- Use `data-disable-scripting` attribute to prevent execution in untrusted areas

## Reference Loading Strategy

1. **For general queries**: Load entire `references/hyperscript-org-docs.md`
2. **For specific features**: Use grep patterns to extract relevant sections
3. **For examples**: Search for "Example:" in the reference
4. **For command syntax**: Look for command names followed by their detailed explanations

## Common Patterns

Reference the cookbook section in the documentation for:

- Toggle patterns
- Form validation
- AJAX loading indicators
- Keyboard shortcuts
- Animation sequences
- Modal dialogs
- Infinite scroll
- Drag and drop

To implement any hyperscript functionality, start by loading the appropriate section from `references/hyperscript-org-docs.md` using the grep patterns provided above, then apply the syntax and patterns documented there.
