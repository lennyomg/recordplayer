from requests import get, put, post
from datetime import datetime
from urllib.parse import urlencode
from threading import Lock

# https://owntone.github.io/owntone-server/json-api/

base = "http://localhost:3689"


def library():
    response = get(f"{base}/api/library")
    response.raise_for_status()
    return response.json()


def outputs():
    response = get(f"{base}/api/outputs")
    response.raise_for_status()
    return response.json()


def player() -> bool:
    response = get(f"{base}/api/player")
    response.raise_for_status()
    return response.json()


def volume(output: str, volume: int):
    json = {"volume": volume}
    response = put(f"{base}/api/outputs/{output}", json=json)
    response.raise_for_status()


def repeat(state: str):
    # all, off, single
    response = put(f"{base}/api/player/repeat?state={state}")
    response.raise_for_status()


def shuffle(state: str):
    # true, false
    response = put(f"{base}/api/player/shuffle?state={state}")
    response.raise_for_status()


def set_outputs(outputs: list[str]):
    json = {"outputs": outputs}
    response = put(f"{base}/api/outputs/set", json=json)
    response.raise_for_status()


def pause():
    response = put(f"{base}/api/player/pause")
    response.raise_for_status()


def play():
    response = put(f"{base}/api/player/play")
    response.raise_for_status()


def stop():
    response = put(f"{base}/api/player/stop")
    response.raise_for_status()


def queue(args: dict):
    q = f"clear=true&playback=start&{urlencode(args)}"
    response = post(f"{base}/api/queue/items/add?{q}")
    response.raise_for_status()


def next():
    response = put(f"{base}/api/player/next")
    response.raise_for_status()


def previous():
    response = put(f"{base}/api/player/previous")
    response.raise_for_status()


if __name__ == "__main__":
    pass