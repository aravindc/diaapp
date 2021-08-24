-- migrate:up
ALTER TABLE bg_log ALTER COLUMN entry_datetime TYPE timestamp with time zone;

-- migrate:down
ALTER TABLE bg_log ALTER COLUMN entry_datetime TYPE timestamp without time zone;
