INSERT INTO categories (name) VALUES
('Русская кухня'),
('Азиатская кухня'),
('Европейская кухня'),
('Американская кухня'),
('Итальянская кухня');


INSERT INTO users (id) VALUES
(1),
(2),
(3),
(4),
(5);


INSERT INTO city (name) VALUES
('Москва'),
('Санкт-Петербург'),
('Новосибирск'),
('Екатеринбург'),
('Нижний Новгород');


INSERT INTO district (name) VALUES
('Московский'),
('Санкт-Петербургский'),
('Новосибирский'),
('Екатеринбургский');


INSERT INTO street (name) VALUES
('Полежаевская'),
('Спортивная'),
('Мира'),
('Пушкина');


INSERT INTO fav_cat_for_user (user_id, cat_id) VALUES 
(1, 1),
(1, 2);


INSERT INTO address (city, district, street, house, location) VALUES
(2, 3, 2, 2, ST_SetSRID(ST_MakePoint(37.617,55.755), 4326)),
(3, 4, 3, 3, ST_SetSRID(ST_MakePoint(37.617,55.755), 4326)),
(4, 5, 4, 4, ST_SetSRID(ST_MakePoint(37.617,55.755), 4326)),
(5, 5, 5, 5, ST_SetSRID(ST_MakePoint(37.617,55.755), 4326)),
(5, 1, 5, 5, ST_SetSRID(ST_MakePoint(37.617,55.755), 4326)); -- Для теста процедуры


INSERT INTO addresses_for_user (user_id, address_id) VALUES 
(2, 5), 
(3, 5),
(1, 1);


INSERT INTO restaurants (name, owner_id, address, main_photo, photos, categories) VALUES 
('Ресторан 3', 
1,   
'{
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [125.6, 10.1]
    },
    "properties": {
      "name": "Dinagat Islands"
    }
}'::JSONB,
'https://example.com/main_photo.jpg',
ARRAY[
  'https://example.com/photo1.jpg', 
  'https://example.com/photo2.jpg', 
  'https://example.com/photo3.jpg'
  ],  
ARRAY[1, 2, 3]
);


CALL update_empty_districts(0.5);


---  Error о том, что нет такой категории 
INSERT INTO restaurants (name, owner_id, address, main_photo, photos, categories) VALUES
('Ресторан 4', 
2,   
'{
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [125.6, 10.1]
    },
    "properties": {
      "name": "Dinagat Islands"
    }
}'::JSONB,
'https://example.com/main_photo.jpg',
ARRAY[
  'https://example.com/photo1.jpg', 
  'https://example.com/photo2.jpg', 
  'https://example.com/photo3.jpg'
  ],  
ARRAY[1, 2, 100]
);


---  Error о том, что передан неправильный формат JSON 
INSERT INTO restaurants (name, owner_id, address, main_photo, photos, categories) VALUES
('Ресторан 5', 
3,   
'{
    "type": "Feature",
    "properties": {
      "name": "Dinagat Islands"
    }
}'::JSONB,
'https://example.com/main_photo.jpg',
ARRAY[
  'https://example.com/photo1.jpg', 
  'https://example.com/photo2.jpg', 
  'https://example.com/photo3.jpg'
  ],  
ARRAY[1, 2]
);


-- Error о том, что нельзя обновить категории
UPDATE restaurants
SET categories = categories || ARRAY[100]
WHERE id = 1;


--- Error о том, что нельзя удалить так как на категорию ссылаются 
DELETE FROM categories WHERE id == 1;





