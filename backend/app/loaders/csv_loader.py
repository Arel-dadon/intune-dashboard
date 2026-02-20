import csv
from pathlib import Path


CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "devices.csv"


def load_devices():
    devices = []

    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            devices.append(row)

    return devices