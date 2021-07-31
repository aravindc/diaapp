-- migrate:up
CREATE TYPE food_qty_type AS ENUM ('g','kg','l','ml','nos');
CREATE TABLE food_carb (
    id UUID PRIMARY KEY,
    food_name varchar(255) NOT NULL,
    food_qty_type food_qty_type NOT NULL,
    food_qty numeric(10,2) NOT NULL,
    carb_count numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
)
-- migrate:down
DROP TABLE food_carb;
DROP TYPE food_qty_type;