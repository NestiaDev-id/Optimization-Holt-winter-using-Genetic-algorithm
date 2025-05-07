from fastapi import FastAPI
from app.api.endpoints import router  # Pastikan import dengan benar
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI(
    title="My ML API",
    description="Backend untuk ML model serving",
    version="0.1.0",
)

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://passager-ga-hw.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}
