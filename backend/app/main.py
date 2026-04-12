import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import health, content, config, search, rules, identify

app = FastAPI(
    title="Backend API",
    description="A basic FastAPI backend",
    version="1.0.0",
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

# Serve Frontend Static Files
# Calculate the absolute path to the frontend dist folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# For Docker, backend is in /app/backend, and frontend dist is in /app/frontend/dist
frontend_dist = os.path.join(os.path.dirname(BASE_DIR), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to the FastAPI Backend! (Frontend build not found)"}
