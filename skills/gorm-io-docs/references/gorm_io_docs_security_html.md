Security | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Security
========
GORM uses the `database/sql`‘s argument placeholders to construct the SQL statement, which will automatically escape arguments to avoid SQL injection
> **NOTE** The SQL from Logger is not fully escaped like the one executed, be careful when copying and executing it in SQL console
Query Condition
User’s input should be only used as an argument, for example:
|  |
| --- |
| ``` userInput := "jinzhu;drop table users;"  // safe, will be escaped db.Where("name = ?", userInput).First(&user)  // SQL injection db.Where(fmt.Sprintf("name = %v", userInput)).First(&user) ``` |
Inline Condition
|  |
| --- |
| ``` // will be escaped db.First(&user, "name = ?", userInput)  // SQL injection db.First(&user, fmt.Sprintf("name = %v", userInput)) ``` |
When retrieving objects with number primary key by user’s input, you should check the type of variable.
|  |
| --- |
| ``` userInputID := "1=1;drop table users;" // safe, return error id, err := strconv.Atoi(userInputID) if err != nil {     return err } db.First(&user, id)  // SQL injection db.First(&user, userInputID) // SELECT * FROM users WHERE 1=1;drop table users; ``` |
SQL injection Methods
To support some features, some inputs are not escaped, be careful when using user’s input with those methods
|  |
| --- |
| ``` db.Select("name; drop table users;").First(&user) db.Distinct("name; drop table users;").First(&user)  db.Model(&user).Pluck("name; drop table users;", &names)  db.Group("name; drop table users;").First(&user)  db.Group("name").Having("1 = 1;drop table users;").First(&user)  db.Raw("select name from users; drop table users;").First(&user)  db.Exec("select name from users; drop table users;")  db.Order("name; drop table users;").First(&user)  db.Table("users; drop table users;").Find(&users)  db.Delete(&User{}, "id=1; drop table users;")  db.Joins("inner join orders; drop table users;").Find(&users)  db.InnerJoins("inner join orders; drop table users;").Find(&users)  //Despite being parameterized in Exec() function, gorm.Expr is still injectable db.Exec("UPDATE users SET name = '?' WHERE id = 1", gorm.Expr("alice'; drop table users;-- "))  db.Where("id=1").Not("name = 'alice'; drop table users;").Find(&users)  db.Where("id=1").Or("name = 'alice'; drop table users;").Find(&users)  db.Find(&User{}, "name = 'alice'; drop table users;")  // The following functions can only be injected by blind SQL injection methods db.First(&users, "2 or 1=1-- ")  db.FirstOrCreate(&users, "2 or 1=1-- ")  db.FirstOrInit(&users, "2 or 1=1-- ")  db.Last(&users, "2 or 1=1-- ")  db.Take(&users, "2 or 1=1-- ") ``` |
The general rule to avoid SQL injection is don’t trust user-submitted data, you can perform whitelist validation to test user input against an existing set of known, approved, and defined input, and when using user’s input, only use them as an argument.
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](composite_primary_key.html "Composite Primary Key")[Next](gorm_config.html "GORM Config")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
[Get the Drop. Weekly front-end tools, tips, and resources.
**Contents**
1. [Query Condition](#Query-Condition)
2. [Inline Condition](#Inline-Condition)
3. [SQL injection Methods](#SQL-injection-Methods)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/security.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)