Composite Primary Key | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Composite Primary Key
Set multiple fields as primary key creates composite primary key, for example:
|  |
| --- |
| ``` type Product struct {   ID           string `gorm:"primaryKey"`   LanguageCode string `gorm:"primaryKey"`   Code         string   Name         string } ``` |
**Note** integer `PrioritizedPrimaryField` enables `AutoIncrement` by default, to disable it, you need to turn off `autoIncrement` for the int fields:
|  |
| --- |
| ``` type Product struct {   CategoryID uint64 `gorm:"primaryKey;autoIncrement:false"`   TypeID     uint64 `gorm:"primaryKey;autoIncrement:false"` } ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](constraints.html "Constraints")[Next](security.html "Security")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/composite_primary_key.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)