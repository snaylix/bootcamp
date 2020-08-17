DROP TABLE IF EXISTS cities;
-- Drop table if it already exists

CREATE TABLE cities (
  id SERIAL PRIMARY KEY NOT NULL, -- name, data type, contraints. PK = unique!
  -- SERIAL automatically incremented integer
  name VARCHAR(50) NOT NULL,
  population INTEGER NOT NULL, -- 2^32
  country VARCHAR(50) NOT NULL
);

INSERT INTO cities (name, population, country)
VALUES ('Berlin', 3800000, 'Germany');
INSERT INTO cities (name, population, country)
VALUES ('Paris', 2200000, 'France');
INSERT INTO cities (name, population, country)
VALUES ('New York City', 8800000, 'USA');
