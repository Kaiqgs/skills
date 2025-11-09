Error Handling | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Error Handling
Effective error handling is a cornerstone of robust application development in Go, particularly when interacting with databases using GORM. GORM’s approach to error handling requires a nuanced understanding based on the API style you’re using.
Basic Error Handling
### Generics API
With the Generics API, errors are returned directly from the operation methods, following Go’s standard error handling pattern:
|  |
| --- |
| ``` ctx := context.Background()  // Error handling with direct return values user, err := gorm.G[User](db).Where("name = ?", "jinzhu").First(ctx) if err != nil {   // Handle error... }  // For operations that don't return a result err := gorm.G[User](db).Where("id = ?", 1).Delete(ctx) if err != nil {   // Handle error... } ``` |
### Traditional API
With the Traditional API, GORM integrates error handling into its chainable method syntax. The `*gorm.DB` instance contains an `Error` field, which is set when an error occurs. The common practice is to check this field after executing database operations, especially after [Finisher Methods](method_chaining.html#finisher_method).
After a chain of methods, it’s crucial to check the `Error` field:
|  |
| --- |
| ``` if err := db.Where("name = ?", "jinzhu").First(&user).Error; err != nil {   // Handle error... } ``` |
Or alternatively:
|  |
| --- |
| ``` if result := db.Where("name = ?", "jinzhu").First(&user); result.Error != nil {   // Handle error... } ``` |
`ErrRecordNotFound`
GORM returns `ErrRecordNotFound` when no record is found using methods like `First`, `Last`, `Take`.
### Generics API
|  |
| --- |
| ``` ctx := context.Background()  user, err := gorm.G[User](db).First(ctx) if errors.Is(err, gorm.ErrRecordNotFound) {   // Handle record not found error... } ``` |
### Traditional API
|  |
| --- |
| ``` err := db.First(&user, 100).Error if errors.Is(err, gorm.ErrRecordNotFound) {   // Handle record not found error... } ``` |
Handling Error Codes
Many databases return errors with specific codes, which can be indicative of various issues like constraint violations, connection problems, or syntax errors. Handling these error codes in GORM requires parsing the error returned by the database and extracting the relevant code.
|  |
| --- |
| ``` import (     "github.com/go-sql-driver/mysql"     "gorm.io/gorm" )  // ...  result := db.Create(&newRecord) if result.Error != nil {     if mysqlErr, ok := result.Error.(*mysql.MySQLError); ok {         switch mysqlErr.Number {         case 1062: // MySQL code for duplicate entry             // Handle duplicate entry         // Add cases for other specific error codes         default:             // Handle other errors         }     } else {         // Handle non-MySQL errors or unknown errors     } } ``` |
Dialect Translated Errors
GORM can return specific errors related to the database dialect being used, when `TranslateError` is enabled, GORM converts database-specific errors into its own generalized errors.
|  |
| --- |
| ``` db, err := gorm.Open(postgres.Open(postgresDSN), &gorm.Config{TranslateError: true}) ``` |
* **ErrDuplicatedKey**
This error occurs when an insert operation violates a unique constraint:
|  |
| --- |
| ``` result := db.Create(&newRecord) if errors.Is(result.Error, gorm.ErrDuplicatedKey) {     // Handle duplicated key error... } ``` |
* **ErrForeignKeyViolated**
This error is encountered when a foreign key constraint is violated:
|  |
| --- |
| ``` result := db.Create(&newRecord) if errors.Is(result.Error, gorm.ErrForeignKeyViolated) {     // Handle foreign key violation error... } ``` |
By enabling `TranslateError`, GORM provides a more unified way of handling errors across different databases, translating database-specific errors into common GORM error types.
Errors
------
For a complete list of errors that GORM can return, refer to the [Errors List](https://github.com/go-gorm/gorm/blob/master/errors.go) in GORM’s documentation.
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](context.html "Context")[Next](method_chaining.html "Method Chaining")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Basic Error Handling](#Basic-Error-Handling)
1. [Generics API](#Generics-API)
2. [Traditional API](#Traditional-API)
2. [ErrRecordNotFound](#ErrRecordNotFound)
1. [Generics API](#Generics-API-1)
2. [Traditional API](#Traditional-API-1)
3. [Handling Error Codes](#Handling-Error-Codes)
4. [Dialect Translated Errors](#Dialect-Translated-Errors)
5. [Errors](#Errors)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/error_handling.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)