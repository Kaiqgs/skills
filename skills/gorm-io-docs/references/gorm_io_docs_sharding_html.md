Sharding | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Sharding
========
Sharding plugin using SQL parser and replace for splits large tables into smaller ones, redirects Query into sharding tables. Give you a high performance database access.
<https://github.com/go-gorm/sharding>
Features
--------
* Non-intrusive design. Load the plugin, specify the config, and all done.
* Lighting-fast. No network based middlewares, as fast as Go.
* Multiple database (PostgreSQL, MySQL) support.
* Integrated primary key generator (Snowflake, PostgreSQL Sequence, Custom, …).
Usage
-----
Config the sharding middleware, register the tables which you want to shard. See [Godoc](https://pkg.go.dev/gorm.io/sharding) for config details.
|  |
| --- |
| ``` import (     "fmt"      "gorm.io/driver/postgres"     "gorm.io/gorm"     "gorm.io/sharding" )  db, err := gorm.Open(postgres.New(postgres.Config{DSN: "postgres://localhost:5432/sharding-db?sslmode=disable"))  db.Use(sharding.Register(sharding.Config{     ShardingKey:         "user_id",     NumberOfShards:      64,     PrimaryKeyGenerator: sharding.PKSnowflake, }, "orders", Notification{}, AuditLog{})) // This case for show up give notifications, audit_logs table use same sharding rule. ``` |
Use the db session as usual. Just note that the query should have the `Sharding Key` when operate sharding tables.
|  |
| --- |
| ``` // Gorm create example, this will insert to orders_02 db.Create(&Order{UserID: 2}) // sql: INSERT INTO orders_2 ...  // Show have use Raw SQL to insert, this will insert into orders_03 db.Exec("INSERT INTO orders(user_id) VALUES(?)", int64(3))  // This will throw ErrMissingShardingKey error, because there not have sharding key presented. db.Create(&Order{Amount: 10, ProductID: 100}) fmt.Println(err)  // Find, this will redirect query to orders_02 var orders []Order db.Model(&Order{}).Where("user_id", int64(2)).Find(&orders) fmt.Printf("%#v\n", orders)  // Raw SQL also supported db.Raw("SELECT * FROM orders WHERE user_id = ?", int64(3)).Scan(&orders) fmt.Printf("%#v\n", orders)  // This will throw ErrMissingShardingKey error, because WHERE conditions not included sharding key err = db.Model(&Order{}).Where("product_id", "1").Find(&orders).Error fmt.Println(err)  // Update and Delete are similar to create and query db.Exec("UPDATE orders SET product_id = ? WHERE user_id = ?", 2, int64(3)) err = db.Exec("DELETE FROM orders WHERE product_id = 3").Error fmt.Println(err) // ErrMissingShardingKey ``` |
The full example is [here](https://github.com/go-gorm/sharding/tree/main/examples).
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](dbresolver.html "Database Resolver")[Next](serializer.html "Serializer")
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
1. [Features](#Features)
2. [Usage](#Usage)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/sharding.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)