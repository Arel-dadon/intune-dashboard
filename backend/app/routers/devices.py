from fastapi import APIRouter
from ..services.device_service import (
    get_all_devices,
    get_grouped_duplicates,
    get_summary,
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