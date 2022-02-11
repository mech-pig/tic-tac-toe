#!/usr/bin/env bash

GAME=$(http POST :8080/games --print b)
GAME_ID=$(echo $GAME | jq -r '.id' )

http POST :8080/games/$GAME_ID/mark player:=1 cell=CENTER_CENTER
http POST :8080/games/$GAME_ID/mark player:=2 cell=BOTTOM_LEFT
http POST :8080/games/$GAME_ID/mark player:=1 cell=TOP_LEFT
http POST :8080/games/$GAME_ID/mark player:=2 cell=BOTTOM_RIGHT
http POST :8080/games/$GAME_ID/mark player:=1 cell=BOTTOM_CENTER
http POST :8080/games/$GAME_ID/mark player:=2 cell=TOP_CENTER
http POST :8080/games/$GAME_ID/mark player:=1 cell=CENTER_RIGHT
http POST :8080/games/$GAME_ID/mark player:=2 cell=CENTER_LEFT
http POST :8080/games/$GAME_ID/mark player:=1 cell=TOP_RIGHT