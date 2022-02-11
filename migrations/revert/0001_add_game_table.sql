-- Revert tic-tac-toe:0001_add_game_table from pg

BEGIN;

DROP TABLE game;

COMMIT;
