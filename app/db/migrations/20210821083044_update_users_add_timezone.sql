-- migrate:up
ALTER TABLE users ADD COLUMN user_tz VARCHAR(255) NOT NULL DEFAULT 'UTC';

-- migrate:down
ALTER TABLE users DROP COLUMN user_tz;
