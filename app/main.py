# app/main.py
from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="My ML API",
    description="Backend untuk ML model serving",
    version="0.1.0",
)

app.include_router(endpoints.router, prefix="/api")

# Add a root endpoint to handle requests to '/'
@app.get("/")
def read_root():
    return {"message": "Welcome to My ML API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
