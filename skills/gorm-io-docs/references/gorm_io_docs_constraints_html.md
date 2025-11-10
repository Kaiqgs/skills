Constraints | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Constraints
GORM allows create database constraints with tag, constraints will be created when [AutoMigrate or CreateTable with GORM](migration.html)
CHECK Constraint
Create CHECK constraints with tag `check`
|  |
| --- |
| ``` type UserIndex struct {   Name  string `gorm:"check:name_checker,name <> 'jinzhu'"`   Name2 string `gorm:"check:name <> 'jinzhu'"`   Name3 string `gorm:"check:,name <> 'jinzhu'"` } ``` |
Index Constraint
Checkout [Database Indexes](indexes.html)
Foreign Key Constraint
GORM will creates foreign keys constraints for associations, you can disable this feature during initialization:
|  |
| --- |
| ``` db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{   DisableForeignKeyConstraintWhenMigrating: true, }) ``` |
GORM allows you setup FOREIGN KEY constraints’s `OnDelete`, `OnUpdate` option with tag `constraint`, for example:
|  |
| --- |
| ``` type User struct {   gorm.Model   CompanyID  int   Company    Company    `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"`   CreditCard CreditCard `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"` }  type CreditCard struct {   gorm.Model   Number string   UserID uint }  type Company struct {   ID   int   Name string } ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](indexes.html "Indexes")[Next](composite_primary_key.html "Composite Primary Key")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [CHECK Constraint](#CHECK-Constraint)
2. [Index Constraint](#Index-Constraint)
3. [Foreign Key Constraint](#Foreign-Key-Constraint)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/constraints.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)