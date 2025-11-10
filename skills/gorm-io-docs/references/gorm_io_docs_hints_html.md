Hints | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Hints
=====
GORM provides optimizer/index/comment hints support
<https://github.com/go-gorm/hints>
Optimizer Hints
|  |
| --- |
| ``` import "gorm.io/hints"  db.Clauses(hints.New("hint")).Find(&User{}) // SELECT * /*+ hint */ FROM `users` ``` |
Index Hints
|  |
| --- |
| ``` import "gorm.io/hints"  db.Clauses(hints.UseIndex("idx_user_name")).Find(&User{}) // SELECT * FROM `users` USE INDEX (`idx_user_name`)  db.Clauses(hints.ForceIndex("idx_user_name", "idx_user_id").ForJoin()).Find(&User{}) // SELECT * FROM `users` FORCE INDEX FOR JOIN (`idx_user_name`,`idx_user_id`)"  db.Clauses(   hints.ForceIndex("idx_user_name", "idx_user_id").ForOrderBy(),   hints.IgnoreIndex("idx_user_name").ForGroupBy(), ).Find(&User{}) // SELECT * FROM `users` FORCE INDEX FOR ORDER BY (`idx_user_name`,`idx_user_id`) IGNORE INDEX FOR GROUP BY (`idx_user_name`)" ``` |
Comment Hints
|  |
| --- |
| ``` import "gorm.io/hints"  db.Clauses(hints.Comment("select", "master")).Find(&User{}) // SELECT /*master*/ * FROM `users`;  db.Clauses(hints.CommentBefore("insert", "node2")).Create(&user) // /*node2*/ INSERT INTO `users` ...;  db.Clauses(hints.CommentAfter("select", "node2")).Create(&user) // /*node2*/ INSERT INTO `users` ...;  db.Clauses(hints.CommentAfter("where", "hint")).Find(&User{}, "id = ?", 1) // SELECT * FROM `users` WHERE id = ? /* hint */ ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](prometheus.html "Prometheus")[Next](indexes.html "Indexes")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Optimizer Hints](#Optimizer-Hints)
2. [Index Hints](#Index-Hints)
3. [Comment Hints](#Comment-Hints)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/hints.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)