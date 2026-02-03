"""
Pydantic models for the Emergency Coordination System.
Defines data structures for incidents, assets, recommendations, and scenarios.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid


# Enums for categorization
class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentType(str, Enum):
    FLOOD_RESCUE = "flood_rescue"
    MEDICAL_EMERGENCY = "medical_emergency"
    STRUCTURAL_COLLAPSE = "structural_collapse"
    EVACUATION = "evacuation"
    UTILITY_FAILURE = "utility_failure"
    ROAD_BLOCKAGE = "road_blockage"


class AssetType(str, Enum):
    BOAT = "boat"
    HELICOPTER = "helicopter"
    GROUND_VEHICLE = "ground_vehicle"
    DRONE = "drone"
    MEDICAL_TEAM = "medical_team"
    RESCUE_TEAM = "rescue_team"


class AssetStatus(str, Enum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    EN_ROUTE = "en_route"
    ON_SCENE = "on_scene"
    RETURNING = "returning"
    MAINTENANCE = "maintenance"


# Location model
class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None


# Incident models
class Incident(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: IncidentType
    priority: Priority
    location: Location
    description: str
    affected_count: int = Field(default=1, ge=0)
    reported_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"
    assigned_assets: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class IncidentCreate(BaseModel):
    type: IncidentType
    priority: Priority
    location: Location
    description: str
    affected_count: int = 1


# Asset models
class Asset(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: AssetType
    status: AssetStatus = AssetStatus.AVAILABLE
    location: Location
    capacity: int = Field(default=4, ge=0)
    crew_size: int = Field(default=2, ge=1)
    assigned_incident: Optional[str] = None
    eta_minutes: Optional[int] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


# AI Recommendation models
class ActionRecommendation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str
    target_incident_id: Optional[str] = None
    assigned_asset_id: Optional[str] = None
    priority_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    estimated_time_minutes: Optional[int] = None
    risk_level: str = "medium"


class SituationAnalysis(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_incidents: int
    critical_incidents: int
    available_assets: int
    deployed_assets: int
    weather_conditions: str
    flood_level: str
    overall_assessment: str
    key_concerns: List[str]


class ScenarioResult(BaseModel):
    scenario_id: str
    description: str
    success_probability: float
    estimated_duration_minutes: int
    resources_required: List[str]
    risks: List[str]
    score: float


class SimulationRequest(BaseModel):
    incident_ids: List[str] = Field(default_factory=list)
    asset_ids: List[str] = Field(default_factory=list)
    simulation_count: int = Field(default=5, ge=1, le=20)


class SimulationResponse(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    scenarios_evaluated: int
    best_scenario: ScenarioResult
    all_scenarios: List[ScenarioResult]
    ai_recommendation: str
    computation_time_ms: int


# Weather and environmental models
class WeatherData(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    hurricane_category: Optional[int] = None
    wind_speed_mph: float
    rainfall_inches: float
    storm_surge_feet: float
    flood_zones_affected: List[str]
    forecast_summary: str


# Request/Response models for AI endpoints
class AnalyzeRequest(BaseModel):
    include_weather: bool = True
    include_predictions: bool = True


class RecommendRequest(BaseModel):
    incident_id: Optional[str] = None
    max_recommendations: int = Field(default=5, ge=1, le=10)
    consider_all_incidents: bool = True


class OptimizeRequest(BaseModel):
    objective: str = "minimize_response_time"
    constraints: List[str] = Field(default_factory=list)
