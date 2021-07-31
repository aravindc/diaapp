-- migrate:up
CREATE TYPE insulin_type AS ENUM ('rapid_insulin_food', 'rapid_insulin_correction', 'long_acting_insulin');
CREATE TABLE bg_log (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    entry_datetime TIMESTAMP NOT NULL,
    bg_level Numeric(10, 2) NOT NULL,
    insulin_qty Numeric(10, 2) NOT NULL,
    insulin_type insulin_type NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);

-- migrate:down
DROP TABLE bg_log;
DROP TYPE insulin_type;
