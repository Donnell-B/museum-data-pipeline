source .env

psql -h $DB_HOST -d $DB_NAME -p $DB_PORT -U $DB_USERNAME << EOF
TRUNCATE TABLE request_interaction;
TRUNCATE TABLE rating_interaction;
EOF
