"""
User Interaction Agent
Multi-Agent Enterprise AI Service Desk
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.models import AgentResponse, RiskLevel


class UserInteractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="User Interaction Agent",
            role="Front-Line Conversation, Intent Elicitation, and Response Synthesis",
            description="Interacts directly with employees, parses user intent, gathers missing details, and formats the final empathetic, human-readable response."
        )

    def analyze_intent(self, text: str) -> Dict[str, Any]:
        """Classifies high-level user intent and checks if critical information is missing."""
        lower = text.lower()
        if len(text.strip()) < 8:
            return {"intent": "CLARIFICATION_NEEDED", "missing": "Sufficient description of the issue"}

        if any(w in lower for w in ["wifi", "wi-fi", "wireless", "disconnect", "internet"]):
            return {"intent": "NETWORK_WIFI", "category": "Network Connectivity"}
        elif any(w in lower for w in ["vpn", "tunnel", "anyconnect", "remote"]):
            return {"intent": "NETWORK_VPN", "category": "Network Connectivity"}
        elif any(w in lower for w in ["password", "mfa", "login", "locked out"]):
            return {"intent": "AUTH_RESET", "category": "Authentication & Access"}
        elif any(w in lower for w in ["install", "download", "software", "application"]):
            return {"intent": "SOFTWARE_INSTALL", "category": "Software & Applications"}
        elif any(w in lower for w in ["ticket", "status", "incident"]):
            return {"intent": "TICKET_QUERY", "category": "Support Inquiry"}
        else:
            return {"intent": "GENERAL_INQUIRY", "category": "General IT"}

    def format_final_response(
        self,
        user_name: str,
        technical_response: AgentResponse,
        tool_results: List[Dict[str, Any]],
        memories_used: Dict[str, str],
        security_assessment: Dict[str, Any]
    ) -> str:
        """Constructs a polished, professional enterprise support response."""
        greeting = f"Hello {user_name},"

        # Case 1: Security Blocked
        if security_assessment.get("is_safe") is False:
            flags = ", ".join(security_assessment.get("flags", []))
            reason = security_assessment.get("reason", "Policy violation detected.")
            return (
                f"{greeting}\n\n"
                f"⚠️ **Security Alert & Request Halted**\n\n"
                f"Your request could not be processed because it triggered enterprise safety guardrails.\n\n"
                f"- **Detected Policy Violations:** `{flags}`\n"
                f"- **Reason:** {reason}\n"
                f"- **Action Taken:** The event has been logged to the Enterprise Security Operations Center (SOC) audit register in accordance with IT Policy POL-SEC-01.\n\n"
                f"If you believe this was triggered in error, please contact your IT Security Liaison."
            )

        # Case 2: Human Approval Pending
        if technical_response.requires_escalation and technical_response.status != "UNCERTAIN":
            return (
                f"{greeting}\n\n"
                f"🛡️ **Action Requires Human-in-the-Loop Authorization**\n\n"
                f"The requested action involves elevated permissions or privileged system modifications and cannot be completed autonomously.\n\n"
                f"- **Approval Status:** Pending Human Administrator Review\n"
                f"- **Justification:** {technical_response.summary}\n\n"
                f"An escalation ticket has been routed to the Tier-2 IT Infrastructure Team. You will receive an email confirmation once reviewed."
            )

        # Case 3: Anti-Hallucination Uncertainty
        if technical_response.status == "UNCERTAIN":
            return (
                f"{greeting}\n\n"
                f"ℹ️ **Verified Documentation Not Found**\n\n"
                f"Our automated AI Service Desk could not find an officially verified enterprise knowledge base article or diagnostic telemetry matching your specific question.\n\n"
                f"To maintain enterprise safety and prevent hallucinated technical advice, I have refrained from generating unverified commands.\n\n"
                f"📋 **Next Steps:**\n"
                f"1. A Level-2 IT Engineer will be assigned to review your inquiry.\n"
                f"2. You can also visit the self-service IT Portal or call the urgent support hotline at ext. 4357."
            )

        # Case 4: Standard Verified Resolution
        steps_text = "\n".join([f"- {s}" for s in technical_response.data.get("steps", [])])
        device = memories_used.get("assigned_device", "Corporate Laptop")

        tool_notes = ""
        if tool_results:
            tool_notes = "\n\n**Automated System Actions Executed:**\n"
            for t in tool_results:
                tool_notes += f"- `{t.get('tool_source', 'System Tool')}`: {t.get('message', t.get('ticket_id', 'Completed'))}\n"

        response = (
            f"{greeting}\n\n"
            f"Here is the recommended technical guidance based on your profile (**{device}**) and corporate IT documentation:\n\n"
            f"{steps_text}\n"
            f"{tool_notes}\n"
            f"If these steps do not immediately resolve the problem, please reply or request an incident ticket creation."
        )
        return response

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        user_input = context.get("user_input", "")
        intent_data = self.analyze_intent(user_input)

        return AgentResponse(
            agent_name=self.name,
            status="SUCCESS",
            summary=f"Parsed user intent as {intent_data.get('intent')} (Category: {intent_data.get('category')}).",
            data=intent_data,
            confidence=0.95,
            recommendations=["Pass extracted intent and category to Supervisor Agent for dispatch."],
            risk_assessment=RiskLevel.LOW,
            requires_escalation=False
        )

