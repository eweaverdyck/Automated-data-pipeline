-- creating database for GANS city/flight/weather data

-- DROP DATABASE gans;
CREATE DATABASE gans;
USE gans;

-- DROP TABLE cities;
CREATE TABLE cities (
	city_id VARCHAR(10),
	city_name VARCHAR(50),
	country_code VARCHAR(5),
    lat FLOAT(10),
    lon FLOAT(10),
	PRIMARY KEY (city_id)
);

-- DROP TABLE weather;
CREATE TABLE weather (
	city_id VARCHAR(10),
    date_time DATETIME,
    temp FLOAT(4),
    wind_speed FLOAT(4),
    outlook VARCHAR(50),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- DROP TABLE populations;
CREATE TABLE populations (
	city_id VARCHAR(10),
    population INT,
    pop_year DATE,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- DROP TABLE airports;
CREATE TABLE airports (
	airport_icao CHAR(4),
    airport_name VARCHAR(50),
    PRIMARY KEY (airport_icao)
);

-- DROP TABLE airports_cities;
CREATE TABLE airports_cities (
	airport_icao CHAR(4),
    city_id VARCHAR(10),
    FOREIGN KEY (airport_icao) REFERENCES airports(airport_icao),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

-- DROP TABLE flights;
CREATE TABLE flights (
	flight_id INT AUTO_INCREMENT,
    flight_num VARCHAR(10),
    departure_icao CHAR(4),
    arrival_icao CHAR(4),
    arrival_time DATETIME,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (arrival_icao) REFERENCES airports(airport_icao)
);