Settings | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Settings
========
GORM provides `Set`, `Get`, `InstanceSet`, `InstanceGet` methods allow users pass values to [hooks](hooks.html) or other methods
GORM uses this for some features, like pass creating table options when migrating table.
|  |
| --- |
| ``` // Add table suffix when creating tables db.Set("gorm:table_options", "ENGINE=InnoDB").AutoMigrate(&User{}) ``` |
Set / Get
---------
Use `Set` / `Get` pass settings to hooks methods, for example:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCard CreditCard   // ... }  func (u *User) BeforeCreate(tx *gorm.DB) error {   myValue, ok := tx.Get("my_value")   // ok => true   // myValue => 123 }  type CreditCard struct {   gorm.Model   // ... }  func (card *CreditCard) BeforeCreate(tx *gorm.DB) error {   myValue, ok := tx.Get("my_value")   // ok => true   // myValue => 123 }  myValue := 123 db.Set("my_value", myValue).Create(&User{}) ``` |
InstanceSet / InstanceGet
Use `InstanceSet` / `InstanceGet` pass settings to current `*Statement`‘s hooks methods, for example:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCard CreditCard   // ... }  func (u *User) BeforeCreate(tx *gorm.DB) error {   myValue, ok := tx.InstanceGet("my_value")   // ok => true   // myValue => 123 }  type CreditCard struct {   gorm.Model   // ... }  // When creating associations, GORM creates a new `*Statement`, so can't read other instance's settings func (card *CreditCard) BeforeCreate(tx *gorm.DB) error {   myValue, ok := tx.InstanceGet("my_value")   // ok => false   // myValue => nil }  myValue := 123 db.InstanceSet("my_value", myValue).Create(&User{}) ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](conventions.html "Conventions")[Next](dbresolver.html "Database Resolver")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Set / Get](#Set-Get)
2. [InstanceSet / InstanceGet](#InstanceSet-InstanceGet)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/settings.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)