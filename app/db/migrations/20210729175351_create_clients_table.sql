-- migrate:up
CREATE TYPE diabetes_type AS ENUM ('type1', 'type2');
CREATE TYPE bg_reading_type AS ENUM ('mmol/l', 'mg/dl');
CREATE TABLE clients (
  id UUID PRIMARY KEY,
  first_name varchar(255),
  last_name varchar(255),
  date_of_birth date,
  diabetes_type diabetes_type,
  bg_reading_type bg_reading_type,
  created_at timestamp with time zone DEFAULT now()
)
-- migrate:down
DROP TABLE clients;
DROP TYPE diabetes_type;
DROP TYPE bg_reading_type;