SQL Builder | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
SQL Builder
Raw SQL
-------
### Generics API
Query Raw SQL with `Scan`
|  |
| --- |
| ``` type Result struct {   ID   int   Name string   Age  int }  // Scan into a single result result, err := gorm.G[Result](db).Raw("SELECT id, name, age FROM users WHERE id = ?", 3).Find(context.Background())  // Scan into a primitive type age, err := gorm.G[int](db).Raw("SELECT SUM(age) FROM users WHERE role = ?", "admin").Find(context.Background())  // Scan into a slice users, err := gorm.G[User](db).Raw("UPDATE users SET name = ? WHERE age = ? RETURNING id, name", "jinzhu", 20).Find(context.Background()) ``` |
`Exec` with Raw SQL
|  |
| --- |
| ``` // Execute raw SQL result := gorm.WithResult() err := gorm.G[any](db, result).Exec(context.Background(), "DROP TABLE users")  // Execute with parameters err = gorm.G[any](db).Exec(context.Background(), "UPDATE orders SET shipped_at = ? WHERE id IN ?", time.Now(), []int64{1, 2, 3})  // Exec with SQL Expression err = gorm.G[any](db).Exec(context.Background(), "UPDATE users SET money = ? WHERE name = ?", gorm.Expr("money * ? + ?", 10000, 1), "jinzhu") ``` |
### Traditional API
Query Raw SQL with `Scan`
|  |
| --- |
| ``` type Result struct {   ID   int   Name string   Age  int }  var result Result db.Raw("SELECT id, name, age FROM users WHERE id = ?", 3).Scan(&result)  db.Raw("SELECT id, name, age FROM users WHERE name = ?", "jinzhu").Scan(&result)  var age int db.Raw("SELECT SUM(age) FROM users WHERE role = ?", "admin").Scan(&age)  var users []User db.Raw("UPDATE users SET name = ? WHERE age = ? RETURNING id, name", "jinzhu", 20).Scan(&users) ``` |
`Exec` with Raw SQL
|  |
| --- |
| ``` db.Exec("DROP TABLE users") db.Exec("UPDATE orders SET shipped_at = ? WHERE id IN ?", time.Now(), []int64{1, 2, 3})  // Exec with SQL Expression db.Exec("UPDATE users SET money = ? WHERE name = ?", gorm.Expr("money * ? + ?", 10000, 1), "jinzhu") ``` |
> **NOTE** GORM allows cache prepared statement to increase performance, checkout [Performance](performance.html) for details
Named Argument
### Generics API
GORM supports named arguments with [`sql.NamedArg`](https://tip.golang.org/pkg/database/sql/#NamedArg), `map[string]interface{}{}` or struct, for example:
|  |
| --- |
### Traditional API
GORM supports named arguments with [`sql.NamedArg`](https://tip.golang.org/pkg/database/sql/#NamedArg), `map[string]interface{}{}` or struct, for example:
|  |
| --- |
| ``` db.Where("name1 = @name OR name2 = @name", sql.Named("name", "jinzhu")).Find(&user) // SELECT * FROM `users` WHERE name1 = "jinzhu" OR name2 = "jinzhu"  db.Where("name1 = @name OR name2 = @name", map[string]interface{}{"name": "jinzhu2"}).First(&result3) // SELECT * FROM `users` WHERE name1 = "jinzhu2" OR name2 = "jinzhu2" ORDER BY `users`.`id` LIMIT 1  // Named Argument with Raw SQL db.Raw("SELECT * FROM users WHERE name1 = @name OR name2 = @name2 OR name3 = @name",    sql.Named("name", "jinzhu1"), sql.Named("name2", "jinzhu2")).Find(&user) // SELECT * FROM users WHERE name1 = "jinzhu1" OR name2 = "jinzhu2" OR name3 = "jinzhu1"  db.Exec("UPDATE users SET name1 = @name, name2 = @name2, name3 = @name",    sql.Named("name", "jinzhunew"), sql.Named("name2", "jinzhunew2")) // UPDATE users SET name1 = "jinzhunew", name2 = "jinzhunew2", name3 = "jinzhunew"  db.Raw("SELECT * FROM users WHERE (name1 = @name AND name3 = @name) AND name2 = @name2",    map[string]interface{}{"name": "jinzhu", "name2": "jinzhu2"}).Find(&user) // SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2"  type NamedArgument struct {   Name string   Name2 string }  db.Raw("SELECT * FROM users WHERE (name1 = @Name AND name3 = @Name) AND name2 = @Name2",    NamedArgument{Name: "jinzhu", Name2: "jinzhu2"}).Find(&user) // SELECT * FROM users WHERE (name1 = "jinzhu" AND name3 = "jinzhu") AND name2 = "jinzhu2" ``` |
DryRun Mode
Generate `SQL` and its arguments without executing, can be used to prepare or test generated SQL, Checkout [Session](session.html) for details
|  |
| --- |
| ``` stmt := db.Session(&gorm.Session{DryRun: true}).First(&user, 1).Statement stmt.SQL.String() //=> SELECT * FROM `users` WHERE `id` = $1 ORDER BY `id` stmt.Vars         //=> []interface{}{1} ``` |
ToSQL
-----
Returns generated `SQL` without executing.
GORM uses the database/sql’s argument placeholders to construct the SQL statement, which will automatically escape arguments to avoid SQL injection, but the generated SQL don’t provide the safety guarantees, please only use it for debugging.
|  |
| --- |
| ``` sql := db.ToSQL(func(tx *gorm.DB) *gorm.DB {   return tx.Model(&User{}).Where("id = ?", 100).Limit(10).Order("age desc").Find(&[]User{}) }) sql //=> SELECT * FROM "users" WHERE id = 100 AND "users"."deleted_at" IS NULL ORDER BY age desc LIMIT 10 ``` |
`Row` & `Rows`
### Generics API
Get result as `*sql.Row`
|  |
| --- |
| ``` // Use GORM API build SQL row := gorm.G[any](db).Table("users").Where("name = ?", "jinzhu").Select("name", "age").Row(context.Background()) row.Scan(&name, &age)  // Use Raw SQL row := gorm.G[any](db).Raw("select name, age, email from users where name = ?", "jinzhu").Row(context.Background()) row.Scan(&name, &age, &email) ``` |
Get result as `*sql.Rows`
|  |
| --- |
| ``` // Use GORM API build SQL rows, err := gorm.G[User](db).Where("name = ?", "jinzhu").Select("name, age, email").Rows(context.Background()) defer rows.Close() for rows.Next() {   rows.Scan(&name, &age, &email)    // do something }  // Raw SQL rows, err := gorm.G[any](db).Raw("select name, age, email from users where name = ?", "jinzhu").Rows(context.Background()) defer rows.Close() for rows.Next() {   rows.Scan(&name, &age, &email)    // do something } ``` |
### Traditional API
Get result as `*sql.Row`
|  |
| --- |
| ``` // Use GORM API build SQL row := db.Table("users").Where("name = ?", "jinzhu").Select("name", "age").Row() row.Scan(&name, &age)  // Use Raw SQL row := db.Raw("select name, age, email from users where name = ?", "jinzhu").Row() row.Scan(&name, &age, &email) ``` |
Get result as `*sql.Rows`
|  |
| --- |
| ``` // Use GORM API build SQL rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() defer rows.Close() for rows.Next() {   rows.Scan(&name, &age, &email)    // do something }  // Raw SQL rows, err := db.Raw("select name, age, email from users where name = ?", "jinzhu").Rows() defer rows.Close() for rows.Next() {   rows.Scan(&name, &age, &email)    // do something } ``` |
Checkout [FindInBatches](advanced_query.html) for how to query and process records in batch
Checkout [Group Conditions](advanced_query.html#group_conditions) for how to build complicated SQL Query
Scan `*sql.Rows` into struct
Use `ScanRows` to scan a row into a struct, for example:
|  |
| --- |
| ``` rows, err := db.Model(&User{}).Where("name = ?", "jinzhu").Select("name, age, email").Rows() // (*sql.Rows, error) defer rows.Close()  var user User for rows.Next() {   // ScanRows scan a row into user   db.ScanRows(rows, &user)    // do something } ``` |
Connection
Run mutliple SQL in same db tcp connection (not in a transaction)
|  |
| --- |
| ``` db.Connection(func(tx *gorm.DB) error {   tx.Exec("SET my.role = ?", "admin")    tx.First(&User{}) }) ``` |
Advanced
--------
### Clauses
GORM uses SQL builder generates SQL internally, for each operation, GORM creates a `*gorm.Statement` object, all GORM APIs add/change `Clause` for the `Statement`, at last, GORM generated SQL based on those clauses
For example, when querying with `First`, it adds the following clauses to the `Statement`
|  |
| --- |
| ``` var limit = 1 clause.Select{Columns: []clause.Column{{Name: "*"}}} clause.From{Tables: []clause.Table{{Name: clause.CurrentTable}}} clause.Limit{Limit: &limit} clause.OrderBy{Columns: []clause.OrderByColumn{   {     Column: clause.Column{       Table: clause.CurrentTable,       Name:  clause.PrimaryKey,     },   }, }} ``` |
Then GORM build finally querying SQL in the `Query` callbacks like:
|  |
| --- |
| ``` Statement.Build("SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "LIMIT", "FOR") ``` |
Which generate SQL:
|  |
| --- |
| ``` SELECT * FROM `users` ORDER BY `users`.`id` LIMIT 1 ``` |
You can define your own `Clause` and use it with GORM, it needs to implements [Interface](https://pkg.go.dev/gorm.io/gorm/clause?tab=doc#Interface)
Check out [examples](https://github.com/go-gorm/gorm/tree/master/clause) for reference
### Clause Builder
For different databases, Clauses may generate different SQL, for example:
|  |
| --- |
| ``` db.Offset(10).Limit(5).Find(&users) // Generated for SQL Server // SELECT * FROM "users" OFFSET 10 ROW FETCH NEXT 5 ROWS ONLY // Generated for MySQL // SELECT * FROM `users` LIMIT 5 OFFSET 10 ``` |
Which is supported because GORM allows database driver register Clause Builder to replace the default one, take the [Limit](https://github.com/go-gorm/sqlserver/blob/512546241200023819d2e7f8f2f91d7fb3a52e42/sqlserver.go#L45) as example
### Clause Options
GORM defined [Many Clauses](https://github.com/go-gorm/gorm/tree/master/clause), and some clauses provide advanced options can be used for your application
Although most of them are rarely used, if you find GORM public API can’t match your requirements, may be good to check them out, for example:
|  |
| --- |
| ``` db.Clauses(clause.Insert{Modifier: "IGNORE"}).Create(&user) // INSERT IGNORE INTO users (name,age...) VALUES ("jinzhu",18...); ``` |
### StatementModifier
GORM provides interface [StatementModifier](https://pkg.go.dev/gorm.io/gorm?tab=doc#StatementModifier) allows you modify statement to match your requirements, take [Hints](hints.html) as example
|  |
| --- |
| ``` import "gorm.io/hints"  db.Clauses(hints.New("hint")).Find(&User{}) // SELECT * /*+ hint */ FROM `users` ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](delete.html "Delete")[Next](belongs_to.html "Belongs To")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Raw SQL](#Raw-SQL)
1. [Generics API](#Generics-API)
2. [Traditional API](#Traditional-API)
2. [Named Argument](#Named-Argument)
1. [Generics API](#Generics-API-1)
2. [Traditional API](#Traditional-API-1)
3. [DryRun Mode](#DryRun-Mode)
4. [ToSQL](#ToSQL)
5. [Row & Rows](#Row-Rows)
1. [Generics API](#Generics-API-2)
2. [Traditional API](#Traditional-API-2)
6. [Scan \*sql.Rows into struct](#Scan-sql-Rows-into-struct)
7. [Connection](#Connection)
8. [Advanced](#Advanced)
1. [Clauses](#Clauses)
2. [Clause Builder](#Clause-Builder)
3. [Clause Options](#Clause-Options)
4. [StatementModifier](#StatementModifier)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/sql_builder.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)