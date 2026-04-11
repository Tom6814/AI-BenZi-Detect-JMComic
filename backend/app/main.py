from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, content, config, search, rules, identify

app = FastAPI(
    title="Backend API",
    description="A basic FastAPI backend",
    version="1.0.0",
)

# CORS Setup
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(content.router)
app.include_router(config.router)
app.include_router(search.router)
app.include_router(rules.router)
app.include_router(identify.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}
