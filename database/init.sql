CREATE DATABASE movie_rec;

\c movie_rec;

CREATE TABLE title_akas (
    titleid VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255)
);


CREATE TABLE title_basics (
    tconst VARCHAR(255) PRIMARY KEY,
    startYear INTEGER,
    genres VARCHAR(255)[]
);
ALTER TABLE title_basics ALTER COLUMN genres TYPE text;

CREATE TABLE title_crew (
    tconst VARCHAR(255) PRIMARY KEY,
    directors VARCHAR(255)[],
    writers VARCHAR(255)[]
);
ALTER TABLE title_crew ALTER COLUMN directors TYPE text;
ALTER TABLE title_crew ALTER COLUMN writers TYPE text;


CREATE TABLE title_principals (
    tconst VARCHAR(255),
    nconst VARCHAR(255),
    category VARCHAR(255),
    PRIMARY KEY (tconst, nconst)
);


CREATE TABLE title_ratings (
    tconst VARCHAR(255) PRIMARY KEY,
    averagerating NUMERIC,
    numvotes INTEGER
);


CREATE TABLE name_basics (
    nconst VARCHAR(255) PRIMARY KEY,
    primaryname VARCHAR(255)
);
