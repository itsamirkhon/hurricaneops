"""
Assets router - REST endpoints for asset tracking and management.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..models import Asset, AssetStatus
from ..services.data_feeds import data_feed_service

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("", response_model=List[Asset])
async def get_all_assets():
    """Get all assets."""
    return data_feed_service.get_all_assets()


@router.get("/available", response_model=List[Asset])
async def get_available_assets():
    """Get only available assets."""
    return data_feed_service.get_available_assets()


@router.get("/{asset_id}", response_model=Asset)
async def get_asset(asset_id: str):
    """Get a specific asset by ID."""
    asset = data_feed_service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.patch("/{asset_id}", response_model=Asset)
async def update_asset(asset_id: str, updates: dict):
    """Update an asset's status or location."""
    asset = data_feed_service.update_asset(asset_id, updates)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/{asset_id}/assign/{incident_id}", response_model=Asset)
async def assign_asset_to_incident(asset_id: str, incident_id: str, eta_minutes: int = None):
    """Assign an asset to an incident."""
    asset = data_feed_service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    incident = data_feed_service.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Update asset
    updated_asset = data_feed_service.assign_asset(asset_id, incident_id, eta_minutes)
    
    # Update incident's assigned assets
    assigned = incident.assigned_assets + [asset_id]
    data_feed_service.update_incident(incident_id, {"assigned_assets": assigned})
    
    return updated_asset


@router.post("/{asset_id}/release", response_model=Asset)
async def release_asset(asset_id: str):
    """Release an asset from its current assignment."""
    asset = data_feed_service.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # If assigned to an incident, remove from that incident's list
    if asset.assigned_incident:
        incident = data_feed_service.get_incident(asset.assigned_incident)
        if incident:
            assigned = [a for a in incident.assigned_assets if a != asset_id]
            data_feed_service.update_incident(asset.assigned_incident, {"assigned_assets": assigned})
    
    return data_feed_service.update_asset(asset_id, {
        "status": AssetStatus.AVAILABLE,
        "assigned_incident": None,
        "eta_minutes": None
    })
