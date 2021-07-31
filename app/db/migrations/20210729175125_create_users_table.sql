-- migrate:up
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email varchar(255) UNIQUE NOT NULL,
    hashed_password varchar(255) NOT NULL,
    is_active boolean NOT NULL DEFAULT FALSE,
    created_at timestamp with time zone DEFAULT now()
)

-- migrate:down
DROP TABLE users