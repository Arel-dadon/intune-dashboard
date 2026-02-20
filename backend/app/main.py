from fastapi import FastAPI
from .routers.devices import router as devices_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Intune Dashboard API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Backend running"}

app.include_router(devices_router)