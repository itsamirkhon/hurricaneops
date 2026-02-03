"""
Incidents router - REST endpoints for incident management.
"""
from typing import List
from fastapi import APIRouter, HTTPException
from ..models import Incident, IncidentCreate
from ..services.data_feeds import data_feed_service

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("", response_model=List[Incident])
async def get_all_incidents():
    """Get all active incidents."""
    return data_feed_service.get_all_incidents()


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    """Get a specific incident by ID."""
    incident = data_feed_service.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("", response_model=Incident)
async def create_incident(incident_data: IncidentCreate):
    """Create a new incident."""
    incident = Incident(**incident_data.model_dump())
    return data_feed_service.add_incident(incident)


@router.patch("/{incident_id}", response_model=Incident)
async def update_incident(incident_id: str, updates: dict):
    """Update an existing incident."""
    incident = data_feed_service.update_incident(incident_id, updates)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.delete("/{incident_id}")
async def delete_incident(incident_id: str):
    """Delete an incident."""
    if not data_feed_service.delete_incident(incident_id):
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"status": "deleted", "incident_id": incident_id}


@router.post("/{incident_id}/notes")
async def add_note(incident_id: str, note: str):
    """Add a note to an incident."""
    incident = data_feed_service.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    notes = incident.notes + [note]
    updated = data_feed_service.update_incident(incident_id, {"notes": notes})
    return updated
