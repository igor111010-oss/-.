from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routes import missions, astronauts, rockets

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Space Missions Tracker API Started")
    print("📊 Database initialized")
    yield
    # Shutdown
    print("👋 Space Missions Tracker API Shutting Down")

app = FastAPI(
    title="Space Missions Tracker API",
    description="Track and manage space missions, astronauts, and rockets",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(missions.router)
app.include_router(astronauts.router)
app.include_router(rockets.router)

@app.get("/")
def root():
    return {
        "message": "🚀 Welcome to Space Missions Tracker API",
        "endpoints": {
            "missions": "/api/missions",
            "astronauts": "/api/astronauts",
            "rockets": "/api/rockets",
            "docs": "/docs"
        }
    }

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "system": "space-missions-tracker"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
