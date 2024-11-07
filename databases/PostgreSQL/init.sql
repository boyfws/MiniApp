-- Extensions
CREATE EXTENSION postgis;



-- Tables
CREATE TABLE log_actions (
    id SMALLINT 
       GENERATED ALWAYS AS IDENTITY 
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
    id SMALLINT 
       GENERATED ALWAYS AS IDENTITY 
       PRIMARY KEY,

    name 
    VARCHAR(20) -- Может измениться в будущем (посмотрим)
    UNIQUE 
    NOT NULL 
);

CREATE INDEX idx_categories_name ON categories USING HASH (name);



CREATE TABLE restaurants (
    id INTEGER 
       GENERATED ALWAYS AS IDENTITY 
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
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    adress JSONB NOT NULL, 

    categories SMALLINT[] NOT NULL, -- Формально массив внешних ключей для id categories

    CONSTRAINT photos_length_check CHECK (array_length(photos, 1) >= 3 AND array_length(photos, 1) <= 8),
    CONSTRAINT check_orig_phone_first_digit CHECK (LEFT(orig_phone, 1) = '7'), -- Стандартизируем хранение номеров
    CONSTRAINT check_wapp_phone_first_digit CHECK (LEFT(wapp_phone, 1) = '7')
);

    


CREATE TABLE user_activity_logs (
    id BIGINT 
       GENERATED ALWAYS AS IDENTITY 
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
    id INTEGER 
       GENERATED ALWAYS AS IDENTITY
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_city_name ON city USING HASH (name);




CREATE TABLE district (
    id INTEGER 
       GENERATED ALWAYS AS IDENTITY 
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_district_name ON district USING HASH (name);



CREATE TABLE street (
    id INTEGER 
       GENERATED ALWAYS AS IDENTITY 
       PRIMARY KEY,
    name VARCHAR(255)
         UNIQUE
         NOT NULL
);

CREATE INDEX idx_street_name ON street USING HASH (name);




CREATE TABLE address (
    id BIGINT 
       GENERATED ALWAYS AS IDENTITY 
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
            -- Улица может быть пустым но тогда он ссылается на пустую строку (Пользоавтелю для поиска достаточно города)
    house SMALLINT,

    location GEOGRAPHY(POINT, 4326)
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

CREATE INDEX idx_addresses_for_user_address_id ON addresses_for_user USING HASH (user_id);




-- Procedures 

CREATE OR REPLACE FUNCTION update_empty_districts(distance_threshold FLOAT)
RETURNS VOID AS $$
DECLARE
    empty_address RECORD;
    full_address RECORD;
BEGIN
    -- Начинаем транзакцию
    BEGIN
        -- Находим все адреса с пустым district и непустым street
        FOR empty_address IN (
            SELECT * FROM address
            WHERE district IN (
                SELECT id FROM district WHERE name = ''
            )
            AND street NOT IN (
                SELECT id FROM street WHERE name = ''
            )
        ) LOOP
            -- Находим соответствующий адрес с заполненным district
            FOR full_address IN (
                SELECT * FROM address
                WHERE district NOT IN (
                    SELECT id FROM district WHERE name = ''
                )
                AND ST_Distance(empty_address.location, location) <= distance_threshold
                AND city = empty_address.city
                AND street = empty_address.street
                AND house = empty_address.house
            ) LOOP
                -- Обновляем ссылки в таблице user_address
                UPDATE addresses_for_user
                SET address_id = full_address.id
                WHERE address_id = empty_address.id;

                -- Удаляем старый адрес с пустым district
                DELETE FROM address
                WHERE id = empty_address.id;

                -- Выходим из цикла, так как нашли соответствующий адрес
                EXIT;
            END LOOP;
        END LOOP;

        -- Фиксируем транзакцию
        COMMIT;
    EXCEPTION
        WHEN OTHERS THEN
            -- Откатываем транзакцию в случае ошибки
            ROLLBACK;
            RAISE;
    END;
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