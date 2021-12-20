# py-slp

Python implementation of Server List Ping.

## Requirements

* Python 3

## Installation

```sh
pip install git+https://github.com/ttk1/py-slp.git
```

## Usage

```sh
$ server-list-ping -h
usage: server-list-ping [-h] [-p PORT] host

positional arguments:
  host                  host name

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port number
```

## Example

```sh
$ server-list-ping localhost | jq
{
  "description": {
    "extra": [
      {
        "text": "A Minecraft Server"
      }
    ],
    "text": ""
  },
  "players": {
    "max": 20,
    "online": 0
  },
  "version": {
    "name": "Spigot 1.18.1",
    "protocol": 757
  }
}
```

## Protocol Specification

https://wiki.vg/Server_List_Ping
