import json
from pathlib import Path

STEPS_FILE = Path("data/steps.json")

def save_steps(steps):
    STEPS_FILE.parent.mkdir(exist_ok=True)
    STEPS_FILE.write_text(json.dumps(steps, indent=2))

def load_steps():
    return json.loads(STEPS_FILE.read_text())
