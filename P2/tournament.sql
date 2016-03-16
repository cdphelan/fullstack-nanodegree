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

CREATE VIEW win_count AS
    SELECT players.id, players.name, count(matches.winner) AS wins
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id;

CREATE VIEW loss_count AS
    SELECT players.id, players.name, count(matches.loser) AS losses
    FROM players LEFT JOIN matches
        ON players.id = matches.loser
    GROUP BY players.id;

CREATE VIEW match_count AS
    SELECT win_count.id, SUM(loss_count.losses + win_count.wins) AS match_num
    FROM win_count LEFT JOIN loss_count
    ON win_count.id=loss_count.id
    GROUP BY win_count.id;

CREATE VIEW rankings AS
    SELECT win_count.id,win_count.name,win_count.wins,
    match_count.match_num AS match_num
    FROM win_count LEFT JOIN match_count
    ON win_count.id=match_count.id
    ORDER BY win_count.wins DESC;

