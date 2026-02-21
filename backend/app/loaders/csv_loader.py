import csv
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "devices.csv"


def load_devices():
    devices = []

    with open(DATA_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            devices.append(row)

    return devices