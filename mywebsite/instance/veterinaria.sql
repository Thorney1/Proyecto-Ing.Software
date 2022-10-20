--
-- File generated with SQLiteStudio v3.3.3 on s�b. oct. 8 21:35:36 2022
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: animal
CREATE TABLE animal (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (1, 45) NOT NULL, tipo_animal_id INTEGER REFERENCES tipo_animal (id) NOT NULL, raza_id INTEGER REFERENCES tipo_animal (id) NOT NULL, edad VARCHAR NOT NULL, chip VARCHAR (15, 15) UNIQUE, stus_id INTEGER REFERENCES tipo_animal (id) NOT NULL, descripcion TEXT NOT NULL, ingreso DATETIME NOT NULL);

-- Table: raza
CREATE TABLE raza (id INTEGER PRIMARY KEY, nombre_raza VARCHAR NOT NULL);

-- Table: stus
CREATE TABLE stus (id INTEGER PRIMARY KEY AUTOINCREMENT, dolencia VARCHAR NOT NULL);

-- Table: tipo_animal
CREATE TABLE tipo_animal (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL);

-- Table: user
CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, rut VARCHAR (1, 10) UNIQUE NOT NULL, name VARCHAR (1, 45) NOT NULL, pass VARCHAR (6, 10) NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
