-- migrate:up
ALTER TABLE food_carb ADD COLUMN food_name_id VARCHAR(50) UNIQUE;

-- migrate:down
ALTER TABLE food_carb DROP COLUMN food_name_id;
