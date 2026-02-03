"""
AI router - Endpoints for Cerebras-powered AI capabilities.
Includes multi-agent collaboration system with real-time streaming.
"""
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

from ..cerebras_client import cerebras_client
from ..services.data_feeds import data_feed_service
from ..services.simulator import simulator_service
from ..models import SimulationRequest
from ..agents.orchestrator import orchestrator

router = APIRouter(prefix="/ai", tags=["AI"])


class AnalyzeResponse(BaseModel):
    timestamp: datetime
    overall_assessment: str
    critical_concerns: List[str]
    resource_adequacy: str
    recommended_priorities: List[str]
    weather_impact: str
    computation_time_ms: int


class RecommendRequest(BaseModel):
    incident_id: Optional[str] = None
    max_recommendations: int = 5


class OptimizeRequest(BaseModel):
    objective: str = "minimize_response_time"


@router.get("/status")
async def get_ai_status():
    """Check AI service status."""
    from ..config import settings
    return {
        "configured": settings.is_configured,
        "model": settings.CEREBRAS_MODEL,
        "message": "AI service ready" if settings.is_configured else "Configure CEREBRAS_API_KEY in .env"
    }


class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None


@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    Chat with AI about the current emergency situation.
    Uses Cerebras ultra-fast inference (gpt-oss-120b) for conversational responses.
    """
    import time
    from ..config import settings
    
    start_time = time.time()
    
    # Build context from current situation
    incidents = data_feed_service.get_all_incidents()
    assets = data_feed_service.get_all_assets()
    weather = data_feed_service.get_weather()
    
    # Format detailed context for AI
    incident_details = "\n".join([f"- [{i.id}] {i.type} at ({i.location.latitude}, {i.location.longitude}): {i.description} (Status: {i.status})" for i in incidents if i.status != 'resolved'])
    asset_details = "\n".join([f"- [{a.id}] {a.name} ({a.type}): {a.status} at {a.location.address}" for a in assets])

    system_prompt = f"""You are an AI emergency coordinator assistant for hurricane response operations.
You have access to real-time data about the ongoing emergency:

Current Weather:
- Hurricane Category: {weather.hurricane_category}
- Wind Speed: {weather.wind_speed_mph} mph
- Storm Surge: {weather.storm_surge_feet} ft

Active Incidents:
{incident_details}

Assets:
{asset_details}

Answer questions concisely and help coordinate the response. Be direct and actionable.
If asked about a specific location, check the incidents list for matches."""

    try:
        response = cerebras_client.chat(
            message=request.message,
            system_prompt=system_prompt
        )
        
        computation_ms = int((time.time() - start_time) * 1000)
        
        return {
            "response": response,
            "computation_ms": computation_ms,
            "model": settings.CEREBRAS_MODEL
        }
    except Exception as e:
        return {
            "error": str(e),
            "response": "Sorry, I couldn't process that request. Please try again."
        }


@router.post("/analyze")
async def analyze_situation():
    """
    Analyze the current emergency situation.
    Uses Cerebras ultra-fast inference to assess all active incidents and resources.
    """
    incidents = data_feed_service.get_all_incidents()
    assets = data_feed_service.get_all_assets()
    weather = data_feed_service.get_weather()
    
    incidents_data = [i.model_dump() for i in incidents]
    assets_data = [a.model_dump() for a in assets]
    weather_data = weather.model_dump()
    
    analysis = cerebras_client.analyze_situation(
        incidents=incidents_data,
        assets=assets_data,
        weather=weather_data
    )
    
    analysis["timestamp"] = datetime.utcnow().isoformat()
    return analysis


@router.post("/recommend")
async def get_recommendations(request: RecommendRequest):
    """
    Get AI-powered action recommendations.
    Returns prioritized, actionable recommendations with confidence levels.
    """
    if request.incident_id:
        incident = data_feed_service.get_incident(request.incident_id)
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        incidents = [incident]
    else:
        incidents = data_feed_service.get_all_incidents()
    
    assets = data_feed_service.get_all_assets()
    
    incidents_data = [i.model_dump() for i in incidents]
    assets_data = [a.model_dump() for a in assets]
    
    recommendations = cerebras_client.recommend_actions(
        incidents=incidents_data,
        assets=assets_data,
        max_recommendations=request.max_recommendations
    )
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "incident_focus": request.incident_id or "all",
        "recommendations": recommendations
    }


@router.post("/simulate")
async def run_simulation(request: SimulationRequest):
    """
    Run rapid multi-scenario simulation.
    Uses Cerebras wafer-scale compute to evaluate multiple tactical plans in seconds.
    """
    result = simulator_service.run_simulation(
        incident_ids=request.incident_ids if request.incident_ids else None,
        asset_ids=request.asset_ids if request.asset_ids else None,
        scenario_count=request.simulation_count
    )
    return result


@router.post("/optimize")
async def optimize_resources(request: OptimizeRequest):
    """
    Optimize resource allocation.
    Dynamically reassigns assets based on the specified objective.
    """
    incidents = data_feed_service.get_all_incidents()
    assets = data_feed_service.get_all_assets()
    
    incidents_data = [i.model_dump() for i in incidents]
    assets_data = [a.model_dump() for a in assets]
    
    optimization = cerebras_client.optimize_resources(
        incidents=incidents_data,
        assets=assets_data,
        objective=request.objective
    )
    
    optimization["timestamp"] = datetime.utcnow().isoformat()
    optimization["objective"] = request.objective
    return optimization


@router.post("/route/{asset_id}/{incident_id}")
async def get_rescue_route(asset_id: str, incident_id: str):
    """
    Calculate optimal rescue route from asset to incident.
    Considers current weather, flood conditions, and road status.
    """
    route = simulator_service.get_rescue_route(asset_id, incident_id)
    if "error" in route:
        raise HTTPException(status_code=400, detail=route["error"])
    return route




# ============== MULTI-AGENT ENDPOINTS ==============

@router.post("/agents/start")
async def start_agent_session():
    """
    Start a new multi-agent collaboration session.
    Initializes all 5 specialized agents for coordinated analysis.
    """
    session = orchestrator.start_session()
    return {
        "session_id": session.id,
        "started_at": session.started_at.isoformat(),
        "agents": list(orchestrator.agents.keys()),
        "message": "Agent session started. Use /agents/collaborate to run collaboration rounds."
    }


@router.get("/agents/status")
async def get_agents_status():
    """
    Get current status of all agents and session statistics.
    Shows computation times, message counts, and agent states.
    """
    return orchestrator.get_session_stats()


@router.get("/agents/messages")
async def get_agent_messages(limit: int = 20):
    """
    Get recent messages from agent collaboration.
    """
    return {
        "messages": orchestrator.get_recent_messages(limit),
        "total_in_session": orchestrator.session.total_messages if orchestrator.session else 0
    }


@router.post("/agents/collaborate")
async def run_agent_collaboration():
    """
    Run a full agent collaboration round.
    All 5 agents analyze the situation and communicate their findings.
    Returns real-time stream of agent messages via SSE.
    """
    async def generate():
        async for event in orchestrator.run_collaboration_round():
            yield f"data: {json.dumps(event)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/agents/stop")
async def stop_agent_session():
    """
    Stop the current agent collaboration session.
    """
    stats = orchestrator.get_session_stats()
    orchestrator.stop_session()
    return {
        "message": "Agent session stopped",
        "final_stats": stats
    }
