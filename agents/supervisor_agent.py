"""
Supervisor Agent (Central Orchestrator & Conflict Resolver)
Multi-Agent Enterprise AI Service Desk
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from agents.user_interaction_agent import UserInteractionAgent
from agents.security_compliance_agent import SecurityComplianceAgent
from agents.memory_agent import MemoryKnowledgeAgent
from agents.technical_resolution_agent import TechnicalResolutionAgent
from agents.tool_execution_agent import ToolExecutionAgent
from core.models import AgentResponse, RiskLevel, ExecutionTrace, ExecutionTraceStep
from core.audit_logger import AuditLogger


class SupervisorAgent(BaseAgent):
    def __init__(
        self,
        user_agent: UserInteractionAgent,
        security_agent: SecurityComplianceAgent,
        memory_agent: MemoryKnowledgeAgent,
        tech_agent: TechnicalResolutionAgent,
        tool_agent: ToolExecutionAgent,
        audit_logger: AuditLogger
    ):
        super().__init__(
            name="Supervisor Agent",
            role="System Orchestration, Task Delegation, Conflict Arbitration, and Output Gatekeeping",
            description="Controls the multi-agent control loop, manages inter-agent message routing, arbitrates conflicts, enforces guardrail precedence, and audits execution traces."
        )
        self.user_agent = user_agent
        self.security_agent = security_agent
        self.memory_agent = memory_agent
        self.tech_agent = tech_agent
        self.tool_agent = tool_agent
        self.audit_logger = audit_logger

    def resolve_conflicts(
        self,
        security_resp: AgentResponse,
        tech_resp: AgentResponse,
        tool_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Conflict Resolution Logic:
        Enforces hierarchical precedence: Security & Compliance > Availability > Performance.
        Detects if Technical Agent wants to perform an action that Security flags or where tools failed.
        """
        conflict_detected = False
        details = None
        arbitrated_verdict = "CONSENSUS_REACHED"

        # Conflict Case A: Technical Agent wants automated resolution, but Security Agent flags High/Critical risk
        if security_resp.risk_assessment in [RiskLevel.HIGH, RiskLevel.CRITICAL] and tech_resp.status == "RESOLVED":
            conflict_detected = True
            details = (
                "Conflict detected between Technical Resolution Agent (proposing automated change) "
                "and Security & Compliance Agent (flagging high security/policy risk). "
                "Supervisor Decision: Security precedence policy overrides technical resolution; halting automated execution."
            )
            arbitrated_verdict = "SECURITY_OVERRIDE"

        # Conflict Case B: Tool execution failure vs optimistic technical resolution
        for t in tool_results:
            if t.get("status") in ["DENIED", "ERROR"] and tech_resp.status == "RESOLVED":
                conflict_detected = True
                details = (
                    f"Conflict detected: Technical Resolution Agent anticipated successful tool outcome, "
                    f"but Tool Execution Agent reported failure '{t.get('status')}'. "
                    f"Supervisor Decision: Downgrading technical status to ESCALATE_HUMAN."
                )
                arbitrated_verdict = "TOOL_FAILURE_OVERRIDE"
                break

        return {
            "conflict_detected": conflict_detected,
            "details": details,
            "verdict": arbitrated_verdict
        }

    def process_request(
        self,
        user_input: str,
        user_profile: Dict[str, Any],
        target_user_id: Optional[str] = None,
        simulate_conflict: bool = False
    ) -> ExecutionTrace:
        start_time = time.time()
        trace_id = f"TRACE-{uuid.uuid4().hex[:8].upper()}"
        steps: List[ExecutionTraceStep] = []
        user_id = user_profile.get("user_id", "ANONYMOUS")
        user_name = user_profile.get("name", "Employee")
        user_role = user_profile.get("role", "EMPLOYEE")

        # --- STEP 1: Front-End Intent Elicitation (User Interaction Agent) ---
        user_context = {"user_input": user_input, "user_profile": user_profile}
        user_agent_resp = self.user_agent.process(user_context)
        steps.append(self.create_trace_step(
            step_number=1,
            action_type="INTENT_ANALYSIS",
            description="User Interaction Agent parsed input intent and categorized issue.",
            inputs={"raw_text": user_input},
            outputs=user_agent_resp.data
        ))

        # --- STEP 2: Security & Compliance Guardrail Check ---
        sec_context = {
            "user_input": user_input,
            "user_profile": user_profile,
            "target_user_id": target_user_id
        }
        sec_resp = self.security_agent.process(sec_context)
        steps.append(self.create_trace_step(
            step_number=2,
            action_type="SECURITY_INSPECTION",
            description="Security and Compliance Agent checked prompt injection, PII patterns, and RBAC.",
            inputs=sec_context,
            outputs=sec_resp.data,
            status="SUCCESS" if sec_resp.status == "APPROVED" else "BLOCKED"
        ))

        # Early termination if critical security violation
        if sec_resp.status == "BLOCKED":
            final_reply = self.user_agent.format_final_response(
                user_name=user_name,
                technical_response=AgentResponse(
                    agent_name="Technical Resolution Agent",
                    status="HALTED",
                    summary="Execution halted by Security Agent",
                    risk_assessment=sec_resp.risk_assessment
                ),
                tool_results=[],
                memories_used={},
                security_assessment=sec_resp.data
            )
            elapsed = (time.time() - start_time) * 1000
            return ExecutionTrace(
                trace_id=trace_id,
                request_text=user_input,
                user_id=user_id,
                steps=steps,
                supervisor_verdict="BLOCKED_BY_SECURITY",
                conflict_detected=False,
                conflict_details="Execution stopped at Step 2 due to security policy violation.",
                final_output=final_reply,
                total_time_ms=round(elapsed, 2)
            )

        # --- STEP 3: Memory & Knowledge Retrieval ---
        mem_context = {
            "user_id": user_id,
            "user_input": user_input,
            "intent": user_agent_resp.data.get("intent")
        }
        mem_resp = self.memory_agent.process(mem_context)
        steps.append(self.create_trace_step(
            step_number=3,
            action_type="MEMORY_KNOWLEDGE_RETRIEVAL",
            description="Memory and Knowledge Agent retrieved conversational history, persistent profile, and KB articles.",
            inputs={"user_id": user_id, "query": user_input},
            outputs={
                "long_term_memories": mem_resp.data.get("long_term_memories"),
                "kb_match_count": len(mem_resp.data.get("kb_matches", []))
            }
        ))

        # --- STEP 4: System Telemetry / Tool Pre-check ---
        tool_results = []
        system_status = {}
        intent = user_agent_resp.data.get("intent", "")

        # If network issue, check VPN or Wi-Fi status
        if "NETWORK" in intent:
            status_tool_resp = self.tool_agent.execute_tool(
                tool_name="check_system_status",
                parameters={"service_name": "VPN Gateway" if "VPN" in intent else "Enterprise Wi-Fi (CorpNet-Secure)"},
                user_role=user_role
            )
            system_status = status_tool_resp
            tool_results.append(status_tool_resp)
            steps.append(self.create_trace_step(
                step_number=4,
                action_type="TELEMETRY_CHECK",
                description="Tool Execution Agent queried real-time enterprise service status.",
                inputs={"service_name": status_tool_resp.get("service_name")},
                outputs=status_tool_resp
            ))

        # --- STEP 5: Technical Resolution Synthesis ---
        tech_context = {
            "user_input": user_input,
            "memory_data": mem_resp.data,
            "system_status": system_status
        }
        tech_resp = self.tech_agent.process(tech_context)
        steps.append(self.create_trace_step(
            step_number=5,
            action_type="TECHNICAL_SYNTHESIS",
            description="Technical Resolution Agent formulated troubleshooting steps or flagged uncertainty.",
            inputs={"device": mem_resp.data.get("assigned_device"), "kb_found": bool(mem_resp.data.get("kb_matches"))},
            outputs=tech_resp.data,
            status=tech_resp.status
        ))

        # --- STEP 6: Automated Ticket Creation or Tool Action (If applicable) ---
        if tech_resp.status == "RESOLVED":
            ticket_tool_resp = self.tool_agent.execute_tool(
                tool_name="create_support_ticket",
                parameters={
                    "user_id": user_id,
                    "user_name": user_name,
                    "issue_type": user_agent_resp.data.get("category", "General IT"),
                    "priority": "HIGH" if "DEGRADED" in str(system_status) else "MEDIUM",
                    "description": f"{user_input} [Assigned Device: {mem_resp.data.get('assigned_device')}]"
                },
                user_role=user_role
            )
            tool_results.append(ticket_tool_resp)
            steps.append(self.create_trace_step(
                step_number=6,
                action_type="AUTOMATED_TICKET_DISPATCH",
                description="Tool Execution Agent automatically created tracking incident ticket.",
                inputs={"user_id": user_id, "priority": ticket_tool_resp.get("priority")},
                outputs=ticket_tool_resp
            ))

        # --- STEP 7: Conflict Resolution & Supervisor Arbitration ---
        if simulate_conflict:
            # Force simulated conflict for experiment 5
            tech_resp = AgentResponse(
                agent_name="Technical Resolution Agent",
                status="RESOLVED",
                summary="Recommended immediate emergency gateway reboot and firewall bypass.",
                data={"steps": ["Force restart VPN gateway remotely", "Disable local endpoint firewall"]},
                confidence=0.85,
                risk_assessment=RiskLevel.HIGH
            )
            sec_resp = AgentResponse(
                agent_name="Security and Compliance Agent",
                status="BLOCKED",
                summary="Prohibited: Disabling endpoint firewall and uncoordinated gateway restarts violate enterprise security baseline SEC-09.",
                data={"flags": ["POLICY_SECURITY_BASELINE_BREACH"]},
                confidence=0.99,
                risk_assessment=RiskLevel.CRITICAL
            )

        conflict_eval = self.resolve_conflicts(sec_resp, tech_resp, tool_results)
        steps.append(self.create_trace_step(
            step_number=7,
            action_type="SUPERVISOR_ARBITRATION",
            description="Supervisor Agent evaluated all agent outputs for conflicts and applied policy precedence.",
            inputs={"security_status": sec_resp.status, "tech_status": tech_resp.status},
            outputs=conflict_eval
        ))

        # --- STEP 8: Final Response Formatting (User Interaction Agent) ---
        if conflict_eval["conflict_detected"] and conflict_eval["verdict"] == "SECURITY_OVERRIDE":
            final_reply = (
                f"Hello {user_name},\n\n"
                f"⚖️ **Supervisor Multi-Agent Conflict Arbitration Applied**\n\n"
                f"A conflict was identified between the Technical Resolution Agent and Security Agent:\n"
                f"- **Technical Recommendation:** Automated aggressive gateway reboot / security bypass.\n"
                f"- **Security Constraint:** Disabling firewalls or restarting production gateways violates SEC-09 without change approval.\n\n"
                f"**Supervisor Ruling:** Enforcing Security Precedence Policy. Automated override was aborted. "
                f"The incident has been safely escalated to Senior Network Engineering for scheduled maintenance review."
            )
        else:
            final_reply = self.user_agent.format_final_response(
                user_name=user_name,
                technical_response=tech_resp,
                tool_results=tool_results,
                memories_used=mem_resp.data.get("long_term_memories", {}),
                security_assessment=sec_resp.data
            )

        # Save to short-term memory buffer
        self.memory_agent.memory_manager.add_short_term_message(
            role="USER", sender=user_name, content=user_input
        )
        self.memory_agent.memory_manager.add_short_term_message(
            role="ASSISTANT", sender="Enterprise AI Service Desk", content=final_reply
        )

        elapsed = (time.time() - start_time) * 1000

        self.audit_logger.log_event(
            event_type="WORKFLOW_COMPLETED",
            agent_name=self.name,
            user_id=user_id,
            severity="INFO",
            details={
                "trace_id": trace_id,
                "conflict_detected": conflict_eval["conflict_detected"],
                "total_time_ms": round(elapsed, 2)
            }
        )

        return ExecutionTrace(
            trace_id=trace_id,
            request_text=user_input,
            user_id=user_id,
            steps=steps,
            supervisor_verdict=conflict_eval["verdict"],
            conflict_detected=conflict_eval["conflict_detected"],
            conflict_details=conflict_eval["details"],
            final_output=final_reply,
            total_time_ms=round(elapsed, 2)
        )

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """Standard process interface required by BaseAgent."""
        trace = self.process_request(
            user_input=context.get("user_input", ""),
            user_profile=context.get("user_profile", {}),
            target_user_id=context.get("target_user_id"),
            simulate_conflict=context.get("simulate_conflict", False)
        )
        return AgentResponse(
            agent_name=self.name,
            status="SUCCESS",
            summary=f"Workflow completed under trace {trace.trace_id} with verdict {trace.supervisor_verdict}.",
            data=trace.model_dump(),
            confidence=1.0,
            risk_assessment=RiskLevel.LOW
        )
