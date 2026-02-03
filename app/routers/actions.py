"""
Actions router - API endpoints for command & control operations.
Allows operators and AI agents to execute actions on the system.
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..actions.executor import action_executor, ActionType, ActionSource
from ..utils.security import get_current_active_user, UserDB

router = APIRouter(prefix="/actions", tags=["Actions"])


# Request models
class DeployRequest(BaseModel):
    asset_id: str
    incident_id: str
    eta_minutes: Optional[int] = 15


class RecallRequest(BaseModel):
    asset_id: str


class AssignRequest(BaseModel):
    asset_id: str
    incident_id: str


class CreateIncidentRequest(BaseModel):
    type: str = "evacuation"
    description: str
    latitude: float
    longitude: float
    address: Optional[str] = "Unknown location"
    priority: str = "medium"
    affected_count: int = 1


class UpdatePriorityRequest(BaseModel):
    incident_id: str
    priority: str


# Endpoints
@router.post("/deploy")
async def deploy_asset(request: DeployRequest, current_user: UserDB = Depends(get_current_active_user)):
    """Deploy an asset to an incident - sends the asset en route"""
    action = action_executor.create_action(
        action_type=ActionType.DEPLOY_ASSET,
        params=request.model_dump(),
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/recall")
async def recall_asset(request: RecallRequest, current_user: UserDB = Depends(get_current_active_user)):
    """Recall an asset back to base"""
    action = action_executor.create_action(
        action_type=ActionType.RECALL_ASSET,
        params=request.model_dump(),
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/assign")
async def assign_asset(request: AssignRequest, current_user: UserDB = Depends(get_current_active_user)):
    """Assign an asset to an incident"""
    action = action_executor.create_action(
        action_type=ActionType.ASSIGN_ASSET,
        params=request.model_dump(),
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/unassign/{asset_id}")
async def unassign_asset(asset_id: str, current_user: UserDB = Depends(get_current_active_user)):
    """Unassign an asset from its current incident"""
    action = action_executor.create_action(
        action_type=ActionType.UNASSIGN_ASSET,
        params={"asset_id": asset_id},
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/incident/create")
async def create_incident(request: CreateIncidentRequest, current_user: UserDB = Depends(get_current_active_user)):
    """Create a new incident"""
    action = action_executor.create_action(
        action_type=ActionType.CREATE_INCIDENT,
        params=request.model_dump(),
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/incident/{incident_id}/resolve")
async def resolve_incident(incident_id: str, current_user: UserDB = Depends(get_current_active_user)):
    """Resolve/close an incident"""
    action = action_executor.create_action(
        action_type=ActionType.RESOLVE_INCIDENT,
        params={"incident_id": incident_id},
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.post("/incident/priority")
async def update_priority(request: UpdatePriorityRequest, current_user: UserDB = Depends(get_current_active_user)):
    """Update incident priority"""
    if request.priority not in ["critical", "high", "medium", "low"]:
        raise HTTPException(status_code=400, detail="Invalid priority")
    
    action = action_executor.create_action(
        action_type=ActionType.UPDATE_PRIORITY,
        params=request.model_dump(),
        source=ActionSource.OPERATOR
    )
    return action.to_dict()


@router.get("/log")
async def get_action_log(limit: int = 50):
    """Get recent action log"""
    return {
        "actions": action_executor.get_action_log(limit),
        "total": len(action_executor.action_log)
    }


@router.get("/pending")
async def get_pending_actions():
    """Get actions awaiting approval"""
    return {
        "pending": action_executor.get_pending_actions(),
        "count": len(action_executor.pending_actions)
    }


@router.post("/approve/{action_id}")
async def approve_action(action_id: str):
    """Approve and execute a pending action"""
    try:
        action = action_executor.approve_action(action_id)
        return action.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/reject/{action_id}")
async def reject_action(action_id: str):
    """Reject a pending action"""
    try:
        action = action_executor.reject_action(action_id)
        return action.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
