参考：[How to use Debezium SMT with Groovy to filter routing events | Red Hat Developer](https://developers.redhat.com/articles/2023/07/06/how-use-debezium-smt-groovy-filter-routing-events#)



After configuring my Kafka Connect Image with Debezium, demonstrated in Hugo Guerrero's article [Improve your Kafka Connect builds of Debezium](https://developers.redhat.com/articles/2021/12/06/improve-your-kafka-connect-builds-debezium#), I needed to configure a type of filter to only bring certain events from the database table to my topics. I was able to do this using Debezium SMT with Groovy.



## What is Debezium SMT?

Debezium SMT (single message transform) is a filter feature provided by Debezium that is used to process only records that you find relevant. To do that, you need to include plugins the implementations of the JSR223 API (Scripting for the Java Platform) inside your Kafka Connect Image.

Note that Debezium does not come with an JSR 223 implementation, so you will need to provide the libs to use this feature. We will use the Groovy implementation of JSR 223, so you can download all the relevant jars from the [Groovy website](https://groovy-lang.org/).

There are other JSR 223 implementations that you can use, however, we will not cover them here. If you want information about this, go to [Debezium documentation](https://access.redhat.com/documentation/en-us/red_hat_integration/2021.q3/html-single/debezium_user_guide/index#filtering-debezium-change-event-records).



## Download the files

First of all, you will need your database plugin (i.e., SQL Server or MySQL) from the [download page](https://access.redhat.com/jbossnetwork/restricted/listSoftware.html?downloadType=distributions&product=red.hat.integration&version=2022-Q4). Figure 1 illustrates the Red Hat software downloads page.

[![A screenshot of the Red Hat software download page.](https://developers.redhat.com/sites/default/files/styles/article_floated/public/screenshot_2023-03-31_at_10.02.31.png?itok=I0rE4fLs)](https://developers.redhat.com/sites/default/files/screenshot_2023-03-31_at_10.02.31.png)

Figure 1: The Red Hat software download page.



That is the connector will need to put in your Kafka Connect to work with MySQL CDC*.* You will also need to download the scripting transformation package.

With this in place, go to the [Groovy website](https://groovy-lang.org/) and download the zip that contains all the JAR's files, as shown in Figure 2.

[![A screenshot of the Groovy download page.](https://developers.redhat.com/sites/default/files/styles/article_floated/public/screenshot_2023-04-03_at_11.59.38.png?itok=TulJKNlR)](https://developers.redhat.com/sites/default/files/screenshot_2023-04-03_at_11.59.38.png)

Figure 2: The Groovy download page.



Figure 3 shows the three zip files that we will unzip in the next steps.

[![A screenshot of the zip files dowloaded for Debezium and Groovy.](https://developers.redhat.com/sites/default/files/styles/article_floated/public/screenshot_2023-04-03_at_12.04.20.png?itok=BuOaJxBH)](https://developers.redhat.com/sites/default/files/screenshot_2023-04-03_at_12.04.20.png)

Figure 3: The zip files dowloaded for Debezium and Groovy.





## Creating the image

Unzip the files dowloaded in the last step. Use the SQL server plugin, as shown in Figure 4.

[![A screenshot of the unzipped debezium and groovy folders.](https://developers.redhat.com/sites/default/files/styles/article_floated/public/screenshot_2023-04-03_at_12.09.15.png?itok=xrl0CNz0)](https://developers.redhat.com/sites/default/files/screenshot_2023-04-03_at_12.09.15.png)

Figure 4: The unzipped debezium and groovy folders.



Go to the **debezium-scripting** folder and copy the debezium-scripting-1.9.7.Final...jar and place it inside the **debezium-connector-sqlserver** folder.

Then go to the **groovy-4.0.11/lib** folder and copy the jars groovy-4.0.11.jar and groovy-jsr223-4.0.11.jar. Place them in the **debezium-connector-sqlserver** folder. At this point, your folder should look like Figure 5. Keep in mind that your versions may be different. These are the versions available at the time of this article.

[![A screenshot of the plugin folder with all the necessary jars.](https://developers.redhat.com/sites/default/files/styles/article_floated/public/screenshot_2023-04-03_at_12.07.52.png?itok=q0QC8EEG)](https://developers.redhat.com/sites/default/files/screenshot_2023-04-03_at_12.07.52.png)

Figure 5: The plugin folder with all the necessary jars.



Now, zip the debezium-connector-sqlserver folder and place this zip file into your nexus or Git. Then use this as your artifact, as shown in the previously mentioned Hugo Guerrero [article](https://developers.redhat.com/articles/2021/12/06/improve-your-kafka-connect-builds-debezium#).



## How to use transformations

To use this feature, create your Kafka connectors and configure them to use the transformations like the following:

```
kind: KafkaConnector
apiVersion: kafka.strimzi.io/v1beta2
metadata:
  name: sql-connector-for-inserts
  labels:
    strimzi.io/cluster: my-connect-cluster
  namespace: kafka
spec:
  class: io.debezium.connector.sqlserver.SqlServerConnector
  tasksMax: 1
  config:
    database.hostname: "server.earth.svc"
    database.port: "1433"
    database.user: "sa"
    database.password: "Password!"
    database.dbname: "InternationalDB"
    table.whitelist: "dbo.Orders"
    database.history.kafka.bootstrap.servers: "my-cluster-kafka-bootstrap:9092"
    database.server.name: "internation-db-insert-topic" <-- # This property need to have a unique value
    database.history.kafka.topic: "dbhistory.internation-db-insert-topic" <-- # This property need to have a unique value
    #### Here start the transforms feature, using the condition where operation is equal 'c', only 
    #### events of that type will be routed to the topic created by this connector.
    transforms: filter 
    transforms.filter.language: jsr223.groovy 
    transforms.filter.type: io.debezium.transforms.Filter 
    transforms.filter.condition: value.op == 'c'
    transforms.filter.topic.regex: internation-db-insert-topic.dbo.Orders\
    #### end of transforms filter
    tombstones.on.delete: 'false'
```