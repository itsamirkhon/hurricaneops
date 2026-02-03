"""
Base Agent class for multi-agent AI system.
Each agent has a specialized role and can communicate with other agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import time
import uuid


class AgentRole(str, Enum):
    SITUATION_ANALYST = "situation_analyst"
    RESOURCE_COORDINATOR = "resource_coordinator"
    ROUTING_AGENT = "routing_agent"
    TRIAGE_AGENT = "triage_agent"
    COMMAND_AGENT = "command_agent"


@dataclass
class AgentMessage:
    """A message exchanged between agents"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    from_agent: str = ""
    to_agent: str = ""
    message_type: str = "analysis"  # analysis, request, response, alert, decision
    content: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    computation_ms: int = 0
    tokens_used: int = 0


@dataclass
class AgentState:
    """Current state of an agent"""
    role: AgentRole
    name: str
    status: str = "idle"  # idle, thinking, responding, waiting
    current_task: str = ""
    last_active: datetime = field(default_factory=datetime.utcnow)
    messages_processed: int = 0
    total_computation_ms: int = 0


class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, role: AgentRole, name: str, cerebras_client):
        self.role = role
        self.name = name
        self.client = cerebras_client
        self.state = AgentState(role=role, name=name)
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self) -> str:
        """Override in subclasses"""
        return "You are an AI assistant."
    
    async def think(self, context: Dict[str, Any], messages: List[AgentMessage]) -> AgentMessage:
        """
        Process context and recent messages, generate a response.
        Returns an AgentMessage with the agent's analysis/response.
        """
        self.state.status = "thinking"
        self.state.current_task = "Analyzing situation..."
        start_time = time.time()
        
        # Build conversation from recent messages
        conversation = self._build_conversation(context, messages)
        
        # Call Cerebras API
        response = self.client.chat(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": conversation}
            ]
        )
        
        computation_ms = int((time.time() - start_time) * 1000)
        
        self.state.status = "idle"
        self.state.messages_processed += 1
        self.state.total_computation_ms += computation_ms
        self.state.last_active = datetime.utcnow()
        
        return AgentMessage(
            from_agent=self.role.value,
            to_agent="broadcast",
            message_type="analysis",
            content=response.get("content", ""),
            computation_ms=computation_ms,
            tokens_used=response.get("tokens_used", 0)
        )
    
    def _build_conversation(self, context: Dict[str, Any], messages: List[AgentMessage]) -> str:
        """Build conversation prompt from context and messages"""
        parts = [f"Current Situation:\n{self._format_context(context)}"]
        
        if messages:
            parts.append("\nRecent Agent Communications:")
            for msg in messages[-5:]:  # Last 5 messages
                parts.append(f"[{msg.from_agent}]: {msg.content}")
        
        parts.append(f"\nAs the {self.name}, provide your analysis or recommendation. Be concise (2-3 sentences max).")
        
        return "\n".join(parts)
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context for the prompt"""
        lines = []
        if "incidents" in context:
            lines.append(f"Active incidents: {len(context['incidents'])}")
            critical = sum(1 for i in context['incidents'] if i.get('priority') == 'critical')
            if critical:
                lines.append(f"Critical situations: {critical}")
        if "assets" in context:
            available = sum(1 for a in context['assets'] if a.get('status') == 'available')
            lines.append(f"Available assets: {available}/{len(context['assets'])}")
        if "weather" in context:
            w = context['weather']
            lines.append(f"Hurricane Cat {w.get('hurricane_category', '?')}, {w.get('wind_speed_mph', '?')}mph winds")
        return "\n".join(lines) if lines else "No context available"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize agent state for API response"""
        return {
            "role": self.role.value,
            "name": self.name,
            "status": self.state.status,
            "current_task": self.state.current_task,
            "messages_processed": self.state.messages_processed,
            "total_computation_ms": self.state.total_computation_ms,
            "last_active": self.state.last_active.isoformat()
        }
