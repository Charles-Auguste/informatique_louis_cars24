CREATE DATABASE IF NOT EXISTS cars24;
USE cars24;

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS transaction;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS engine;
DROP TABLE IF EXISTS transmission;

-- Engine Table
CREATE TABLE engine (
  id_engine VARCHAR(255) PRIMARY KEY,
  fuel_type VARCHAR(50),
  capacity VARCHAR(50)
);

-- Transmission Table
CREATE TABLE transmission (
  id_transmission VARCHAR(255) PRIMARY KEY,
  transmission_type VARCHAR(50)
);

-- Model Table
CREATE TABLE model (
  id_model VARCHAR(255) PRIMARY KEY,
  model_name VARCHAR(100),
  id_engine VARCHAR(255),
  id_transmission VARCHAR(255),
  manufacturing_year INT
);

-- Customer Table
CREATE TABLE customer (
  id_customer VARCHAR(255) PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(255),
  rating VARCHAR(10)
);

-- Transaction Table
CREATE TABLE transaction (
  id_transaction VARCHAR(255) PRIMARY KEY,
  id_customer VARCHAR(255),
  id_model VARCHAR(255),
  price FLOAT,
  km_driven FLOAT,
  spare_key BOOLEAN,
  ownership INT,
  imperfections INT,
  repainted_parts INT
);

-- Create a new user and grant all privileges on `cars24`
CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'secret';
GRANT ALL PRIVILEGES ON cars24.* TO 'admin'@'%';
FLUSH PRIVILEGES;

