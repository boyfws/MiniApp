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
       PRIMARY KEY
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
    house SMALLINT

    location GEOMETRY(POINT, 4326)
             NOT NULL, 
    PRIMARY KEY (city, district, street, house)
);






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
                SET address_id = (full_address.city, full_address.district, full_address.street, full_address.house)
                WHERE address_id = (empty_address.city, empty_address.district, empty_address.street, empty_address.house);

                -- Удаляем старый адрес с пустым district
                DELETE FROM address
                WHERE city = empty_address.city
                AND district = empty_address.district
                AND street = empty_address.street
                AND house = empty_address.house;

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