-- migrate:up
CREATE TYPE ratio_type AS ENUM ('same', 'time_range');
CREATE TABLE carb_ratio (
    id UUID PRIMARY KEY,
    client_id UUID REFERENCES clients(id) NOT NULL ,
    ratio_type ratio_type NOT NULL,
    carb_ratio Numeric(10, 2) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    insulin_sensitivity Numeric(10, 2) NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);

-- migrate:down
DROP TABLE carb_ratio;
DROP TYPE ratio_type;