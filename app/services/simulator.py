"""
Scenario simulation engine leveraging Cerebras for rapid multi-scenario evaluation.
"""
import time
from typing import List, Dict, Any
from ..cerebras_client import cerebras_client
from .data_feeds import data_feed_service


class SimulatorService:
    """Service for running rapid scenario simulations using Cerebras AI."""
    
    def __init__(self):
        self.client = cerebras_client
    
    def run_simulation(self, incident_ids: List[str] = None, 
                       asset_ids: List[str] = None,
                       scenario_count: int = 5) -> Dict[str, Any]:
        """
        Run a multi-scenario simulation for the given incidents and assets.
        
        Args:
            incident_ids: Specific incident IDs to consider (None = all active)
            asset_ids: Specific asset IDs to consider (None = all available)
            scenario_count: Number of scenarios to simulate
            
        Returns:
            Simulation results with ranked scenarios
        """
        start_time = time.time()
        
        # Get incidents
        if incident_ids:
            incidents = [
                data_feed_service.get_incident(iid) 
                for iid in incident_ids 
                if data_feed_service.get_incident(iid)
            ]
        else:
            incidents = data_feed_service.get_all_incidents()
        
        # Get assets
        if asset_ids:
            assets = [
                data_feed_service.get_asset(aid)
                for aid in asset_ids
                if data_feed_service.get_asset(aid)
            ]
        else:
            assets = data_feed_service.get_all_assets()
        
        # Convert to dicts for AI
        incidents_data = [i.model_dump() for i in incidents]
        assets_data = [a.model_dump() for a in assets]
        
        # Run AI simulation
        result = self.client.simulate_scenarios(
            incidents=incidents_data,
            assets=assets_data,
            scenario_count=scenario_count
        )
        
        elapsed_ms = int((time.time() - start_time) * 1000)
        result["total_computation_time_ms"] = elapsed_ms
        result["incidents_considered"] = len(incidents_data)
        result["assets_considered"] = len(assets_data)
        
        return result
    
    def get_rescue_route(self, asset_id: str, incident_id: str) -> Dict[str, Any]:
        """
        Calculate optimal rescue route for an asset to an incident.
        
        Args:
            asset_id: The asset to route
            incident_id: The target incident
            
        Returns:
            Route information with waypoints and timing
        """
        asset = data_feed_service.get_asset(asset_id)
        incident = data_feed_service.get_incident(incident_id)
        
        if not asset or not incident:
            return {"error": "Asset or incident not found"}
        
        # Use AI for route optimization
        messages = [{
            "role": "user",
            "content": f"""Calculate optimal rescue route:

FROM: {asset.name} at {asset.location.model_dump()}
TO: {incident.description} at {incident.location.model_dump()}

Consider:
- Current flood conditions (6+ feet storm surge)
- Road closures and debris
- Weather: 120 mph winds, heavy rain

Provide JSON with:
- route_type: boat/helicopter/ground
- waypoints: list of {{lat, lon, description}}
- estimated_time_minutes: total time
- risks: potential hazards
- alternative_route: backup option if primary fails"""
        }]
        
        response = self.client.chat(messages, response_format={"type": "json_object"})
        
        try:
            import json
            route = json.loads(response["content"])
            route["asset_id"] = asset_id
            route["incident_id"] = incident_id
            return route
        except:
            return {"error": "Failed to calculate route", "raw": response["content"]}


# Singleton instance
simulator_service = SimulatorService()
