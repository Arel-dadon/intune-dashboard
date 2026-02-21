from collections import defaultdict
from ..loaders.csv_loader import load_devices


def get_all_devices(compliance_state: str | None = None):
    devices = load_devices_cached()

    if compliance_state:
        devices = [
            d for d in devices
            if d.get("complianceState", "").lower()
            == compliance_state.lower()
        ]

    return devices


def get_summary():
    devices = load_devices()

    total = len(devices)

    compliant = len([
        d for d in devices
        if d.get("complianceState", "").lower() == "compliant"
    ])

    noncompliant = len([
        d for d in devices
        if d.get("complianceState", "").lower() == "noncompliant"
    ])

    return {
        "total": total,
        "compliant": compliant,
        "nonCompliant": noncompliant
    }


def get_grouped_duplicates(devices):
    groups = defaultdict(list)

    for d in devices:
        name = d.get("deviceName") or "(missing)"
        groups[name].append(d)

    result = []

    for name, items in groups.items():
        if len(items) > 1:
            compliance_states = {
                d.get("complianceState", "").lower()
                for d in items
            }

            severity = "HIGH" if "noncompliant" in compliance_states else "LOW"

            result.append({
                "deviceName": name,
                "count": len(items),
                "severity": severity,
                "devices": items
            })

    result.sort(key=lambda x: x["deviceName"])
    return result

_devices_cache = None

def load_devices_cached():
    global _devices_cache
    if _devices_cache is None:
        _devices_cache = load_devices()
    return _devices_cache