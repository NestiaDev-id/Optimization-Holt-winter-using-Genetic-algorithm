# app/main.py
from fastapi import FastAPI
from app.api import endpoints
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Defense System Helper - Python Backend",
    description="Quantum-Safe Security Implementation",
    version="1.0.0",
    root_path="/api/v1",
)

CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["CORS_ORIGIN"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}