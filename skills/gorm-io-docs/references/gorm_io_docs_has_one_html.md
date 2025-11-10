Has One | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Has One
=======
Has One
-------
A `has one` association sets up a one-to-one connection with another model, but with somewhat different semantics (and consequences). This association indicates that each instance of a model contains or possesses one instance of another model.
For example, if your application includes users and credit cards, and each user can only have one credit card.
### Declare
|  |
| --- |
| ``` // User has one CreditCard, UserID is the foreign key type User struct {   gorm.Model   CreditCard CreditCard }  type CreditCard struct {   gorm.Model   Number string   UserID uint } ``` |
### Retrieve
|  |
| --- |
| ``` // Retrieve user list with eager loading credit card func GetAll(db *gorm.DB) ([]User, error) {   var users []User   err := db.Model(&User{}).Preload("CreditCard").Find(&users).Error   return users, err } ``` |
Override Foreign Key
For a `has one` relationship, a foreign key field must also exist, the owner will save the primary key of the model belongs to it into this field.
The field’s name is usually generated with `has one` model’s type plus its `primary key`, for the above example it is `UserID`.
When you give a credit card to the user, it will save the User’s `ID` into its `UserID` field.
If you want to use another field to save the relationship, you can change it with tag `foreignKey`, e.g:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCard CreditCard `gorm:"foreignKey:UserName"`   // use UserName as foreign key }  type CreditCard struct {   gorm.Model   Number   string   UserName string } ``` |
Override References
By default, the owned entity will save the `has one` model’s primary key into a foreign key, you could change to save another field’s value, like using `Name` for the below example.
You are able to change it with tag `references`, e.g:
|  |
| --- |
| ``` type User struct {   gorm.Model   Name       string     `gorm:"index"`   CreditCard CreditCard `gorm:"foreignKey:UserName;references:Name"` }  type CreditCard struct {   gorm.Model   Number   string   UserName string } ``` |
CRUD with Has One
Please checkout [Association Mode](associations.html#Association-Mode) for working with `has one` relations
Eager Loading
GORM allows eager loading `has one` associations with `Preload` or `Joins`, refer [Preloading (Eager loading)](preload.html) for details
Self-Referential Has One
|  |
| --- |
| ``` type User struct {   gorm.Model   Name      string   ManagerID *uint   Manager   *User } ``` |
FOREIGN KEY Constraints
You can setup `OnUpdate`, `OnDelete` constraints with tag `constraint`, it will be created when migrating with GORM, for example:
|  |
| --- |
| ``` type User struct {   gorm.Model   CreditCard CreditCard `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;"` }  type CreditCard struct {   gorm.Model   Number string   UserID uint } ``` |
You are also allowed to delete selected has one associations with `Select` when deleting, checkout [Delete with Select](associations.html#delete_with_select) for details
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](belongs_to.html "Belongs To")[Next](has_many.html "Has Many")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Has One](#Has-One)
1. [Declare](#Declare)
2. [Retrieve](#Retrieve)
2. [Override Foreign Key](#Override-Foreign-Key)
3. [Override References](#Override-References)
4. [CRUD with Has One](#CRUD-with-Has-One)
5. [Eager Loading](#Eager-Loading)
6. [Self-Referential Has One](#Self-Referential-Has-One)
7. [FOREIGN KEY Constraints](#FOREIGN-KEY-Constraints)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/has_one.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)