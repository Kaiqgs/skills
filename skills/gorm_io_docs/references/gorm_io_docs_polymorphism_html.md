Polymorphism | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Polymorphism
Polymorphism Association
GORM supports polymorphism association for `has one` and `has many`, it will save owned entity’s table name into polymorphic type’s field, primary key value into the polymorphic field
By default `polymorphic:<value>` will prefix the column type and column id with `<value>`.
The value will be the table name pluralized.
|  |
| --- |
| ``` type Dog struct {   ID   int   Name string   Toys []Toy `gorm:"polymorphic:Owner;"` }  type Toy struct {   ID        int   Name      string   OwnerID   int   OwnerType string }  db.Create(&Dog{Name: "dog1", Toys: []Toy{{Name: "toy1"}, {Name: "toy2"}}}) // INSERT INTO `dogs` (`name`) VALUES ("dog1") // INSERT INTO `toys` (`name`,`owner_id`,`owner_type`) VALUES ("toy1",1,"dogs"), ("toy2",1,"dogs") ``` |
You can specify polymorphism properties separately using the following GORM tags:
* `polymorphicType`: Specifies the column type.
* `polymorphicId`: Specifies the column ID.
* `polymorphicValue`: Specifies the value of the type.
|  |
| --- |
| ``` type Dog struct {   ID   int   Name string   Toys []Toy `gorm:"polymorphicType:Kind;polymorphicId:OwnerID;polymorphicValue:master"` }  type Toy struct {   ID        int   Name      string   OwnerID   int   Kind      string }  db.Create(&Dog{Name: "dog1", Toys: []Toy{{Name: "toy1"}, {Name: "toy2"}}}) // INSERT INTO `dogs` (`name`) VALUES ("dog1") // INSERT INTO `toys` (`name`,`owner_id`,`kind`) VALUES ("toy1",1,"master"), ("toy2",1,"master") ``` |
In these examples, we’ve used a has-many relationship, but the same principles apply to has-one relationships.
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](many_to_many.html "Many To Many")[Next](associations.html "Association Mode")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Polymorphism Association](#Polymorphism-Association)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/polymorphism.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)