# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI(
    title="Defense System Helper - Python Backend",
    description="Quantum-Safe Security Implementation",
    version="1.0.0",
    root_path="/api/",
)

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["CORS_ORIGIN", "http://localhost:5173"],  # Allow specific frontend URL or all origins
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}