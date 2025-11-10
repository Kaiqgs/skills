Logger | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Logger
======
Logger
------
Gorm has a [default logger implementation](https://github.com/go-gorm/gorm/blob/master/logger/logger.go), it will print Slow SQL and happening errors by default
The logger accepts few options, you can customize it during initialization, for example:
|  |
| --- |
| ``` newLogger := logger.New(   log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer   logger.Config{     SlowThreshold:              time.Second,   // Slow SQL threshold     LogLevel:                   logger.Silent, // Log level     IgnoreRecordNotFoundError: true,           // Ignore ErrRecordNotFound error for logger     ParameterizedQueries:      true,           // Don't include params in the SQL log     Colorful:                  false,          // Disable color   }, )  // Globally mode db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{   Logger: newLogger, })  // Continuous session mode tx := db.Session(&Session{Logger: newLogger}) tx.First(&user) tx.Model(&user).Update("Age", 18) ``` |
### Log Levels
GORM defined log levels: `Silent`, `Error`, `Warn`, `Info`
|  |
| --- |
| ``` db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{   Logger: logger.Default.LogMode(logger.Silent), }) ``` |
### Debug
Debug a single operation, change current operation’s log level to logger.Info
|  |
| --- |
| ``` db.Debug().Where("name = ?", "jinzhu").First(&User{}) ``` |
Customize Logger
Refer to GORM’s [default logger](https://github.com/go-gorm/gorm/blob/master/logger/logger.go) for how to define your own one
The logger needs to implement the following interface, it accepts `context`, so you can use it for log tracing
|  |
| --- |
| ``` type Interface interface {   LogMode(LogLevel) Interface   Info(context.Context, string, ...interface{})   Warn(context.Context, string, ...interface{})   Error(context.Context, string, ...interface{})   Trace(ctx context.Context, begin time.Time, fc func() (sql string, rowsAffected int64), err error) } ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](migration.html "Migration")[Next](generic_interface.html "Generic Database Interface")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Logger](#Logger)
1. [Log Levels](#Log-Levels)
2. [Debug](#Debug)
2. [Customize Logger](#Customize-Logger)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/logger.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)