-- migrate:up
CREATE TYPE food_type AS ENUM ('breakfast', 'lunch', 'dinner', 'snacks');
CREATE TABLE food_log(
    id UUID PRIMARY KEY,
    entry_datetime TIMESTAMP NOT NULL,
    food_type food_type NOT NULL,
    food_carb_id UUID NOT NULL,
    user_id UUID NOT NULL,
    created_at timestamp with time zone DEFAULT now()
  );
ALTER TABLE food_log ADD CONSTRAINT food_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE food_log ADD CONSTRAINT food_log_food_carb_id_fkey FOREIGN KEY (food_carb_id) REFERENCES food_carb(id);
-- migrate:down
ALTER TABLE food_log DROP CONSTRAINT food_log_user_id_fkey;
ALTER TABLE food_log DROP CONSTRAINT food_log_food_carb_id_fkey;
DROP TABLE food_log;
DROP TYPE food_type;
