-- Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;



-- Tables
CREATE TABLE log_actions (
    id SMALLSERIAL 
       PRIMARY KEY,

    description VARCHAR(255) 
                UNIQUE
                NOT NULL
);



CREATE TABLE users (
    id BIGINT 
       PRIMARY KEY,
    owner BOOLEAN
    NOT NULL
    DEFAULT FALSE
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
            REFERENCES users(id)
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



CREATE TABLE user_activity_logs (
    id BIGSERIAL 
       PRIMARY KEY,

    user_id BIGINT 
            REFERENCES users(id)
            ON DELETE RESTRICT -- Доп защита, так как удалние пользоавтелей не предусмотрено 
            ON UPDATE RESTRICT
            NOT NULL,

    log_time BIGINT 
             NOT NULL, -- UNIX timestamp GMT+0

    action_id SMALLINT 
              REFERENCES log_actions(id) 
              ON DELETE RESTRICT  -- Доп защита, так как удалние действий - рекдая операция, меняющая систему и необходимо вручную очистить логи
              ON UPDATE RESTRICT
              NOT NULL,

    cat_link SMALLINT 
             REFERENCES categories(id)
             ON DELETE RESTRICT -- Доп защита, так как удалние категорий - рекдая операция, меняющая систему и необходимо вручную очистить логи
             ON UPDATE RESTRICT,

    restaurant_link INTEGER 
                    REFERENCES restaurants(id) 
                    ON DELETE CASCADE
                    ON UPDATE RESTRICT
);




CREATE TABLE city (
    id SERIAL 
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_city_name ON city USING HASH (name);




CREATE TABLE district (
    id SERIAL 
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_district_name ON district USING HASH (name);



CREATE TABLE street (
    id SERIAL  
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_street_name ON street USING HASH (name);




-- !!! IMPORTANT NOTE: Тут может возникнуть ситуация что при пустом district 
-- при одинаковых city street и house будут разные location. Это необходимо учитывать 
-- при добавлении ссылки в таблицу addresses_for_user. Ппри нахождении нескольких id 
-- с одинаковыми парметрами city, street, house и пустым district необходимо сверить еще и локацию.
-- Для быстрого поиска и вставки id в таблицу addresses_for_user строится индекс на наборе  
-- (city, district, street, house)
CREATE TABLE address (
    id BIGSERIAL 
       PRIMARY KEY,

    city INTEGER
         REFERENCES city(id)
         ON DELETE RESTRICT
         ON UPDATE RESTRICT
         NOT NULL,

    district INTEGER                              
             REFERENCES district(id) 
             ON DELETE RESTRICT
             ON UPDATE RESTRICT
             NOT NULL,
             -- Район может быть пустым но тогда он ссылается на пустую строку (API модет возрашать пустой район)

    street INTEGER 
           REFERENCES street(id)
           ON DELETE RESTRICT
           ON UPDATE RESTRICT
           NOT NULL,
            -- Улица может быть пустой но тогда она ссылается на пустую строку (Пользоавтелю для поиска достаточно города)
    house SMALLINT,

    location GEOGRAPHY(POINT, 4326) --lon lat
             NOT NULL 
);

-- B-tree index 
CREATE INDEX idx_address_composite ON address (city, district, street, house);



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

CREATE INDEX idx_addresses_for_user_address_id ON addresses_for_user USING HASH (user_id);



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

CREATE INDEX idx_fav_cat_for_user_user_id ON fav_cat_for_user USING HASH (user_id);



CREATE TABLE fav_rest_for_user (
    user_id BIGINT 
            REFERENCES users(id)
            ON DELETE RESTRICT 
            ON UPDATE RESTRICT
            NOT NULL,

    rest_id INTEGER 
            REFERENCES restaurants(id)
            ON DELETE RESTRICT
            ON UPDATE RESTRICT
            NOT NULL,
    PRIMARY KEY (user_id, rest_id)
);

CREATE INDEX idx_fav_rest_for_user_user_id ON fav_rest_for_user USING HASH (user_id);



-- Procedures 

CREATE OR REPLACE PROCEDURE update_empty_districts(distance_threshold FLOAT)
AS $$
DECLARE
    empty_address RECORD;
    full_address RECORD;
BEGIN
    -- Находим все адреса с пустым district и непустым street
    FOR empty_address IN (SELECT * FROM address WHERE 
                            district = (
                                       SELECT id FROM district WHERE name = '' -- Обязательно должны существовать эти элемент
                                       )
                            AND 
                            street != (
                                      SELECT id FROM street WHERE name = '' -- Обязательно должны существовать эти элементы 
                                      ) 
                            -- Значения точно уникальны (исходя из условий в street, district)
                        ) 
    LOOP
            -- Находим соответствующий адрес с заполненным district
        FOR full_address IN (SELECT * FROM address WHERE 
                                district != (
                                            SELECT id FROM district WHERE name = ''
                                            )
                                -- Значение точно уникально
                                AND 
                                ST_Distance(empty_address.location, location) <= distance_threshold
                                AND 
                                city = empty_address.city
                                AND 
                                street = empty_address.street
                                AND 
                                house = empty_address.house
                            ) 
        LOOP
                -- Обновляем ссылки в таблице user_address
            UPDATE addresses_for_user
            SET address_id = full_address.id
            WHERE address_id = empty_address.id;

             -- Удаляем старый адрес с пустым district
            DELETE FROM address
            WHERE id = empty_address.id;

        END LOOP;


    END LOOP;
END;
$$ LANGUAGE plpgsql;




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



-- Users
CREATE USER backend WITH PASSWORD '${BACKEND_PASSWORD}';
CREATE USER clearing_trigger WITH PASSWORD '${CLEARING_TRIGGER_PASSWORD}';
CREATE USER logger WITH PASSWORD '${LOGGER_PASSWORD}';
CREATE USER reader WITH PASSWORD '${READER_PASSWORD}';



-- Roots
 -- backend
-- Разрешение на подключение и использоавние 
GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO backend;
-- Сначала отзываем все права потом даем права на работу с данными, но не даем менять структуру
REVOKE ALL ON SCHEMA public FROM backend;
GRANT USAGE ON SCHEMA public TO backend;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO backend;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO backend;

 --clearing_trigger
-- Даем права на подключение и процедуру
GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO clearing_trigger;
GRANT EXECUTE ON PROCEDURE update_empty_districts(FLOAT) TO clearing_trigger;
-- Даем права на обновление и удаление для выполнение процедуры
GRANT SELECT, UPDATE, DELETE ON address TO clearing_trigger;
GRANT SELECT, UPDATE ON addresses_for_user TO clearing_trigger;
GRANT SELECT ON district TO clearing_trigger;
GRANT SELECT ON street TO clearing_trigger;

 --logger
GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO logger;
-- Даем права для записей логов и выборки данных для удобства записи 
GRANT INSERT ON user_activity_logs TO logger;
GRANT SELECT ON users TO logger;
GRANT SELECT ON log_actions TO logger;
GRANT SELECT ON categories TO logger;
GRANT SELECT ON restaurants TO logger;

 --reader
GRANT CONNECT ON DATABASE "${POSTGRES_DB}" TO reader;
-- Предоставление прав на чтение всех таблиц в базе данных
GRANT USAGE ON SCHEMA public TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
-- Для будущих таблиц, чтобы права на чтение автоматически предоставлялись
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO reader;



-- Insertions
---!!!! City всегда непустой 
INSERT INTO district (name) VALUES ('');
INSERT INTO street (name) VALUES ('');

INSERT INTO categories (name) VALUES 
('Бургеры'),
('Суши'),
('Пицца'),
('Паста'),
('Десерты');
-- !!! Добавим допом чуть больше 