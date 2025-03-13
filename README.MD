## Real-Time Pipeline
Data engineering project that takes data provided by a Kafka cluster, cleans it and uploads it to a database.


`python3 realtime_pipeline.py` To run the project. To enable logging `-l` or `--log` can be added

`database.py` Contains methods for connecting to the database and uploading data

`bash clear_tables.sh` Clears data from the tables (but does not remake them)

`lmnh_schema.sql` Defines the database Schema and provides seed data - Specific for LMNH

`test_realtime_pipeline.py` Contains tests for `realtime_pipeline.py`

`.env` is required and should consist of:

```
BOOTSTRAP_SERVERS=<KAFKA_SERVER:PORT>
SECURITY_PROTOCOL=<KAFKA PROTOCOL>>
SASL_MECHANISM=PLAIN
USERNAME_KAFKA=<KAFKA_USERNAME>
PASSWORD=<KAFKA_PASSWORD>
GROUP_ID=<GROUP_NAME_HERE>

DB_HOST=<DATABASE_HOST_URL>
DB_USERNAME=<DATABASE_USER>
DB_PASSWORD=<DATABASE_PASSWORD>
DB_NAME=<DATABASE_NAME>
DB_PORT=<DATABASE_PORT>
```