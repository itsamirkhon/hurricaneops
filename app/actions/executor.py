"""
Action Executor - Handles all operational commands.
Provides a unified interface for both human operators and AI agents.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import uuid


class ActionType(str, Enum):
    DEPLOY_ASSET = "deploy_asset"
    RECALL_ASSET = "recall_asset"
    ASSIGN_ASSET = "assign_asset"
    UNASSIGN_ASSET = "unassign_asset"
    CREATE_INCIDENT = "create_incident"
    RESOLVE_INCIDENT = "resolve_incident"
    UPDATE_PRIORITY = "update_priority"
    ESCALATE = "escalate"


class ActionSource(str, Enum):
    OPERATOR = "operator"
    AI_AGENT = "ai_agent"
    SYSTEM = "system"


class ActionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    EXECUTED = "executed"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass
class Action:
    """Represents an action to be executed"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: ActionType = ActionType.DEPLOY_ASSET
    source: ActionSource = ActionSource.OPERATOR
    params: Dict[str, Any] = field(default_factory=dict)
    status: ActionStatus = ActionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    executed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "source": self.source.value,
            "params": self.params,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "result": self.result,
            "error": self.error
        }


class ActionExecutor:
    """
    Executes actions on the system.
    Acts as the central command processor for all operations.
    """
    
    def __init__(self):
        self.action_log: List[Action] = []
        self.pending_actions: List[Action] = []
    
    def create_action(
        self,
        action_type: ActionType,
        params: Dict[str, Any],
        source: ActionSource = ActionSource.OPERATOR,
        auto_execute: bool = True
    ) -> Action:
        """Create a new action, optionally auto-executing it"""
        action = Action(
            type=action_type,
            source=source,
            params=params
        )
        
        if auto_execute:
            return self.execute(action)
        else:
            action.status = ActionStatus.PENDING
            self.pending_actions.append(action)
            return action
    
    def execute(self, action: Action) -> Action:
        """Execute an action and update system state"""
        from ..services.data_feeds import data_feed_service
        
        action.status = ActionStatus.APPROVED
        
        try:
            if action.type == ActionType.DEPLOY_ASSET:
                result = self._deploy_asset(action.params, data_feed_service)
            elif action.type == ActionType.RECALL_ASSET:
                result = self._recall_asset(action.params, data_feed_service)
            elif action.type == ActionType.ASSIGN_ASSET:
                result = self._assign_asset(action.params, data_feed_service)
            elif action.type == ActionType.UNASSIGN_ASSET:
                result = self._unassign_asset(action.params, data_feed_service)
            elif action.type == ActionType.CREATE_INCIDENT:
                result = self._create_incident(action.params, data_feed_service)
            elif action.type == ActionType.RESOLVE_INCIDENT:
                result = self._resolve_incident(action.params, data_feed_service)
            elif action.type == ActionType.UPDATE_PRIORITY:
                result = self._update_priority(action.params, data_feed_service)
            else:
                raise ValueError(f"Unknown action type: {action.type}")
            
            action.status = ActionStatus.EXECUTED
            action.executed_at = datetime.utcnow()
            action.result = result
            
        except Exception as e:
            action.status = ActionStatus.FAILED
            action.error = str(e)
        
        self.action_log.append(action)
        
        # Broadcast real-time update
        try:
            import asyncio
            from ..services.websocket import manager
            
            loop = asyncio.get_event_loop()
            if loop.is_running():
                msg = {
                    "type": "action_log",
                    "action": action.type.value,
                    "message": action.result.get("message") if action.result else "Action executed"
                }
                asyncio.run_coroutine_threadsafe(manager.broadcast(msg), loop)
                
                # Also trigger data refresh
                asyncio.run_coroutine_threadsafe(manager.broadcast({"type": "update"}), loop)
        except Exception as e:
            print(f"WS Broadcast failed: {e}")

        return action
    
    def _deploy_asset(self, params: Dict, service) -> Dict:
        """Deploy an asset to an incident location"""
        asset_id = params.get("asset_id")
        incident_id = params.get("incident_id")
        
        asset = service.get_asset(asset_id)
        incident = service.get_incident(incident_id)
        
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")
        
        # Update asset status and location
        service.update_asset(
            asset_id,
            status="en_route",
            assigned_incident=incident_id,
            eta_minutes=params.get("eta_minutes", 15)
        )
        
        return {
            "asset_id": asset_id,
            "incident_id": incident_id,
            "new_status": "en_route",
            "message": f"{asset.name} deployed to {incident_id}"
        }
    
    def _recall_asset(self, params: Dict, service) -> Dict:
        """Recall an asset back to base"""
        asset_id = params.get("asset_id")
        asset = service.get_asset(asset_id)
        
        if not asset:
            raise ValueError(f"Asset {asset_id} not found")
        
        service.update_asset(
            asset_id,
            status="returning",
            assigned_incident=None,
            eta_minutes=None
        )
        
        return {
            "asset_id": asset_id,
            "new_status": "returning",
            "message": f"{asset.name} recalled to base"
        }
    
    def _assign_asset(self, params: Dict, service) -> Dict:
        """Assign an asset to an incident"""
        asset_id = params.get("asset_id")
        incident_id = params.get("incident_id")
        
        service.assign_asset(asset_id, incident_id)
        
        return {
            "asset_id": asset_id,
            "incident_id": incident_id,
            "message": f"Asset {asset_id} assigned to {incident_id}"
        }
    
    def _unassign_asset(self, params: Dict, service) -> Dict:
        """Unassign an asset from its current incident"""
        asset_id = params.get("asset_id")
        
        service.release_asset(asset_id)
        
        return {
            "asset_id": asset_id,
            "message": f"Asset {asset_id} released"
        }
    
    def _create_incident(self, params: Dict, service) -> Dict:
        """Create a new incident"""
        from ..models import Incident, Location
        
        incident = Incident(
            id=f"INC-{str(uuid.uuid4())[:4].upper()}",
            type=params.get("type", "evacuation"),
            description=params.get("description", "New incident"),
            location=Location(
                latitude=params.get("latitude"),
                longitude=params.get("longitude"),
                address=params.get("address", "Unknown location")
            ),
            priority=params.get("priority", "medium"),
            affected_count=params.get("affected_count", 1),
            status="active"
        )
        
        service.add_incident(incident)
        
        return {
            "incident_id": incident.id,
            "message": f"Created incident {incident.id}"
        }
    
    def _resolve_incident(self, params: Dict, service) -> Dict:
        """Mark an incident as resolved"""
        incident_id = params.get("incident_id")
        
        service.update_incident(incident_id, status="resolved")
        
        # Release any assigned assets
        for asset in service.get_all_assets():
            if asset.assigned_incident == incident_id:
                service.release_asset(asset.id)
        
        return {
            "incident_id": incident_id,
            "message": f"Incident {incident_id} resolved"
        }
    
    def _update_priority(self, params: Dict, service) -> Dict:
        """Update incident priority"""
        incident_id = params.get("incident_id")
        new_priority = params.get("priority")
        
        service.update_incident(incident_id, priority=new_priority)
        
        return {
            "incident_id": incident_id,
            "new_priority": new_priority,
            "message": f"Priority updated to {new_priority}"
        }
    
    def get_action_log(self, limit: int = 50) -> List[Dict]:
        """Get recent action log"""
        return [a.to_dict() for a in self.action_log[-limit:]]
    
    def get_pending_actions(self) -> List[Dict]:
        """Get actions awaiting approval"""
        return [a.to_dict() for a in self.pending_actions]
    
    def approve_action(self, action_id: str) -> Action:
        """Approve and execute a pending action"""
        for i, action in enumerate(self.pending_actions):
            if action.id == action_id:
                self.pending_actions.pop(i)
                return self.execute(action)
        raise ValueError(f"Action {action_id} not found")
    
    def reject_action(self, action_id: str) -> Action:
        """Reject a pending action"""
        for i, action in enumerate(self.pending_actions):
            if action.id == action_id:
                action.status = ActionStatus.REJECTED
                self.pending_actions.pop(i)
                self.action_log.append(action)
                return action
        raise ValueError(f"Action {action_id} not found")


# Global executor instance
action_executor = ActionExecutor()
