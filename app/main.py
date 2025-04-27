# app/main.py
from fastapi import FastAPI
from app.api import endpoints
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI(
    title="My ML API",
    description="Backend untuk ML model serving",
    version="0.1.0",
)

# Get FRONTEND_URL from environment
frontend_url = os.getenv("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url] if frontend_url else ["*"],  # Allow specific frontend URL or all origins
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

# Add a root endpoint to handle requests to '/'
@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}

