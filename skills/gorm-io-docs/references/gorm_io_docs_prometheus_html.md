Prometheus | GORM - The fantastic ORM library for Golang, aims to be developer friendly.
Prometheus
GORM provides Prometheus plugin to collect [DBStats](https://pkg.go.dev/database/sql?tab=doc#DBStats) or user-defined metrics
<https://github.com/go-gorm/prometheus>
Usage
-----
|  |
| --- |
| ``` import (   "gorm.io/gorm"   "gorm.io/driver/sqlite"   "gorm.io/plugin/prometheus" )  db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{})  db.Use(prometheus.New(prometheus.Config{   DBName:          "db1", // use `DBName` as metrics label   RefreshInterval: 15,    // Refresh metrics interval (default 15 seconds)   PushAddr:        "prometheus pusher address", // push metrics if `PushAddr` configured   StartServer:     true,  // start http server to expose metrics   HTTPServerPort:  8080,  // configure http server port, default port 8080 (if you have configured multiple instances, only the first `HTTPServerPort` will be used to start server)   MetricsCollector: []prometheus.MetricsCollector {     &prometheus.MySQL{       VariableNames: []string{"Threads_running"},     },   },  // user defined metrics })) ``` |
User-Defined Metrics
You can define your metrics and collect them with GORM Prometheus plugin, which needs to implements `MetricsCollector` interface
|  |
| --- |
| ``` type MetricsCollector interface {   Metrics(*Prometheus) []prometheus.Collector } ``` |
### MySQL
GORM provides an example for how to collect MySQL Status as metrics, check it out [prometheus.MySQL](https://github.com/go-gorm/prometheus/blob/master/mysql.go)
|  |
| --- |
| ``` &prometheus.MySQL{   Prefix: "gorm_status_",   // Metrics name prefix, default is `gorm_status_`   // For example, Threads_running's metric name is `gorm_status_Threads_running`   Interval: 100,   // Fetch interval, default use Prometheus's RefreshInterval   VariableNames: []string{"Threads_running"},   // Select variables from SHOW STATUS, if not set, uses all status variables } ``` |
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/go-gorm/gorm?label=Latest GORM Release&color=red&&style=for-the-badge&logo=go&logoColor=red)](v2_release_note.html)
Last updated: 2025-11-04
[Prev](serializer.html "Serializer")[Next](hints.html "Hints")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Gold Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
Platinum Sponsors
[Become a Sponsor!](/contribute.html#Donations "Help to deliver a better GORM!")
**Contents**
1. [Usage](#Usage)
2. [User-Defined Metrics](#User-Defined-Metrics)
1. [MySQL](#MySQL)
[Improve this page](https://github.com/go-gorm/gorm.io/edit/master/pages/docs/prometheus.md)
[Back to Top](#)
© 2013~2025 [Jinzhu](https://github.com/jinzhu)