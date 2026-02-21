from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.devices import router as devices_router

app = FastAPI(
    title="Intune Dashboard API",
    version="1.0.0"
)

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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.devices import router as devices_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices_router)

@app.get("/")
def root():
    return {"message": "Backend running"}