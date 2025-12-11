### How to enlarge the maximum size of the message delivered to Kafka?

From: [Frequently Asked Questions](https://debezium.io/documentation/faq/#how_to_enlarge_the_maximum_size_of_the_message_delivered_to_kafka)

For large transactions it is possible that Kafka Connect emits message that is larger then the pre-set maximum. The log usually contains an exception similar to:

```
org.apache.kafka.common.errors.RecordTooLargeException: The message is 1740572 bytes when serialized which is larger than 1048576, which is the value of the max.request.size configuration.
```

To solve the issue the configuration option `producer.max.request.size` must be set in Kafka Connect worker config file `connect-distributed.properties`. If the global change is not desirable then the connector can override the default setting using configuration option `producer.override.max.request.size` set to a larger value.

In the latter case it is also necessary to configure `connector.client.config.override.policy=ALL` option in Kafka Connect worker config file `connect-distributed.properties`. For Debezium `connect` Docker image the environment variable `CONNECT_CONNECTOR_CLIENT_CONFIG_OVERRIDE_POLICY` can be used to configure the option.



#### See also:  [spring - org.apache.kafka.common.errors.RecordTooLargeException: The request included a message larger than the max message size the server will accept - Stack Overflow](https://stackoverflow.com/questions/55181375/org-apache-kafka-common-errors-recordtoolargeexception-the-request-included-a-m)

By default,Kafka accepts a message of size 1 MB. The size of your message is more than default size.

You need to change the value of the property max.request.size,message.max.bytes and max.partition.fetch.bytes to fix this issue.

Find the kafka server configuration file 'server.properties' in your system. In Ubuntu, look for the '/etc/systemd/system/kafka.service' file to get the path of 'server.properties'. Open the 'server.properties' file and add the lines below and restart kafka service to increase the message size to ~25MB.

```ini
buffer.memory=200000000
max.request.size=200000000
message.max.bytes=200000000
max.partition.fetch.bytes=200000000
```

**Note:** Add `buffer.memory` config to avoid error like "the message is xxx bytes when serialized which is larger than the total memory buffer you have configured with the buffer.memory configuration." (from: [java - RecordTooLargeException in kafka - Stack Overflow](https://stackoverflow.com/questions/63528508/recordtoolargeexception-in-kafka))

Then restart the kafka server.



#### See alse: [apache zookeeper - How to restart kafka server properly? - Stack Overflow](https://stackoverflow.com/questions/51428465/how-to-restart-kafka-server-properly)

Otherwise, you can stop your broker using

```bash
./bin/kafka-server-stop.sh
```

and re-start it:

```bash
./bin/kafka-server-start.sh config/server.properties

# Or use '-daemon' for background serve.
./bin/kafka-server-start.sh -daemon config/server.properties
```
