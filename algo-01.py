#!/usr/bin/env python3
import requests
import json
import time
import webbrowser

BASE_URL = "https://berghain.challenges.listenlabs.ai"
PLAYER_ID = "e97f8594-f26f-4e0a-b848-0edf468588ca"

def log_data(data, prefix=""):
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {prefix}{json.dumps(data, indent=None)}")

def create_new_game(scenario=1):
    url = f"{BASE_URL}/new-game?scenario={scenario}&playerId={PLAYER_ID}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def decide_and_next(game_id, person_index, accept=True):
    url = f"{BASE_URL}/decide-and-next?gameId={game_id}&personIndex={person_index}&accept={str(accept).lower()}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def main():
    print("Starting Berghain Bouncer Challenge - Algorithm 01")

    try:
        game_data = create_new_game(scenario=1)
        log_data(game_data, "NEW GAME: ")
    except Exception as e:
        print(f"Failed to create new game: {e}")
        return

    game_id = game_data["gameId"]
    print(f"Game ID: {game_id}")

    game_url = f"{BASE_URL}/game/{game_id}"
    print(f"Opening game in browser: {game_url}")
    webbrowser.open(game_url)

    status = "running"
    person_index = 0

    while person_index <= 20000 and status == "running":
        try:
            decision_data = decide_and_next(game_id, person_index, accept=True)

            log_data(decision_data, f"P{person_index:04d}: ")

            status = decision_data.get("status", "running")
            next_person = decision_data.get("nextPerson")

            if next_person:
                person_index = next_person["personIndex"]
            else:
                break

        except Exception as e:
            print(f"Error during decision for person {person_index}: {e}")
            break

    if status in ["completed", "failed"]:
        log_data(decision_data, f"FINAL ({status.upper()}): ")

    print(f"Game ended with status: {status}")

if __name__ == "__main__":
    main()
