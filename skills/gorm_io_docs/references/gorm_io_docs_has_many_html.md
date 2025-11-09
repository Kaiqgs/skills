Has Many | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Has Many
========
Has Many
--------
A `has many` association sets up a one-to-many connection with another model, unlike `has one`, the owner could have zero or many instances of models.
For example, if your application includes users and credit card, and each user can have many credit cards.
### Declare
|  |
| --- |
| ``` // User has many CreditCards, UserID is the foreign key type User struct {   gorm.Model   CreditCards []CreditCard }  type CreditCard struct {   gorm.Model   Number string   UserID uint } ``` |
### Retrieve
|  |
| --- |
| ``` // Retrieve user list with eager loading credit cards func GetAll(db *gorm.DB) ([]User, error) {     var users []User     err := db.Model(&User{}).Preload("CreditCards").Find(&users).Error     return users, err } ``` |
Override Foreign Key
To define a `has many` relationship, a foreign key must exist. The default foreign key’s name is the owner’s type name plus the name of its primary key field
For example, to define a model that belongs to `User`, the foreign key should be `UserID`.
To use another field as foreign key, you can customize it with a `foreignKey` tag, e.g:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCards []CreditCard `gorm:"foreignKey:UserRefer"` }  type CreditCard struct {   gorm.Model   Number    string   UserRefer uint } ``` |
Override References
GORM usually uses the owner’s primary key as the foreign key’s value, for the above example, it is the `User`‘s `ID`,
When you assign credit cards to a user, GORM will save the user’s `ID` into credit cards’ `UserID` field.
You are able to change it with tag `references`, e.g:
|  |
| --- |
| ``` type User struct {   gorm.Model   MemberNumber string   CreditCards  []CreditCard `gorm:"foreignKey:UserNumber;references:MemberNumber"` }  type CreditCard struct {   gorm.Model   Number     string   UserNumber string } ``` |
CRUD with Has Many
Please checkout [Association Mode](associations.html#Association-Mode) for working with has many relations
Eager Loading
GORM allows eager loading has many associations with `Preload`, refer [Preloading (Eager loading)](preload.html) for details
Self-Referential Has Many
|  |
| --- |
| ``` type User struct {   gorm.Model   Name      string   ManagerID *uint   Team      []User `gorm:"foreignkey:ManagerID"` } ``` |
FOREIGN KEY Constraints
You can setup `OnUpdate`, `OnDelete` constraints with tag `constraint`, it will be created when migrating with GORM, for example:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCards []CreditCard `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"` }  type CreditCard struct {   gorm.Model   Number string   UserID uint } ``` |
You are also allowed to delete selected has many associations with `Select` when deleting, checkout [Delete with Select](associations.html#delete_with_select) for details
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](has_one.html "Has One")[Next](many_to_many.html "Many To Many")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Has Many](#Has-Many)
1. [Declare](#Declare)
2. [Retrieve](#Retrieve)
2. [Override Foreign Key](#Override-Foreign-Key)
3. [Override References](#Override-References)
4. [CRUD with Has Many](#CRUD-with-Has-Many)
5. [Eager Loading](#Eager-Loading)
6. [Self-Referential Has Many](#Self-Referential-Has-Many)
7. [FOREIGN KEY Constraints](#FOREIGN-KEY-Constraints)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/has_many.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)