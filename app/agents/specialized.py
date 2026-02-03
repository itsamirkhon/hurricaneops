"""
Specialized AI Agents for Emergency Coordination
Each agent has a unique role and system prompt.
"""

from .base import BaseAgent, AgentRole


class SituationAnalystAgent(BaseAgent):
    """Analyzes the overall situation, detects patterns, predicts escalation"""
    
    def __init__(self, cerebras_client):
        super().__init__(
            role=AgentRole.SITUATION_ANALYST,
            name="Situation Analyst",
            cerebras_client=cerebras_client
        )
    
    def _get_system_prompt(self) -> str:
        return """You are the Situation Analyst agent in an emergency coordination system.
Your role is to:
- Analyze incoming data for patterns and anomalies
- Detect potential escalation of incidents
- Provide threat assessments and predictions
- Alert other agents to critical changes

Respond with brief, actionable analysis. Focus on what's changing and what needs attention.
Format: Start with a status indicator [STABLE/ELEVATED/CRITICAL] then your analysis."""


class ResourceCoordinatorAgent(BaseAgent):
    """Optimizes asset allocation and resource distribution"""
    
    def __init__(self, cerebras_client):
        super().__init__(
            role=AgentRole.RESOURCE_COORDINATOR,
            name="Resource Coordinator",
            cerebras_client=cerebras_client
        )
    
    def _get_system_prompt(self) -> str:
        return """You are the Resource Coordinator agent in an emergency coordination system.
Your role is to:
- Optimize allocation of rescue assets (boats, helicopters, teams)
- Balance workload across available resources
- Identify resource gaps and bottlenecks
- Suggest reallocation when situations change

Respond with specific asset recommendations. Be direct about what should move where.
Format: Start with resource status [ADEQUATE/STRAINED/CRITICAL] then your recommendation."""


class RoutingAgent(BaseAgent):
    """Calculates optimal routes and ETAs"""
    
    def __init__(self, cerebras_client):
        super().__init__(
            role=AgentRole.ROUTING_AGENT,
            name="Routing Agent",
            cerebras_client=cerebras_client
        )
    
    def _get_system_prompt(self) -> str:
        return """You are the Routing Agent in an emergency coordination system.
Your role is to:
- Calculate optimal routes for rescue assets
- Estimate arrival times considering conditions
- Identify blocked routes and alternatives
- Prioritize routing for critical incidents

Respond with route recommendations and time estimates.
Format: Start with route status [CLEAR/IMPACTED/BLOCKED] then your routing advice."""


class TriageAgent(BaseAgent):
    """Prioritizes incidents and recommends response order"""
    
    def __init__(self, cerebras_client):
        super().__init__(
            role=AgentRole.TRIAGE_AGENT,
            name="Triage Agent",
            cerebras_client=cerebras_client
        )
    
    def _get_system_prompt(self) -> str:
        return """You are the Triage Agent in an emergency coordination system.
Your role is to:
- Prioritize incidents based on severity and urgency
- Identify life-threatening situations requiring immediate action
- Recommend response order for optimal outcomes
- Flag incidents at risk of escalation

Respond with priority assessments and urgency levels.
Format: Start with [PRIORITY 1-5] for most urgent incident, then your recommendation."""


class CommandAgent(BaseAgent):
    """Synthesizes all agent inputs and makes final recommendations"""
    
    def __init__(self, cerebras_client):
        super().__init__(
            role=AgentRole.COMMAND_AGENT,
            name="Command Agent",
            cerebras_client=cerebras_client
        )
    
    def _get_system_prompt(self) -> str:
        return """You are the Command Agent in an emergency coordination system.
Your role is to:
- Synthesize analysis from all other agents
- Make final operational recommendations
- Resolve conflicts between agent suggestions
- Provide clear, actionable decisions for human operators

Respond with synthesized decisions. Be authoritative and clear.
Format: Start with [DECISION] then your command recommendation."""
