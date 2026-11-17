"""
Technical Resolution Agent
Multi-Agent Enterprise AI Service Desk
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.models import AgentResponse, RiskLevel


class TechnicalResolutionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Technical Resolution Agent",
            role="Technical Diagnostics, Root Cause Analysis, and Troubleshooting Formulation",
            description="Analyzes telemetry data, KB recommendations, and user hardware configurations to draft technical solutions or flag uncertainty."
        )

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        user_input = context.get("user_input", "")
        memory_data = context.get("memory_data", {})
        kb_matches = memory_data.get("kb_matches", [])
        top_kb = memory_data.get("top_kb_article")
        system_status = context.get("system_status", {})
        device_profile = memory_data.get("assigned_device", "Standard Corporate Laptop")

        # 1. Hallucination Guardrail Check
        # If no verified KB article exists and no direct telemetry matches, trigger uncertainty
        if not kb_matches or not top_kb:
            return AgentResponse(
                agent_name=self.name,
                status="UNCERTAIN",
                summary="No verified IT documentation exists for this request. Refusing to synthesize unverified steps (Anti-Hallucination Guardrail).",
                data={
                    "verified_kb_found": False,
                    "confidence_score": 0.1,
                    "reason": "Request does not map to any approved enterprise knowledge base article."
                },
                confidence=0.1,
                recommendations=[
                    "Do NOT fabricate technical commands or procedures",
                    "Acknowledge lack of ground truth to user",
                    "Escalate request to Tier-2 Systems Engineering Team"
                ],
                risk_assessment=RiskLevel.MEDIUM,
                requires_escalation=True
            )

        # 2. Synthesize verified solution
        title = top_kb.get("title", "")
        content = top_kb.get("content", "")
        article_id = top_kb.get("id", "")

        troubleshooting_steps = [
            f"Verified Knowledge Base Reference: {article_id} - {title}",
            f"Target Endpoint Hardware: {device_profile}",
            f"Step 1: Inspect local adapter and certificate status per official policy.",
            f"Step 2: Follow protocol instructions: {content}",
        ]

        # Check telemetry correlation (e.g. VPN or Wi-Fi degradation)
        if system_status and system_status.get("operational_status") == "DEGRADED":
            troubleshooting_steps.insert(
                0,
                f"ALERT: Enterprise telemetry shows '{system_status.get('service_name')}' is currently DEGRADED ({system_status.get('telemetry_details')}). Local troubleshooting may be limited by upstream outage."
            )

        return AgentResponse(
            agent_name=self.name,
            status="RESOLVED",
            summary=f"Formulated verified resolution based on KB article {article_id}.",
            data={
                "article_id": article_id,
                "title": title,
                "steps": troubleshooting_steps,
                "device_profile": device_profile,
                "telemetry_evaluated": system_status.get("service_name") if system_status else "None"
            },
            confidence=0.92,
            recommendations=[
                "Present ordered troubleshooting steps to user",
                "Offer self-service ticket creation if issue persists"
            ],
            risk_assessment=RiskLevel.LOW,
            requires_escalation=False
        )

