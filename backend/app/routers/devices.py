from fastapi import APIRouter
from ..services.device_service import (
    get_all_devices,
    get_summary,
    get_duplicate_devices
)

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/")
def all_devices():
    return get_all_devices()


@router.get("/summary")
def summary():
    return get_summary()


@router.get("/duplicates")
def duplicates(page: int = 1, page_size: int = 10):
    return get_duplicate_devices(page, page_size)