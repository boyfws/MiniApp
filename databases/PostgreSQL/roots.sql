-- Пользоавтели уже созданы до этого 


-- Roots
 -- backend
GRANT USAGE ON SCHEMA public TO backend;

GRANT 
    SELECT 
ON 
    public.categories
TO backend;

GRANT INSERT, DELETE, SELECT ON 
    public.fav_rest_for_user, 
    public.fav_cat_for_user,
    public.addresses_for_user 
TO backend;

GRANT 
    SELECT, 
    INSERT 
ON 
    public.address,
    public.region,
    public.district, 
    public.street, 
    public.city
TO backend;

GRANT 
    INSERT, 
    DELETE, 
    UPDATE, 
    SELECT 
ON 
    public.restaurants 
    public.owner
TO backend;

GRANT 
    SELECT,
    INSERT,
    UPDATE
ON 
    public.users
TO backend;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO backend;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO backend;

-- Если мы находимся в тестовой базе, даем доступ бэку на последоавтельности для удобства тестов 
DO $$
DECLARE
    TEST_DB_NAME TEXT := '${TEST_DB_NAME}';
BEGIN
    IF current_database() = TEST_DB_NAME THEN
        GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO backend;
        GRANT TRUNCATE ON ALL TABLES IN SCHEMA public TO backend;



        RAISE NOTICE 'Выданы доп права пользователю backend';
    ELSE 
        RAISE NOTICE 'Доп права пользователю backend не были выданы';
    END IF;
END $$;


 --reader
GRANT USAGE ON SCHEMA public TO reader;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
-- Для будущих таблиц, чтобы права на чтение автоматически предоставлялись
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO reader;