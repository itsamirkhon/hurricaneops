"""
Cerebras API client wrapper for ultra-fast AI inference.
Provides methods for emergency coordination AI capabilities.
"""
import json
import time
from typing import Optional, List, Dict, Any
from cerebras.cloud.sdk import Cerebras
from .config import settings


class CerebrasClient:
    """Wrapper for Cerebras API providing emergency coordination AI capabilities."""
    
    def __init__(self):
        self.client: Optional[Cerebras] = None
        self.model = settings.CEREBRAS_MODEL
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Cerebras client if API key is configured."""
        if settings.is_configured:
            self.client = Cerebras(api_key=settings.CEREBRAS_API_KEY)
        else:
            print("⚠️ Cerebras API key not configured. AI features will use mock responses.")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for emergency coordination."""
        return """You are an AI emergency coordination assistant for hurricane response operations in Florida.
Your role is to analyze emergency situations, prioritize rescue operations, and provide actionable recommendations.

Key responsibilities:
1. Analyze incident reports and prioritize based on urgency and severity
2. Recommend optimal resource allocation (boats, helicopters, ground vehicles, drones)
3. Suggest efficient rescue routes considering flood levels and road conditions
4. Provide triage recommendations for medical emergencies
5. Coordinate multi-agency response efforts

Always provide:
- Clear, actionable recommendations
- Confidence levels for your assessments
- Risk factors to consider
- Time estimates when possible

Remember: Human incident commanders make final decisions. Your role is advisory.
Respond in structured JSON format when requested."""

    def chat(self, messages: List[Dict[str, str]] = None, 
             response_format: Optional[Dict] = None,
             message: str = None,
             system_prompt: str = None) -> Dict[str, Any]:
        """
        Send a chat completion request to Cerebras.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            response_format: Optional JSON schema for structured output
            message: Simple text message (alternative to messages list)
            system_prompt: Custom system prompt (for simple message mode)
            
        Returns:
            Response dict with 'content' and 'usage' info, or just the text response for simple mode
        """
        start_time = time.time()
        
        # Handle simple message mode
        if message and not messages:
            messages = [{"role": "user", "content": message}]
            use_simple_mode = True
        else:
            use_simple_mode = False
        
        if not self.client:
            # Return mock response if not configured
            if use_simple_mode:
                return "I'm running in demo mode. Configure CEREBRAS_API_KEY for real AI responses."
            return self._mock_response(messages)
        
        try:
            # Prepare request params
            prompt = system_prompt if system_prompt else self._get_system_prompt()
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt},
                    *messages
                ],
            }
            
            if response_format:
                params["response_format"] = response_format
            
            # Make API call
            response = self.client.chat.completions.create(**params)
            
            elapsed_ms = int((time.time() - start_time) * 1000)
            
            # Return simple string for simple mode
            if use_simple_mode:
                return response.choices[0].message.content
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "computation_time_ms": elapsed_ms,
                "model": self.model
            }
            
        except Exception as e:
            print(f"Cerebras API error: {e}")
            if use_simple_mode:
                return f"Error: {str(e)}"
            return self._mock_response(messages)
    
    def analyze_situation(self, incidents: List[Dict], assets: List[Dict], 
                          weather: Dict) -> Dict[str, Any]:
        """
        Analyze the current emergency situation.
        
        Args:
            incidents: List of active incidents
            assets: List of available assets
            weather: Current weather conditions
            
        Returns:
            Situation analysis with key insights
        """
        prompt = f"""Analyze this emergency situation and provide a structured assessment:

ACTIVE INCIDENTS:
{json.dumps(incidents, indent=2, default=str)}

AVAILABLE ASSETS:
{json.dumps(assets, indent=2, default=str)}

WEATHER CONDITIONS:
{json.dumps(weather, indent=2, default=str)}

Provide your analysis in JSON format with these fields:
- overall_assessment: Brief summary of the situation
- critical_concerns: List of top 3-5 urgent concerns
- resource_adequacy: Assessment of whether resources are sufficient
- recommended_priorities: Ordered list of incident IDs by priority
- weather_impact: How weather affects operations"""

        response = self.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            analysis = json.loads(response["content"])
            analysis["computation_time_ms"] = response.get("computation_time_ms", 0)
            return analysis
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response", "raw": response["content"]}
    
    def recommend_actions(self, incidents: List[Dict], assets: List[Dict],
                          max_recommendations: int = 5) -> List[Dict]:
        """
        Generate prioritized action recommendations.
        
        Args:
            incidents: Active incidents requiring response
            assets: Available and deployed assets
            max_recommendations: Maximum number of recommendations
            
        Returns:
            List of action recommendations with priorities and reasoning
        """
        prompt = f"""Based on the current situation, recommend the top {max_recommendations} actions:

INCIDENTS:
{json.dumps(incidents, indent=2, default=str)}

ASSETS:
{json.dumps(assets, indent=2, default=str)}

For each recommendation, provide JSON with:
- action: Clear description of what to do
- target_incident_id: Which incident this addresses (if applicable)
- assigned_asset_id: Which asset to use (if applicable)
- priority_score: 0-100 score (100 = most urgent)
- confidence: 0-1 confidence in this recommendation
- reasoning: Why this action is recommended
- estimated_time_minutes: Expected time to complete
- risk_level: low/medium/high

Return as JSON array of recommendations."""

        response = self.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            result = json.loads(response["content"])
            if isinstance(result, dict) and "recommendations" in result:
                return result["recommendations"]
            elif isinstance(result, list):
                return result
            return [result]
        except json.JSONDecodeError:
            return [{"error": "Failed to parse AI response", "raw": response["content"]}]
    
    def simulate_scenarios(self, incidents: List[Dict], assets: List[Dict],
                           scenario_count: int = 5) -> Dict[str, Any]:
        """
        Simulate multiple rescue scenarios and rank them.
        
        Args:
            incidents: Active incidents
            assets: Available assets
            scenario_count: Number of scenarios to simulate
            
        Returns:
            Simulation results with ranked scenarios
        """
        prompt = f"""Simulate {scenario_count} different response scenarios for this situation:

INCIDENTS:
{json.dumps(incidents, indent=2, default=str)}

ASSETS:
{json.dumps(assets, indent=2, default=str)}

For each scenario, provide:
- scenario_id: Unique identifier (S1, S2, etc.)
- description: Brief description of the approach
- asset_assignments: Which assets go where
- sequence: Order of operations
- success_probability: 0-1 probability of success
- estimated_duration_minutes: Total time estimate
- risks: List of potential problems
- score: Overall score 0-100

Return JSON with:
- best_scenario: The highest-scoring scenario
- all_scenarios: Array of all scenarios
- recommendation: Your advice on which to choose and why"""

        start_time = time.time()
        response = self.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        try:
            result = json.loads(response["content"])
            result["computation_time_ms"] = elapsed_ms
            return result
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response", "raw": response["content"]}
    
    def optimize_resources(self, incidents: List[Dict], assets: List[Dict],
                           objective: str = "minimize_response_time") -> Dict[str, Any]:
        """
        Optimize resource allocation based on objective.
        
        Args:
            incidents: Active incidents
            assets: All assets
            objective: Optimization goal
            
        Returns:
            Optimized allocation plan
        """
        prompt = f"""Optimize resource allocation with objective: {objective}

INCIDENTS:
{json.dumps(incidents, indent=2, default=str)}

ASSETS:
{json.dumps(assets, indent=2, default=str)}

Provide an optimal allocation plan in JSON with:
- allocations: Array of {{asset_id, incident_id, route_summary, eta_minutes}}
- unassigned_assets: Assets to keep in reserve
- coverage_gaps: Incidents without adequate resources
- efficiency_score: 0-100 overall efficiency
- rationale: Explanation of the optimization logic"""

        response = self.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response["content"])
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI response", "raw": response["content"]}
    
    def _mock_response(self, messages: List[Dict]) -> Dict[str, Any]:
        """Generate mock response when API is not configured."""
        return {
            "content": json.dumps({
                "message": "Mock AI response - Configure CEREBRAS_API_KEY for real AI",
                "overall_assessment": "Demo mode - AI analysis unavailable",
                "recommendations": [
                    {
                        "action": "Deploy Boat Alpha to Grid 7 for flood rescue",
                        "priority_score": 95,
                        "confidence": 0.85,
                        "reasoning": "Multiple 911 calls from flooded area",
                        "estimated_time_minutes": 15,
                        "risk_level": "medium"
                    }
                ]
            }),
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "computation_time_ms": 50,
            "model": "mock"
        }


# Singleton instance
cerebras_client = CerebrasClient()
