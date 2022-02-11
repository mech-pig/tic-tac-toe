# Tic-Tac-Toe as a service

Play tic-tac-toe via API.

### Quickstart

The simplest way to try the service is by using docker.
In the `Makefile` you can find a bunch of commands to spin up the app and the required dependencies.

To start a complete environment you can execute:

```sh
make ctx-run
```

This command creates a postgres database using docker-compose, then it performs the required schema migrations and finally starts the http server exposing it on port 8080 by default.

You can check the OpenAPI docs at http://localhost:8080/docs.

To stop the environmen you can use:

```sh
make ctx-down
```

The following example requests are perfomed using [httpie](https://httpie.io/):

#### start a new game

```sh
http POST :8080/games

HTTP/1.1 201 Created
content-length: 97
content-type: application/json
date: Fri, 11 Feb 2022 12:12:35 GMT
server: uvicorn

{
    "id": "6bd0831e6e164d448630551d800e3591",
    "state": {
        "marks": {},
        "next_player": 1,
        "status": "ONGOING"
    }
}
```

#### add mark

```sh
http POST :8080/games/6bd0831e6e164d448630551d800e3591/mark player:=1 cell=BOTTOM_LEFT

HTTP/1.1 200 OK
content-length: 112
content-type: application/json
date: Fri, 11 Feb 2022 13:16:23 GMT
server: uvicorn

{
    "id": "6bd0831e6e164d448630551d800e3591",
    "state": {
        "marks": {
            "BOTTOM_LEFT": 1
        },
        "next_player": 2,
        "status": "ONGOING"
    }
}
```

#### get game

```sh
http GET :8080/games/6bd0831e6e164d448630551d800e3591

HTTP/1.1 200 OK
content-length: 112
content-type: application/json
date: Fri, 11 Feb 2022 13:17:42 GMT
server: uvicorn

{
    "id": "6bd0831e6e164d448630551d800e3591",
    "state": {
        "marks": {
            "BOTTOM_LEFT": 1
        },
        "next_player": 2,
        "status": "ONGOING"
    }
}
```

In the `examples` folder there are some scripts that simulate a complete game.
