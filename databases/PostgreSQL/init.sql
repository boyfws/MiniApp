-- Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;



-- Tables
CREATE TABLE owners (
    id BIGINT 
    PRIMARY KEY
    -- Выносим как отдельную сущность так как может понадобиться доп инфа специфичная для владельца в будущем 
);



CREATE TABLE users (
    id BIGINT 
       PRIMARY KEY
);


 
CREATE TABLE categories (
    id SMALLSERIAL 
       PRIMARY KEY,

    name 
    VARCHAR(20) -- Может измениться в будущем (посмотрим)
    UNIQUE 
    NOT NULL 
);

CREATE INDEX idx_categories_name ON categories USING HASH (name);



CREATE TABLE restaurants (
    id SERIAL 
       PRIMARY KEY,
    owner_id BIGINT 
            REFERENCES owners(id)
            ON DELETE RESTRICT -- Доп защита, так как удалние пользоавтелей не предусмотрено
            ON UPDATE RESTRICT
            NOT NULL,

    name VARCHAR(100) -- Бизнесовое ограничениие, более 100 символов неудобно 
         NOT NULL,
    main_photo VARCHAR(1000) --Ссылка на фото для главной страницы 
               NOT NULL,
    photos VARCHAR(1000)[] -- Ссылка на фото ресторана 
           NOT NULL, 
    -- Ссылки на ресторан в другом сервисе 
    ext_serv_link_1 VARCHAR(1000), 
    ext_serv_link_2 VARCHAR(1000), 
    ext_serv_link_3 VARCHAR(1000),
    -- Оценки ресторана в дрругом сервисе
    ext_serv_rank_1 NUMERIC(3, 2),
    ext_serv_rank_2 NUMERIC(3, 2),
    ext_serv_rank_3 NUMERIC(3, 2),
    -- Количество отзывов в другом сервисе
    ext_serv_reviews_1 INTEGER,
    ext_serv_reviews_2 INTEGER,
    ext_serv_reviews_3 INTEGER,
    -- Ссылки на соц сети
    tg_link VARCHAR(1000),
    inst_link VARCHAR(1000),
    vk_link VARCHAR(1000),

    -- Номера телефона 
    orig_phone VARCHAR(11), -- ру номера 
    wapp_phone VARCHAR(11),

    -- Адрес ресторана
    location GEOGRAPHY(POINT, 4326), --lon lat
    address JSONB NOT NULL, 

    categories SMALLINT[] NOT NULL, -- Формально массив внешних ключей для id categories

    CONSTRAINT photos_length_check CHECK (array_length(photos, 1) >= 3 AND array_length(photos, 1) <= 8),
    CONSTRAINT check_orig_phone_first_digit CHECK (LEFT(orig_phone, 1) = '7'), -- Стандартизируем хранение номеров
    CONSTRAINT check_wapp_phone_first_digit CHECK (LEFT(wapp_phone, 1) = '7')
);

CREATE INDEX idx_gin_name_search ON restaurants USING GIN (name gin_trgm_ops);
CREATE INDEX idx_location_search On restaurants USING SPGiST (location);



CREATE TABLE city (
    id SERIAL 
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);



CREATE TABLE district (
    id BIGSERIAL 
       PRIMARY KEY,
    city_id INTEGER 
            REFERENCES city(id)
            NOT NULL,
    name VARCHAR(255),
    CONSTRAINT district_city_name_unique_comb UNIQUE (city_id, name)
);


CREATE TABLE street (
    id BIGSERIAL  
       PRIMARY KEY,
    district_id BIGINT
                REFERENCES district(id)
                ON UPDATE CASCADE,
    name VARCHAR(255)
    -- Ограничение не накалдывается, так как если район undefined может
    -- возникинуть ситуация при которой, есть две динаковые улица    
);

CREATE INDEX idx_street_name ON street(name);



CREATE TABLE address (
    id BIGSERIAL 
       PRIMARY KEY,
    street_id BIGINT 
              REFERENCES street(id)
              NOT NULL,
    house SMALLINT,

    location GEOGRAPHY(POINT, 4326) --lon lat
             NOT NULL 
);


CREATE TABLE addresses_for_user (
    user_id BIGINT 
            REFERENCES users(id)
            ON DELETE RESTRICT -- Доп защита, так как удалние пользоавтелей не предусмотрено
            ON UPDATE RESTRICT
            NOT NULL,

    address_id BIGINT 
               REFERENCES address(id)
               ON DELETE RESTRICT
               ON UPDATE RESTRICT
               NOT NULL,

    PRIMARY KEY (user_id, address_id)
);



CREATE TABLE fav_cat_for_user (
    user_id BIGINT 
            REFERENCES users(id)
            ON DELETE RESTRICT 
            ON UPDATE RESTRICT
            NOT NULL,

    cat_id SMALLINT 
          REFERENCES categories(id)
          ON DELETE RESTRICT
          ON UPDATE RESTRICT
          NOT NULL,
    PRIMARY KEY (user_id, cat_id)
);



CREATE TABLE fav_rest_for_user (
    user_id BIGINT 
            REFERENCES users(id)
            ON DELETE RESTRICT 
            ON UPDATE RESTRICT
            NOT NULL,

    rest_id INTEGER 
            REFERENCES restaurants(id)
            ON DELETE CASCADE
            ON UPDATE RESTRICT
            NOT NULL,
    PRIMARY KEY (user_id, rest_id)
);



-- Triggers 

-- Триггер для проверки наличия категорий в таблице categories перед вставкой или обновлением каегории в массив внутри restaurants
CREATE OR REPLACE FUNCTION check_categories() RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, что все идентификаторы в массиве categories существуют в таблице categories
    IF EXISTS (
        SELECT 1
        FROM unnest(NEW.categories) AS category_id
        WHERE category_id NOT IN (SELECT id FROM categories)
    ) THEN
        RAISE EXCEPTION 'One or more category_ids do not exist in the categories table';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_categories_trigger
BEFORE INSERT OR UPDATE ON restaurants
FOR EACH ROW
EXECUTE FUNCTION check_categories();



-- Функция для проверки на удаление категории
CREATE OR REPLACE FUNCTION prevent_category_deletion() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM restaurants
        WHERE OLD.id = ANY(categories)
    ) THEN
        RAISE EXCEPTION 'Cannot delete category because it is referenced by one or more restaurants';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_category_deletion_trigger
BEFORE DELETE ON categories
FOR EACH ROW
EXECUTE FUNCTION prevent_category_deletion();



-- Функция для проверки на изменение категории
CREATE OR REPLACE FUNCTION prevent_category_update() RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, ссылаются ли какие-либо рестораны на изменяемую категорию
    IF EXISTS (
        SELECT 1
        FROM restaurants
        WHERE OLD.id = ANY(categories)
    ) THEN
        RAISE EXCEPTION 'Cannot update category because it is referenced by one or more restaurants';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_category_update_trigger
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION prevent_category_update();



-- Автораспаковка адреса
CREATE OR REPLACE FUNCTION update_location()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка наличия ключей в JSONB
    IF NEW.address ? 'geometry' AND NEW.address->'geometry' ? 'coordinates' THEN
        -- Проверка типа данных координат
        IF jsonb_typeof(NEW.address->'geometry'->'coordinates') = 'array' THEN
            -- Проверка наличия двух элементов в массиве координат
            IF jsonb_array_length(NEW.address->'geometry'->'coordinates') = 2 THEN
                -- Извлечение координат и преобразование в тип float
                NEW.location := ST_SetSRID(ST_MakePoint(
                    (NEW.address->'geometry'->'coordinates'->>0)::float,
                    (NEW.address->'geometry'->'coordinates'->>1)::float
                ), 4326);
            ELSE
                RAISE EXCEPTION 'Координаты должны быть массивом из двух элементов';
            END IF;
        ELSE
            RAISE EXCEPTION 'Координаты должны быть массивом';
        END IF;
    ELSE
        RAISE EXCEPTION 'JSONB должен содержать ключи "geometry" и "coordinates"';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_location
BEFORE INSERT OR UPDATE ON restaurants
FOR EACH ROW
EXECUTE FUNCTION update_location();



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
TO backend;

GRANT 
    SELECT,
    INSERT,
    UPDATE
ON 
    public.users
TO backend;


-- Если мы находимся в тестовой базе, даем доступ бэку на последоавтельности для удобства тестов 
DO $$
BEGIN
    IF current_database() = '${TEST_DB_NAME}' THEN
        GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO backend;
        GRANT TRUNCATE ON ALL TABLES IN SCHEMA public TO backend;
    END IF;
END $$;


 --reader
GRANT USAGE ON SCHEMA public TO reader;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
-- Для будущих таблиц, чтобы права на чтение автоматически предоставлялись
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO reader;



-- Insertions
INSERT INTO categories (name) VALUES 
('Бургеры'),
('Суши'),
('Пицца'),
('Паста'),
('Десерты');
-- !!! Добавим допом чуть больше 