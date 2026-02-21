from fastapi import APIRouter
from ..services.device_service import (
    get_all_devices,
    get_grouped_duplicates,
    get_summary,
    get_stale_devices,
    get_os_distribution,
    get_compliance_breakdown,
    get_device_health
)

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/")
def get_devices():
    return get_all_devices()


@router.get("/summary")
def summary():
    return get_summary()


@router.get("/duplicates")
def duplicates():
    devices = get_all_devices()
    return get_grouped_duplicates(devices)


@router.get("/stale")
def stale_devices_route(days: int = 7):
    return get_stale_devices(days)


@router.get("/os-distribution")
def os_distribution():
    return get_os_distribution()


@router.get("/compliance-breakdown")
def compliance_breakdown():
    return get_compliance_breakdown()


@router.get("/health")
def device_health():
    return get_device_health()