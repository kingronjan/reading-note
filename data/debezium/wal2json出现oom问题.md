## 搭建测试环境

PG9.6:

dockerfile:

```Dockerfile
# FROM hub.rat.dev/postgres:9.6
FROM docker.xuanyuan.me/frodenas/postgresql:latest

# acording https://wiki.postgresql.org/wiki/Apt
# 旧版 Debian/Ubuntu 发行版的软件包已移至 https://apt-archive.postgresql.org
RUN sed -i 's/apt.p/apt-archive.p/g' /etc/apt/sources.list.d/pgdg.list

# install wal2json

# from https://askubuntu.com/questions/1065231/dpkg-deb-error-archive-has-premature-member-control-tar-xz-before-contr
# if error like this:
# dpkg-deb: error: archive ... has premature member 'control.tar.xz' before 'control.tar.gz', giving up
# add 
# RUN apt-get clean && \
#    apt-get update && \
#    apt-get install dpkg

RUN apt-get update
RUN apt-get install -f -y --no-install-recommends postgresql-9.6-wal2json

# default
ENV PG_OPTIONS='-c wal_level=logical -c max_wal_senders=10 -c max_replication_slots=10'

# supoort PG_OPTIONS
RUN sed '$s/$/ \$PG_OPTIONS/' /scripts/run.sh
```

build:
```shell
docker build -t pg96-wal2json:1.0.0 .
```


验证 wal2json 是否安装：

```sql
SELECT * FROM pg_create_logical_replication_slot('my_wal2json_slot', 'wal2json');
```


docker compose 配置：

```yaml
# docker-compose.yml
services:
  postgres:
    image: pg96-wal2json:1.0.0
    container_name: postgres
    ports:
      - "5432:5432"
    volumes:
      - /home/kingron/data/postgres:/data
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
      - PGDATA=/data
    restart: always

  kafka:
    image: hub.rat.dev/apache/kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_PROCESS_ROLES: 'broker,controller'
      KAFKA_NODE_ID: 1
      KAFKA_LISTENERS: 'PLAINTEXT://:9092,CONTROLLER://:9093'
      KAFKA_ADVERTISED_LISTENERS: 'PLAINTEXT://kafka:9092'
      KAFKA_CONTROLLER_LISTENER_NAMES: 'CONTROLLER'
      KAFKA_INTER_BROKER_LISTENER_NAME: 'PLAINTEXT'
      KAFKA_CONTROLLER_QUORUM_VOTERS: '1@kafka:9093'
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: '1'
      CLUSTER_ID: '5L6g3nShT-eMCtK--X86sw'
      KAFKA_LOG_DIRS: '/tmp/kafka-logs'

  debezium:
    image: hub.rat.dev/debezium/connect:1.9.7.Final
    container_name: debezium
    ports:
      - "8083:8083"
    depends_on:
      - kafka
      - postgres
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: 1
      CONFIG_STORAGE_TOPIC: my_connect_configs
      OFFSET_STORAGE_TOPIC: my_connect_offsets
      STATUS_STORAGE_TOPIC: my_connect_statuses
```

修改用户密码：

```shell
docker exec postgres psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres';"
```

配置用户 replication 权限：

```shell
docker exec postgres /bin/sh -c "echo 'host    replication     postgres        0.0.0.0/0           md5' >> /data/pg_hba.conf"
# 配置后需要重启
docker exec -u postgres postgres /usr/lib/postgresql/9.6/bin/pg_ctl reload -D /data 
```


## 测试数据

```sql
CREATE TABLE large_object_table (
    id SERIAL PRIMARY KEY,
    data TEXT
);

-- debezium 建立后写入数据
INSERT INTO large_object_table (data) SELECT repeat('a', 1024 * 1024 * 1000);
```


debezium 配置：

```json
{
    "name": "pg-wal2json-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "database.hostname": "postgres",
        "database.port": "5432",
        "database.user": "postgres",
        "database.password": "postgres",
        "database.dbname": "postgres",
        "database.server.name": "pgserver1000",
        "table.include.list": "public.large_object_table",
        "plugin.name": "wal2json",
        "transforms": "route",
        "transforms.route.type": "io.debezium.transforms.ByLogicalTableRouter",
        "transforms.route.topic.regex": "pgserver1000\.public\.(.*)",
        "transforms.route.topic.replacement": "all_postgres_changes"
    }
}
```


## 参考

- [在 Amazon RDS 上使用 PostgreSQL 运行 Debezium 的经验教训](https://debezium.io/blog/2020/02/25/lessons-learned-running-debezium-with-postgresql-on-rds/)