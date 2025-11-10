---
name: gorm-io-docs
description: This skill should be used when working with GORM (Go Object-Relational Mapping library) for database operations in Go applications. Apply this skill when defining models, performing CRUD operations, managing database connections, implementing associations, writing migrations, optimizing queries, or troubleshooting GORM-related issues.
---

# GORM Documentation

This skill provides comprehensive guidance for working with GORM, the Go ORM library for database interactions. Use this skill to efficiently build, query, and maintain database-driven Go applications.

## Overview

GORM is a developer-friendly ORM library for Golang that supports MySQL, PostgreSQL, SQLite, SQL Server, and other databases. This skill covers model declaration, CRUD operations, associations, migrations, performance optimization, and advanced features.

## Getting Started

### Initial Setup and Connection

For database connection setup and configuration, consult `references/gorm-io-docs-connecting-to-the-database-html.md`. This reference covers:
- Connecting to MySQL, PostgreSQL, SQLite, SQL Server, and other databases
- Connection pool configuration
- DSN (Data Source Name) formatting

For an overview of GORM capabilities and quick examples, refer to `references/gorm-io-docs-index-html.md` and `references/gorm-io-docs.md`.

### Using the Generics API

GORM v1.30.0+ supports Go generics for type-safe database operations. For comprehensive guidance on the generics approach versus traditional API, consult `references/gorm-io-docs-the-generics-way-html.md`.

## Defining Models

### Model Declaration

To define database models with proper struct tags and field types, consult `references/gorm-io-docs-models-html.md`. This reference covers:
- Basic model structure with gorm.Model
- Field tags for customization (column names, types, constraints)
- Primary keys and auto-increment
- Embedded structs
- Field-level permissions (read-only, write-only, create-only, update-only, ignored)

### Conventions

GORM follows conventions for table names, column names, and timestamps. For details on default behaviors and how to override them, refer to `references/gorm-io-docs-conventions-html.md`.

### Custom Data Types

To implement custom data types with Scanner and Valuer interfaces, consult `references/gorm-io-docs-data-types-html.md`. This covers serialization of complex types to database columns.

For advanced serialization strategies, refer to `references/gorm-io-docs-serializer-html.md`.

## CRUD Operations

### Creating Records

For inserting single records, batch inserts, and handling created associations, consult `references/gorm-io-docs-create-html.md`. Key topics include:
- Create with generics: `gorm.G[User](db).Create(ctx, &user)`
- Batch creation
- Default values and hooks
- Upsert operations
- Associations on create

### Querying Records

For retrieving data with various conditions and methods, consult `references/gorm-io-docs-query-html.md`. This reference covers:
- First, Last, Find methods
- Where conditions with placeholders
- Not, Or conditions
- Selecting specific fields
- Ordering, limiting, and offsetting
- Group by and having clauses
- Distinct queries
- Joins
- Scanning results into structs or maps

**Grep patterns for query.md**: "First", "Find", "Where", "Select", "Order", "Limit", "Group", "Having", "Joins", "Scan"

### Advanced Querying

For complex query patterns and optimization techniques, consult `references/gorm-io-docs-advanced-query-html.md`. Topics include:
- Smart field selection
- Locking (FOR UPDATE)
- SubQueries
- From SubQuery
- Group conditions
- Named arguments
- Find to Map
- FirstOrInit, FirstOrCreate
- Optimizer hints and index hints
- Iterating with FindInBatches

**Grep patterns for advanced_query.md**: "SubQuery", "Locking", "FindInBatches", "FirstOrInit", "FirstOrCreate", "Index Hints"

### Updating Records

For modifying existing records with various strategies, consult `references/gorm-io-docs-update-html.md`. Key operations:
- Save (update all fields)
- Update single column
- Updates multiple columns
- Update with struct or map
- Select and Omit for controlling updated fields
- Batch updates
- Update with SQL expressions
- Returning updated data

**Grep patterns for update.md**: "Save", "Update", "Updates", "Select", "Omit", "SQL Expr"

### Deleting Records

For removing records and soft delete functionality, consult `references/gorm-io-docs-delete-html.md`. Topics include:
- Delete single records
- Batch delete
- Soft delete with DeletedAt
- Permanently deleting soft-deleted records
- Finding soft-deleted records with Unscoped

## Associations

### Association Types

GORM supports four association types. Consult the following references for each:

**Belongs To**: `references/gorm-io-docs-belongs-to-html.md`
- Defining belongs to relationships
- Foreign keys and references
- Override defaults

**Has One**: `references/gorm-io-docs-has-one-html.md`
- One-to-one relationships
- Foreign key configuration
- Polymorphic has one

**Has Many**: `references/gorm-io-docs-has-many-html.md`
- One-to-many relationships
- Foreign key and references
- Self-referential has many

**Many To Many**: `references/gorm-io-docs-many-to-many-html.md`
- Join table configuration
- Custom join table names and fields
- Self-referential many-to-many

### Working with Associations

For CRUD operations on associations and association mode, consult `references/gorm-io-docs-associations-html.md`. This covers:
- Auto create/update associations
- Skip auto create/update
- Association mode methods (Append, Replace, Delete, Clear, Count)
- Select and Omit with associations
- Deleting with Select

**Grep patterns for associations.md**: "Association Mode", "Append", "Replace", "Delete associations", "Select associations"

### Preloading (Eager Loading)

To efficiently load associations and avoid N+1 query problems, consult `references/gorm-io-docs-preload-html.md`. Topics include:
- Preload with generics API
- Preloading multiple associations
- Nested preloading
- Conditions on preload
- Custom preloading SQL
- Preload all associations

**Grep patterns for preload.md**: "Preload", "Nested", "Conditions", "Preload All"

### Polymorphic Associations

For associations where a model can belong to multiple other models on a single association, consult `references/gorm-io-docs-polymorphism-html.md`.

## Database Management

### Migrations

For schema creation and modification using AutoMigrate, consult `references/gorm-io-docs-migration-html.md`. Topics include:
- AutoMigrate for creating/updating tables
- Migrator interface for advanced operations
- Creating/dropping tables, columns, indexes
- Checking for existence
- Constraints management

**Grep patterns for migration.md**: "AutoMigrate", "Migrator", "CreateTable", "DropTable", "AddColumn", "CreateIndex"

### Indexes

To define and manage database indexes for performance, consult `references/gorm-io-docs-indexes-html.md`. This covers:
- Composite indexes
- Unique indexes
- Index naming
- Index priority and options
- Creating and dropping indexes via Migrator

### Constraints

For foreign key constraints, check constraints, and other database constraints, consult `references/gorm-io-docs-constraints-html.md`.

### Composite Primary Keys

When models require multiple fields as primary key, consult `references/gorm-io-docs-composite-primary-key-html.md`.

## Advanced Topics

### Transactions

For ensuring data consistency with transaction support, consult `references/gorm-io-docs-transactions-html.md`. Topics include:
- Transaction with closure
- Manual transaction control (Begin, Commit, Rollback)
- Nested transactions and SavePoint
- Transaction with context

### Hooks

To execute custom logic at specific points in GORM operations, consult `references/gorm-io-docs-hooks-html.md`. Hooks include:
- Creating: BeforeSave, BeforeCreate, AfterSave, AfterCreate
- Updating: BeforeSave, BeforeUpdate, AfterSave, AfterUpdate
- Deleting: BeforeDelete, AfterDelete
- Querying: AfterFind

### Context Support

For timeout control and context propagation through database operations, consult `references/gorm-io-docs-context-html.md`.

### Sessions

To create new session instances with specific configurations, consult `references/gorm-io-docs-session-html.md`. Session options include:
- DryRun (generate SQL without executing)
- PrepareStmt (prepared statement mode)
- NewDB (create new DB instance without conditions)
- SkipHooks, DisableNestedTransaction
- AllowGlobalUpdate, FullSaveAssociations

### Method Chaining

To understand GORM's fluent API and chain multiple methods, consult `references/gorm-io-docs-method-chaining-html.md`. Topics include:
- Chain methods vs finisher methods
- Reusing logic with method chains
- New session vs shared instance

### Scopes

For reusable query logic encapsulated in functions, consult `references/gorm-io-docs-scopes-html.md`. Scopes enable composable query patterns.

### Raw SQL and SQL Builder

For executing raw SQL queries and building custom SQL, consult `references/gorm-io-docs-sql-builder-html.md`. This covers:
- Raw queries with Scan
- Exec for non-query operations
- Named arguments (sql.Named, map)
- DryRun for SQL inspection
- Row and Rows methods
- ToSQL method for SQL generation

**Grep patterns for sql_builder.md**: "Raw", "Exec", "Named", "DryRun", "ToSQL", "Row", "Rows"

### Error Handling

For checking and handling GORM-specific errors, consult `references/gorm-io-docs-error-handling-html.md`. Important errors include:
- ErrRecordNotFound
- Error translation from database drivers

### Database Resolver

For read/write splitting and multiple database sources, consult `references/gorm-io-docs-dbresolver-html.md`. Topics include:
- Configuring replicas and sources
- Load balancing strategies
- Automatic read/write splitting
- Manual source selection
- Transaction handling with resolver

**Grep patterns for dbresolver.md**: "Replicas", "Sources", "Load Balancing", "Read Write Splitting"

### Sharding

For horizontal partitioning of large tables, consult `references/gorm-io-docs-sharding-html.md`.

### Performance Optimization

To improve query performance and reduce overhead, consult `references/gorm-io-docs-performance-html.md`. Topics include:
- Disabling default transaction for Create/Update/Delete
- Prepared statement caching
- Using indexes effectively
- Selecting specific fields

### Hints

For database-specific optimizer hints and index hints, consult `references/gorm-io-docs-hints-html.md`.

### Settings

For managing custom configuration via Set/Get on DB instance, consult `references/gorm-io-docs-settings-html.md`.

## Configuration

### GORM Configuration

For initialization options and global configuration, consult `references/gorm-io-docs-gorm-config-html.md`. Configuration includes:
- Logger configuration
- NamingStrategy for table/column names
- DisableAutomaticPing, DisableForeignKeyConstraintWhenMigrating
- Prepared statement support
- Transaction options

### Logger Configuration

For customizing GORM's logging behavior, consult `references/gorm-io-docs-logger-html.md`. Topics include:
- Log levels (Silent, Error, Warn, Info)
- Custom logger implementation
- Slow query threshold
- Colorized output

### Generic Database Interface

To access the underlying `*sql.DB` for connection pooling and advanced operations, consult `references/gorm-io-docs-generic-interface-html.md`.

## Monitoring and Plugins

### Prometheus Integration

For exposing GORM metrics to Prometheus, consult `references/gorm-io-docs-prometheus-html.md`.

### Writing Plugins

To extend GORM with custom plugins using callbacks, consult `references/gorm-io-docs-write-plugins-html.md`. Topics include:
- Callback system (Query, Create, Update, Delete, Row)
- Registering callbacks
- Plugin interface implementation

### Writing Database Drivers

To implement custom database driver support, consult `references/gorm-io-docs-write-driver-html.md`.

## Security

### SQL Injection Prevention

For security best practices and avoiding SQL injection vulnerabilities, consult `references/gorm-io-docs-security-html.md`. Key principles:
- Always use parameterized queries
- Avoid concatenating user input into SQL
- Validating input before database operations

## Migration and Version Information

### Upgrading to GORM 2.0

For breaking changes and migration guide from GORM v1, consult `references/gorm-io-docs-v2-release-note-html.md`. Major changes include:
- API changes and incompatibilities
- New features (Context, Batch Insert, Named Arguments)
- Performance improvements
- Plugin system changes

**Grep patterns for v2-release-note.md**: "Breaking Changes", "Context", "Batch Insert", "Named Argument", "Association Mode"

### Changelog

For version history and recent changes, consult `references/gorm-io-docs-changelog-html.md`.

## Workflow Guidance

### Common Development Patterns

**Define Models → Connect → Migrate → Query**

1. Define models using guidance from `references/gorm-io-docs-models-html.md` and `references/gorm-io-docs-conventions-html.md`
2. Establish database connection using `references/gorm-io-docs-connecting-to-the-database-html.md`
3. Run migrations using `references/gorm-io-docs-migration-html.md`
4. Execute CRUD operations using `references/gorm-io-docs-create-html.md`, `references/gorm-io-docs-query-html.md`, `references/gorm-io-docs-update-html.md`, and `references/gorm-io-docs-delete-html.md`

**Optimizing Complex Queries**

1. Start with basic queries in `references/gorm-io-docs-query-html.md`
2. Apply advanced techniques from `references/gorm-io-docs-advanced-query-html.md`
3. Use preloading from `references/gorm-io-docs-preload-html.md` to avoid N+1 queries
4. Add indexes using `references/gorm-io-docs-indexes-html.md`
5. Monitor performance with `references/gorm-io-docs-performance-html.md`
6. Apply hints if needed using `references/gorm-io-docs-hints-html.md`

**Implementing Association-Heavy Models**

1. Define associations using `references/gorm-io-docs-belongs-to-html.md`, `references/gorm-io-docs-has-one-html.md`, `references/gorm-io-docs-has-many-html.md`, or `references/gorm-io-docs-many-to-many-html.md`
2. Use Association Mode from `references/gorm-io-docs-associations-html.md` for relationship management
3. Apply eager loading from `references/gorm-io-docs-preload-html.md`
4. Consider polymorphic associations from `references/gorm-io-docs-polymorphism-html.md` if applicable

**Building Production-Ready Applications**

1. Configure logging using `references/gorm-io-docs-logger-html.md`
2. Implement proper error handling with `references/gorm-io-docs-error-handling-html.md`
3. Use context for timeout control per `references/gorm-io-docs-context-html.md`
4. Apply transactions from `references/gorm-io-docs-transactions-html.md` for data consistency
5. Add hooks from `references/gorm-io-docs-hooks-html.md` for auditing or validation
6. Review security practices in `references/gorm-io-docs-security-html.md`
7. Configure connection pooling via `references/gorm-io-docs-generic-interface-html.md`
8. Set up monitoring with `references/gorm-io-docs-prometheus-html.md`

## Finding Specific Information

When searching for specific GORM functionality:

- **Model definition issues**: Check `references/gorm-io-docs-models-html.md`, `references/gorm-io-docs-conventions-html.md`, and `references/gorm-io-docs-data-types-html.md`
- **Query problems**: Start with `references/gorm-io-docs-query-html.md`, escalate to `references/gorm-io-docs-advanced-query-html.md`
- **Association errors**: Identify type in `references/gorm-io-docs-belongs-to-html.md`, `references/gorm-io-docs-has-one-html.md`, `references/gorm-io-docs-has-many-html.md`, or `references/gorm-io-docs-many-to-many-html.md`, then check `references/gorm-io-docs-associations-html.md`
- **Performance issues**: Review `references/gorm-io-docs-performance-html.md`, `references/gorm-io-docs-preload-html.md`, and `references/gorm-io-docs-indexes-html.md`
- **Configuration problems**: Check `references/gorm-io-docs-gorm-config-html.md` and `references/gorm-io-docs-connecting-to-the-database-html.md`
- **Raw SQL needs**: Consult `references/gorm-io-docs-sql-builder-html.md`
- **Advanced features**: Review `references/gorm-io-docs-dbresolver-html.md`, `references/gorm-io-docs-sharding-html.md`, `references/gorm-io-docs-session-html.md`
