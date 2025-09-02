#!/usr/bin/env python3
import requests
import json
import webbrowser
import os
from datetime import datetime

BASE_URL = "https://berghain.challenges.listenlabs.ai"
PLAYER_ID = "e97f8594-f26f-4e0a-b848-0edf468588ca"

os.makedirs("logs", exist_ok=True)

LOG_FILE = None
FIRST_LOG_ENTRY = True

def init_logging():
    global LOG_FILE, FIRST_LOG_ENTRY
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/algo_01_{timestamp}.json"
    LOG_FILE = open(log_filename, 'w', buffering=1)
    LOG_FILE.write('[\n')
    FIRST_LOG_ENTRY = True
    return log_filename

def log(message, data=None):
    global FIRST_LOG_ENTRY
    if LOG_FILE is None:
        return

    if not FIRST_LOG_ENTRY:
        LOG_FILE.write(',\n')
    else:
        FIRST_LOG_ENTRY = False

    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "message": message
    }

    if data is not None:
        log_entry["data"] = data

    json.dump(log_entry, LOG_FILE, indent=2, default=str)
    LOG_FILE.flush()

def close_logging():
    global LOG_FILE
    if LOG_FILE:
        LOG_FILE.write('\n]')
        LOG_FILE.close()
        LOG_FILE = None

def log_data(data, prefix=""):
    log(prefix.strip(), data)

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
    log_filename = init_logging()
    print(f"Starting Berghain Bouncer Challenge - Algorithm 01")
    print(f"Logs will be written to: {log_filename}")
    log("Starting Berghain Bouncer Challenge - Algorithm 01")

    try:
        game_data = create_new_game(scenario=1)
        log_data(game_data, "NEW GAME")

        game_id = game_data["gameId"]
        print(f"Game ID: {game_id}")
        log(f"Game ID: {game_id}")

        game_url = f"{BASE_URL}/game/{game_id}"
        print(f"Opening game in browser: {game_url}")
        log(f"Opening game in browser: {game_url}")
        webbrowser.open(game_url)

        status = "running"
        person_index = 0

        while person_index <= 20000 and status == "running":
            try:
                decision_data = decide_and_next(game_id, person_index, accept=True)

                log_data(decision_data, f"P{person_index:05d}")

                status = decision_data.get("status", "running")
                next_person = decision_data.get("nextPerson")

                if next_person:
                    person_index = next_person["personIndex"]
                else:
                    break

            except Exception as e:
                log(f"Error during decision for person {person_index}: {e}")
                print(f"Error during decision for person {person_index}: {e}")
                break

        if status in ["completed", "failed"]:
            log_data(decision_data, f"FINAL ({status.upper()})")

        log(f"Game ended with status: {status}, total decisions: {person_index}")
        print(f"Game ended with status: {status}, total decisions: {person_index}")

    except Exception as e:
        log(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
    finally:
        close_logging()

if __name__ == "__main__":
    main()
