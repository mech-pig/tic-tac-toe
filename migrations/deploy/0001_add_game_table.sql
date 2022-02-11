-- Deploy tic-tac-toe:0001_add_game_table to pg

BEGIN;

CREATE TABLE game (
    id TEXT UNIQUE NOT NULL PRIMARY KEY,
    state JSONB NOT NULL
);

COMMIT;
