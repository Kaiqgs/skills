Generic database interface sql.DB | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Generic database interface sql.DB
GORM provides the method `DB` which returns a generic database interface [\*sql.DB](https://pkg.go.dev/database/sql#DB) from the current `*gorm.DB`
|  |
| --- |
| ``` // Get generic database object sql.DB to use its functions sqlDB, err := db.DB()  // Ping sqlDB.Ping()  // Close sqlDB.Close()  // Returns database statistics sqlDB.Stats() ``` |
> **NOTE** If the underlying database connection is not a `*sql.DB`, like in a transaction, it will returns error
Connection Pool
|  |
| --- |
| ``` // Get generic database object sql.DB to use its functions sqlDB, err := db.DB()  // SetMaxIdleConns sets the maximum number of connections in the idle connection pool. sqlDB.SetMaxIdleConns(10)  // SetMaxOpenConns sets the maximum number of open connections to the database. sqlDB.SetMaxOpenConns(100)  // SetConnMaxLifetime sets the maximum amount of time a connection may be reused. sqlDB.SetConnMaxLifetime(time.Hour) ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](logger.html "Logger")[Next](performance.html "Performance")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Connection Pool](#Connection-Pool)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/generic_interface.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)