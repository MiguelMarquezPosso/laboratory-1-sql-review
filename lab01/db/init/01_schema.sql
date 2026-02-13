CREATE TABLE IF NOT EXISTS country (
  country_id SMALLINT PRIMARY KEY,
  country VARCHAR(50) NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS city (
  city_id SMALLINT PRIMARY KEY,
  city VARCHAR(50) NOT NULL,
  country_id SMALLINT NOT NULL REFERENCES country(country_id),
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS address (
  address_id INTEGER PRIMARY KEY,
  address VARCHAR(50) NOT NULL,
  address2 VARCHAR(50),
  district VARCHAR(50) NOT NULL,
  city_id SMALLINT NOT NULL REFERENCES city(city_id),
  postal_code VARCHAR(20),
  phone VARCHAR(20),
  location BYTEA,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS store (
  store_id SMALLINT PRIMARY KEY,
  manager_staff_id SMALLINT NOT NULL,
  address_id INTEGER NOT NULL REFERENCES address(address_id),
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS staff (
  staff_id SMALLINT PRIMARY KEY,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  address_id INTEGER NOT NULL REFERENCES address(address_id),
  picture BYTEA,
  email VARCHAR(50),
  store_id SMALLINT NOT NULL REFERENCES store(store_id),
  active SMALLINT NOT NULL,
  username VARCHAR(16) NOT NULL,
  password VARCHAR(40),
  last_update TIMESTAMP NOT NULL
);

ALTER TABLE store
  ADD CONSTRAINT fk_store_manager_staff
  FOREIGN KEY (manager_staff_id) REFERENCES staff(staff_id);

CREATE TABLE IF NOT EXISTS customer (
  customer_id INTEGER PRIMARY KEY,
  store_id SMALLINT NOT NULL REFERENCES store(store_id),
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(50),
  address_id INTEGER NOT NULL REFERENCES address(address_id),
  active SMALLINT NOT NULL,
  create_date TIMESTAMP NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS language (
  language_id SMALLINT PRIMARY KEY,
  name VARCHAR(20) NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS film (
  film_id INTEGER PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  release_year SMALLINT,
  language_id SMALLINT NOT NULL REFERENCES language(language_id),
  original_language_id SMALLINT REFERENCES language(language_id),
  rental_duration SMALLINT NOT NULL,
  rental_rate NUMERIC(4,2) NOT NULL,
  length SMALLINT,
  replacement_cost NUMERIC(5,2) NOT NULL,
  rating VARCHAR(10),
  special_features VARCHAR(255),
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS actor (
  actor_id INTEGER PRIMARY KEY,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
  category_id SMALLINT PRIMARY KEY,
  name VARCHAR(25) NOT NULL,
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS film_actor (
  actor_id INTEGER NOT NULL REFERENCES actor(actor_id),
  film_id INTEGER NOT NULL REFERENCES film(film_id),
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY (actor_id, film_id)
);

CREATE TABLE IF NOT EXISTS film_category (
  film_id INTEGER NOT NULL REFERENCES film(film_id),
  category_id SMALLINT NOT NULL REFERENCES category(category_id),
  last_update TIMESTAMP NOT NULL,
  PRIMARY KEY (film_id, category_id)
);

CREATE TABLE IF NOT EXISTS inventory (
  inventory_id INTEGER PRIMARY KEY,
  film_id INTEGER NOT NULL REFERENCES film(film_id),
  store_id SMALLINT NOT NULL REFERENCES store(store_id),
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS rental (
  rental_id INTEGER PRIMARY KEY,
  rental_date TIMESTAMP NOT NULL,
  inventory_id INTEGER NOT NULL REFERENCES inventory(inventory_id),
  customer_id INTEGER NOT NULL REFERENCES customer(customer_id),
  return_date TIMESTAMP,
  staff_id SMALLINT NOT NULL REFERENCES staff(staff_id),
  last_update TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS payment (
  payment_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customer(customer_id),
  staff_id SMALLINT NOT NULL REFERENCES staff(staff_id),
  rental_id INTEGER NOT NULL REFERENCES rental(rental_id),
  amount NUMERIC(5,2) NOT NULL,
  payment_date TIMESTAMP NOT NULL,
  last_update TIMESTAMP NOT NULL
);