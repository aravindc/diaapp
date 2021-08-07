-- migrate:up
ALTER TABLE food_carb ADD food_image_url VARCHAR(1024);
ALTER TABLE food_carb ADD user_id UUID REFERENCES users(id);

-- migrate:down
ALTER TABLE food_carb DROP food_image_url;
ALTER TABLE food_carb DROP user_id;