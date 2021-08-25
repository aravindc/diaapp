-- migrate:up
ALTER TABLE carb_ratio ALTER COLUMN start_time TYPE varchar(8);
ALTER TABLE carb_ratio ALTER COLUMN end_time TYPE varchar(8);

-- migrate:down
ALTER TABLE carb_ratio ALTER COLUMN start_time TYPE time;
ALTER TABLE carb_ratio ALTER COLUMN end_time TYPE time;
