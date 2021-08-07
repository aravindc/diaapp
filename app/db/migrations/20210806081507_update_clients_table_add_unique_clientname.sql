-- migrate:up
ALTER TABLE clients ADD client_name VARCHAR(50) UNIQUE;

-- migrate:down
ALTER TABLE clients DROP client_name;
