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

from datetime import datetime


def get_stale_devices(days: int = 7):
    devices = load_devices()

    stale = []
    now = datetime.utcnow()

    for d in devices:
        last_sync = d.get("lastSyncDateTime")
        if not last_sync:
            continue

        try:
            last_sync_date = datetime.strptime(last_sync, "%Y-%m-%d")
            delta = (now - last_sync_date).days

            if delta >= days:
                stale.append({
                    "deviceName": d.get("deviceName"),
                    "daysSinceLastSync": delta,
                    "complianceState": d.get("complianceState"),
                    "ipAddress": d.get("ipAddress")
                })

        except Exception:
            continue

    return stale


def get_os_distribution():
    devices = load_devices()
    distribution = {}

    for d in devices:
        os_name = d.get("operatingSystem", "Unknown")
        distribution[os_name] = distribution.get(os_name, 0) + 1

    return distribution


def get_compliance_breakdown():
    devices = load_devices()
    breakdown = {}

    for d in devices:
        state = d.get("complianceState", "unknown")
        breakdown[state] = breakdown.get(state, 0) + 1

    return breakdown


def get_device_health():
    devices = load_devices()
    now = datetime.utcnow()

    health = []

    for d in devices:
        last_sync = d.get("lastSyncDateTime")
        if not last_sync:
            continue

        try:
            last_sync_date = datetime.strptime(last_sync, "%Y-%m-%d")
            delta = (now - last_sync_date).days

            if delta <= 3:
                status = "Healthy"
            elif delta <= 7:
                status = "Warning"
            else:
                status = "Critical"

            health.append({
                "deviceName": d.get("deviceName"),
                "daysSinceLastSync": delta,
                "status": status
            })

        except Exception:
            continue

    return health