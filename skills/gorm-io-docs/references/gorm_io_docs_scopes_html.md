Scopes | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Scopes
======
Scopes allow you to re-use commonly used logic, the shared logic needs to be defined as type `func(*gorm.DB) *gorm.DB`
Query
-----
Scope examples for querying
|  |
| --- |
| ``` func AmountGreaterThan1000(db *gorm.DB) *gorm.DB {   return db.Where("amount > ?", 1000) }  func PaidWithCreditCard(db *gorm.DB) *gorm.DB {   return db.Where("pay_mode = ?", "card") }  func PaidWithCod(db *gorm.DB) *gorm.DB {   return db.Where("pay_mode = ?", "cod") }  func OrderStatus(status []string) func (db *gorm.DB) *gorm.DB {   return func (db *gorm.DB) *gorm.DB {     return db.Scopes(AmountGreaterThan1000).Where("status IN (?)", status)   } }  db.Scopes(AmountGreaterThan1000, PaidWithCreditCard).Find(&orders) // Find all credit card orders and amount greater than 1000  db.Scopes(AmountGreaterThan1000, PaidWithCod).Find(&orders) // Find all COD orders and amount greater than 1000  db.Scopes(AmountGreaterThan1000, OrderStatus([]string{"paid", "shipped"})).Find(&orders) // Find all paid, shipped orders that amount greater than 1000 ``` |
### Pagination
|  |
| --- |
| ``` func Paginate(r *http.Request) func(db *gorm.DB) *gorm.DB {   return func (db *gorm.DB) *gorm.DB {     q := r.URL.Query()     page, _ := strconv.Atoi(q.Get("page"))     if page <= 0 {       page = 1     }      pageSize, _ := strconv.Atoi(q.Get("page_size"))     switch {     case pageSize > 100:       pageSize = 100     case pageSize <= 0:       pageSize = 10     }      offset := (page - 1) * pageSize     return db.Offset(offset).Limit(pageSize)   } }  db.Scopes(Paginate(r)).Find(&users) db.Scopes(Paginate(r)).Find(&articles) ``` |
Dynamically Table
Use `Scopes` to dynamically set the query Table
|  |
| --- |
| ``` func TableOfYear(user *User, year int) func(db *gorm.DB) *gorm.DB {   return func(db *gorm.DB) *gorm.DB {     tableName := user.TableName() + strconv.Itoa(year)     return db.Table(tableName)   } }  DB.Scopes(TableOfYear(user, 2019)).Find(&users) // SELECT * FROM users_2019;  DB.Scopes(TableOfYear(user, 2020)).Find(&users) // SELECT * FROM users_2020;  // Table form different database func TableOfOrg(user *User, dbName string) func(db *gorm.DB) *gorm.DB {   return func(db *gorm.DB) *gorm.DB {     tableName := dbName + "." + user.TableName()     return db.Table(tableName)   } }  DB.Scopes(TableOfOrg(user, "org1")).Find(&users) // SELECT * FROM org1.users;  DB.Scopes(TableOfOrg(user, "org2")).Find(&users) // SELECT * FROM org2.users; ``` |
Updates
-------
Scope examples for updating/deleting
|  |
| --- |
| ``` func CurOrganization(r *http.Request) func(db *gorm.DB) *gorm.DB {   return func (db *gorm.DB) *gorm.DB {     org := r.Query("org")      if org != "" {       var organization Organization       if db.Session(&Session{}).First(&organization, "name = ?", org).Error == nil {         return db.Where("org_id = ?", organization.ID)       }     }      db.AddError("invalid organization")     return db   } }  db.Model(&article).Scopes(CurOrganization(r)).Update("Name", "name 1") // UPDATE articles SET name = "name 1" WHERE org_id = 111 db.Scopes(CurOrganization(r)).Delete(&Article{}) // DELETE FROM articles WHERE org_id = 111 ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](data_types.html "Customize Data Types")[Next](conventions.html "Conventions")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Query](#Query)
1. [Pagination](#Pagination)
2. [Dynamically Table](#Dynamically-Table)
3. [Updates](#Updates)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/scopes.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)