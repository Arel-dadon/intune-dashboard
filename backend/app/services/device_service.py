from collections import defaultdict
from ..loaders.csv_loader import load_devices
print("LOADED DEVICE SERVICE FROM:", __file__)

# ---------------------------------------------------------
# Get all devices (optional compliance filter)
# ---------------------------------------------------------
def get_all_devices(compliance_state: str | None = None):
    devices = load_devices()

    if compliance_state:
        devices = [
            d for d in devices
            if d.get("complianceState", "").lower()
            == compliance_state.lower()
        ]

    return devices


# ---------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Duplicate device analytics (grouped + paginated)
# ---------------------------------------------------------
def get_duplicate_devices(page: int = 1, page_size: int = 10):
    devices = load_devices()

    # 1️⃣ Group devices by deviceName
    grouped = defaultdict(list)

    for device in devices:
        name = device.get("deviceName", "Unknown")
        grouped[name].append(device)

    # 2️⃣ Keep only names that appear more than once
    duplicate_groups = {
        name: devs
        for name, devs in grouped.items()
        if len(devs) > 1
    }

    result_groups = []

    for name, devs in duplicate_groups.items():

        # Determine severity
        compliance_states = {
            d.get("complianceState", "").lower()
            for d in devs
        }

        if "noncompliant" in compliance_states:
            severity = "high"
        else:
            severity = "low"

        # Detect serial mismatch (if serialNumber exists)
        serials = {
            d.get("serialNumber")
            for d in devs
            if d.get("serialNumber")
        }

        serial_mismatch = len(serials) > 1

        result_groups.append({
            "deviceName": name,
            "duplicateCount": len(devs),
            "severity": severity,
            "serialMismatch": serial_mismatch,
            "devices": devs
        })

    # 3️⃣ Pagination logic
    total_groups = len(result_groups)

    total_pages = (
        total_groups // page_size
        + (1 if total_groups % page_size else 0)
    )

    start = (page - 1) * page_size
    end = start + page_size

    paged_groups = result_groups[start:end]

    # 4️⃣ Return structured response (matches frontend)
    return {
        "totalDuplicateGroups": total_groups,
        "currentPage": page,
        "totalPages": total_pages,
        "value": paged_groups
    }