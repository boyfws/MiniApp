CREATE USER backend WITH 
    PASSWORD '${BACKEND_PASSWORD}'
    CONNECTION LIMIT 1;
CREATE USER reader WITH 
    PASSWORD '${READER_PASSWORD}'
    CONNECTION LIMIT 10;

GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO backend;
GRANT CONNECT ON DATABASE "${TEST_DB_NAME}" TO backend;

GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO reader;
GRANT CONNECT ON DATABASE "${TEST_DB_NAME}" TO reader;
