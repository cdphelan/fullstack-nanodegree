-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create database, named tournament
CREATE DATABASE tournament;
\c tournament;

-- create the two necessary tables: players and matches
-- table players includes player name
CREATE TABLE players(
	id serial PRIMARY KEY,
	name varchar(50));

-- table matches includes the ids of the winning and losing players
CREATE TABLE matches(
	match_id serial PRIMARY KEY,
	winner serial REFERENCES players(id),
	loser serial REFERENCES players(id));




