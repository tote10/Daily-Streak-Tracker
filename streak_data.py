import json
FILENAME = "streaks.json"

def load_streaks():
    try:
        with open(FILENAME, 'r') as f:
            streaks = json.load(f)
    except FileNotFoundError:
        streaks = {}
    return streaks
def save_streaks(streaks):
    with open(FILENAME, 'w') as f:
        json.dump(streaks, f, indent=4)