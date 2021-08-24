-- migrate:up
CREATE TYPE food_type AS ENUM ('breakfast', 'lunch', 'dinner', 'snacks');
CREATE TABLE food_log(
    id UUID PRIMARY KEY,
    entry_datetime TIMESTAMP NOT NULL,
    food_type food_type NOT NULL,
    food_carb_id UUID REFERENCES food_carb(id) NOT NULL,
    food_qty numeric(10,2) NOT NULL,
    carb_count numeric(10,2) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    client_id UUID REFERENCES clients(id) ON DELETE CASCADE,
    created_at timestamp with time zone DEFAULT now()
  );

-- migrate:down
DROP TABLE food_log;
DROP TYPE food_type;
