"""
Agent Orchestrator - Coordinates multi-agent collaboration
Manages agent communication, message flow, and session state.
"""

import asyncio
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field
import json
import uuid

from .base import AgentMessage, AgentRole
from .specialized import (
    SituationAnalystAgent,
    ResourceCoordinatorAgent,
    RoutingAgent,
    TriageAgent,
    CommandAgent
)
from ..cerebras_client import cerebras_client
from ..services.data_feeds import data_feed_service


@dataclass
class AgentSession:
    """Represents an active agent collaboration session"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    started_at: datetime = field(default_factory=datetime.utcnow)
    messages: List[AgentMessage] = field(default_factory=list)
    is_active: bool = True
    total_computation_ms: int = 0
    total_messages: int = 0


class AgentOrchestrator:
    """
    Orchestrates multi-agent collaboration for emergency coordination.
    Manages agent lifecycle, message routing, and real-time updates.
    """
    
    def __init__(self):
        self.agents = {}
        self.session: Optional[AgentSession] = None
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Create all specialized agents"""
        self.agents = {
            AgentRole.SITUATION_ANALYST: SituationAnalystAgent(cerebras_client),
            AgentRole.RESOURCE_COORDINATOR: ResourceCoordinatorAgent(cerebras_client),
            AgentRole.ROUTING_AGENT: RoutingAgent(cerebras_client),
            AgentRole.TRIAGE_AGENT: TriageAgent(cerebras_client),
            AgentRole.COMMAND_AGENT: CommandAgent(cerebras_client),
        }
    
    def get_context(self) -> Dict[str, Any]:
        """Get current emergency context for agents"""
        incidents = [i.model_dump() for i in data_feed_service.get_all_incidents()]
        assets = [a.model_dump() for a in data_feed_service.get_all_assets()]
        weather = data_feed_service.get_weather().model_dump()
        
        return {
            "incidents": incidents,
            "assets": assets,
            "weather": weather,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def start_session(self) -> AgentSession:
        """Start a new agent collaboration session"""
        self.session = AgentSession()
        # Reset agent states
        for agent in self.agents.values():
            agent.state.status = "idle"
            agent.state.messages_processed = 0
            agent.state.total_computation_ms = 0
        return self.session
    
    def stop_session(self):
        """Stop the current session"""
        if self.session:
            self.session.is_active = False
    
    async def run_collaboration_round(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run a full collaboration round where all agents analyze and respond.
        Yields messages as they are generated for real-time streaming.
        """
        if not self.session:
            self.start_session()
        
        context = self.get_context()
        recent_messages = self.session.messages[-10:]  # Last 10 messages
        
        # Agent communication order (simulates realistic collaboration)
        communication_flow = [
            (AgentRole.SITUATION_ANALYST, "Analyzing current emergency situation..."),
            (AgentRole.TRIAGE_AGENT, "Assessing incident priorities..."),
            (AgentRole.RESOURCE_COORDINATOR, "Evaluating resource allocation..."),
            (AgentRole.ROUTING_AGENT, "Calculating optimal routes..."),
            (AgentRole.COMMAND_AGENT, "Synthesizing recommendations..."),
        ]
        
        round_start = time.time()
        messages_this_round = []
        
        for role, task_desc in communication_flow:
            agent = self.agents[role]
            agent.state.current_task = task_desc
            
            # Notify that agent is thinking
            yield {
                "type": "agent_status",
                "agent": role.value,
                "status": "thinking",
                "task": task_desc
            }
            
            # Small delay for visual effect
            await asyncio.sleep(0.1)
            
            # Agent thinks and generates response
            try:
                message = await agent.think(context, recent_messages + messages_this_round)
                messages_this_round.append(message)
                self.session.messages.append(message)
                self.session.total_messages += 1
                self.session.total_computation_ms += message.computation_ms
                
                # Yield the message
                yield {
                    "type": "agent_message",
                    "message": {
                        "id": message.id,
                        "from_agent": message.from_agent,
                        "to_agent": message.to_agent,
                        "content": message.content,
                        "computation_ms": message.computation_ms,
                        "timestamp": message.timestamp.isoformat()
                    }
                }
                
                # Notify that agent is done
                yield {
                    "type": "agent_status",
                    "agent": role.value,
                    "status": "idle",
                    "task": ""
                }
                
            except Exception as e:
                yield {
                    "type": "error",
                    "agent": role.value,
                    "error": str(e)
                }
        
        round_time = int((time.time() - round_start) * 1000)
        
        # Yield round summary
        yield {
            "type": "round_complete",
            "round_time_ms": round_time,
            "messages_count": len(messages_this_round),
            "avg_computation_ms": round_time // max(len(messages_this_round), 1)
        }
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics"""
        if not self.session:
            return {"active": False}
        
        return {
            "active": self.session.is_active,
            "session_id": self.session.id,
            "started_at": self.session.started_at.isoformat(),
            "total_messages": self.session.total_messages,
            "total_computation_ms": self.session.total_computation_ms,
            "avg_computation_ms": (
                self.session.total_computation_ms // max(self.session.total_messages, 1)
            ),
            "agents": {
                role.value: agent.to_dict()
                for role, agent in self.agents.items()
            }
        }
    
    def get_recent_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent messages from the session"""
        if not self.session:
            return []
        
        return [
            {
                "id": m.id,
                "from_agent": m.from_agent,
                "to_agent": m.to_agent,
                "content": m.content,
                "computation_ms": m.computation_ms,
                "timestamp": m.timestamp.isoformat()
            }
            for m in self.session.messages[-limit:]
        ]


# Global orchestrator instance
orchestrator = AgentOrchestrator()
