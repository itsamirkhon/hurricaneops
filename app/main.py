"""
FastAPI Application Entry Point
AI-Assisted Emergency Coordination System powered by Cerebras
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .config import settings
from .routers import incidents, assets, ai, actions, auth, analytics
from .services.data_feeds import data_feed_service

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    AI-powered emergency response coordination system for hurricane response operations.
    
    Powered by Cerebras wafer-scale compute for ultra-fast inference.
    
    ## Features
    - Real-time situational awareness
    - Rapid multi-scenario simulation
    - Prioritized action recommendations
    - Dynamic resource allocation
    - Cross-domain asset coordination
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(incidents.router, prefix="/api")
app.include_router(assets.router, prefix="/api")
app.include_router(ai.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(actions.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

# WebSocket Endpoint
from fastapi import WebSocket, WebSocketDisconnect
from .services.websocket import manager

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for messages (if any needed from client)
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def root():
    """Serve the main dashboard."""
    index_path = os.path.join(static_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Emergency Coordination System API", "docs": "/docs"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_configured": settings.is_configured
    }


@app.get("/api/summary")
async def get_summary():
    """Get summary statistics for the dashboard."""
    return data_feed_service.get_summary_stats()


@app.get("/api/weather")
async def get_weather():
    """Get current weather conditions."""
    return data_feed_service.get_weather()


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    if settings.is_configured:
        print("✅ Cerebras API configured")
    else:
        print("⚠️ Cerebras API not configured - using mock responses")
    print(f"📊 Loaded {len(data_feed_service.get_all_incidents())} demo incidents")
    print(f"🚁 Loaded {len(data_feed_service.get_all_assets())} demo assets")
    print(f"📡 API docs available at http://{settings.HOST}:{settings.PORT}/docs")
