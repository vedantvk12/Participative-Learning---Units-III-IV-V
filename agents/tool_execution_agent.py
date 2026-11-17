"""
Tool Execution Agent
Multi-Agent Enterprise AI Service Desk
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.models import AgentResponse, RiskLevel
from core.tools import ToolExecutionEngine


class ToolExecutionAgent(BaseAgent):
    def __init__(self, tool_engine: ToolExecutionEngine):
        super().__init__(
            name="Tool Execution Agent",
            role="Deterministic Tool Invocation and Output Marshalling",
            description="Validates tool input parameters, executes approved enterprise tools in a sandboxed simulator, and records execution audit trails."
        )
        self.tool_engine = tool_engine

    def execute_tool(self, tool_name: str, parameters: Dict[str, Any], user_role: str = "EMPLOYEE") -> Dict[str, Any]:
        # Validate permissions
        if not self.tool_engine._check_permission(user_role, tool_name):
            return {
                "status": "DENIED",
                "error": f"Authorization Error: Role '{user_role}' is not granted execution rights for tool '{tool_name}'.",
                "policy": "Least-Privilege RBAC Matrix"
            }

        # Dispatch
        if tool_name == "create_support_ticket":
            return self.tool_engine.create_support_ticket(
                user_id=parameters.get("user_id", "UNKNOWN"),
                user_name=parameters.get("user_name", "Unknown Employee"),
                issue_type=parameters.get("issue_type", "General IT Inquiry"),
                priority=parameters.get("priority", "MEDIUM"),
                description=parameters.get("description", "No description provided.")
            )
        elif tool_name == "search_existing_tickets":
            return self.tool_engine.search_existing_tickets(
                user_id=parameters.get("user_id", "UNKNOWN"),
                ticket_id=parameters.get("ticket_id")
            )
        elif tool_name == "search_it_knowledge_base":
            return self.tool_engine.search_it_knowledge_base(
                query=parameters.get("query", ""),
                category=parameters.get("category")
            )
        elif tool_name == "check_system_status":
            return self.tool_engine.check_system_status(
                service_name=parameters.get("service_name", "VPN Gateway")
            )
        elif tool_name == "retrieve_troubleshooting_info":
            return self.tool_engine.retrieve_troubleshooting_info(
                issue_code_or_device=parameters.get("issue_code_or_device", "")
            )
        elif tool_name == "escalate_for_human_approval":
            return self.tool_engine.escalate_for_human_approval(
                action_type=parameters.get("action_type", "PRIVILEGED_ACTION"),
                required_role=parameters.get("required_role", "IT_ADMIN"),
                context=parameters.get("context", {}),
                justification=parameters.get("justification", "User requested elevated change.")
            )
        elif tool_name == "restart_enterprise_service":
            return self.tool_engine.restart_enterprise_service(
                service_name=parameters.get("service_name", "VPN Gateway"),
                user_role=user_role
            )
        else:
            return {
                "status": "ERROR",
                "error": f"Unknown tool '{tool_name}'."
            }

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        tool_name = context.get("tool_name", "")
        params = context.get("parameters", {})
        user_role = context.get("user_role", "EMPLOYEE")

        result = self.execute_tool(tool_name, params, user_role)
        status = "SUCCESS" if result.get("status") == "SUCCESS" else "DENIED" if result.get("status") == "DENIED" else "COMPLETED"

        risk = RiskLevel.LOW
        if result.get("status") == "DENIED":
            risk = RiskLevel.HIGH

        return AgentResponse(
            agent_name=self.name,
            status=status,
            summary=f"Executed tool '{tool_name}' with status: {status}.",
            data={
                "tool_name": tool_name,
                "parameters": params,
                "tool_output": result
            },
            confidence=1.0 if status == "SUCCESS" else 0.3,
            recommendations=["Verify tool execution outcome before final response formatting"],
            risk_assessment=risk,
            requires_escalation=(result.get("status") == "PENDING_HUMAN_APPROVAL")
        )

