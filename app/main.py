# app/main.py
from fastapi import FastAPI
from app.api import endpoints
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from dotenv import load_dotenv

app = FastAPI(
    title="My ML API",
    description="Backend untuk ML model serving",
    version="0.1.0",
)
load_dotenv()
# Get FRONTEND_URL from environment
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "https://passager-ga-hw.vercel.app"],  # Allow specific frontend URL or all origins
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api")

# Add a root endpoint to handle requests to '/'
@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}

# ! For development purposes only, remove in production
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)