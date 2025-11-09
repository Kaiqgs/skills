GORM Guides | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
GORM Guides
The fantastic ORM library for Golang aims to be developer friendly.
Overview
--------
* Full-Featured ORM
* Associations (Has One, Has Many, Belongs To, Many To Many, Polymorphism, Single-table inheritance)
* Hooks (Before/After Create/Save/Update/Delete/Find)
* Eager loading with `Preload`, `Joins`
* Transactions, Nested Transactions, Save Point, RollbackTo to Saved Point
* Context, Prepared Statement Mode, DryRun Mode
* Batch Insert, FindInBatches, Find/Create with Map, CRUD with SQL Expr and Context Valuer
* SQL Builder, Upsert, Locking, Optimizer/Index/Comment Hints, Named Argument, SubQuery
* Composite Primary Key, Indexes, Constraints
* Auto Migrations
* Logger
* Generics API for type-safe queries and operations
* Extendable, flexible plugin API: Database Resolver (multiple databases, read/write splitting) / Prometheus…
* Every feature comes with tests
* Developer Friendly
Install
-------
|  |
| --- |
| ``` go get -u gorm.io/gorm go get -u gorm.io/driver/sqlite ``` |
Quick Start
### Generics API (>= v1.30.0)
|  |
| --- |
### Traditional API
|  |
| --- |
| ``` package main  import (   "gorm.io/driver/sqlite"   "gorm.io/gorm" )  type Product struct {   gorm.Model   Code  string   Price uint }  func main() {   db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})   if err != nil {     panic("failed to connect database")   }    // Migrate the schema   db.AutoMigrate(&Product{})    // Create   db.Create(&Product{Code: "D42", Price: 100})    // Read   var product Product   db.First(&product, 1) // find product with integer primary key   db.First(&product, "code = ?", "D42") // find product with code D42    // Update - update product's price to 200   db.Model(&product).Update("Price", 200)   // Update - update multiple fields   db.Model(&product).Updates(Product{Price: 200, Code: "F42"}) // non-zero fields   db.Model(&product).Updates(map[string]interface{}{"Price": 200, "Code": "F42"})    // Delete - delete product   db.Delete(&product, 1) } ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Next](models.html "Declaring Models")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Overview](#Overview)
2. [Install](#Install)
3. [Quick Start](#Quick-Start)
1. [Generics API (>= v1.30.0)](#Generics-API-v1-30-0)
2. [Traditional API](#Traditional-API)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/index.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)