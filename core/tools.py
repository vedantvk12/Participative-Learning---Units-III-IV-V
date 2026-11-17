"""
Simulated Enterprise IT Tools & Execution Engine
Multi-Agent Enterprise AI Service Desk
"""

import sqlite3
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.config import DB_PATH, SIMULATED_SERVICES, ROLE_PERMISSIONS
from core.models import Ticket, TicketPriority, TicketStatus, ToolCallRecord
from core.knowledge_base import KnowledgeBaseEngine
from core.audit_logger import AuditLogger


class ToolExecutionEngine:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.kb_engine = KnowledgeBaseEngine()
        self.audit_logger = AuditLogger(db_path)
        self._init_tickets_db()

    def _init_tickets_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS support_tickets (
                    ticket_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    user_name TEXT NOT NULL,
                    issue_type TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    resolution_notes TEXT,
                    assigned_agent TEXT,
                    requires_human_approval INTEGER DEFAULT 0,
                    approved_by TEXT
                )
            """)
            conn.commit()

    def _check_permission(self, user_role: str, tool_name: str) -> bool:
        allowed = ROLE_PERMISSIONS.get(user_role, [])
        return tool_name in allowed

    # --- Tool 1: Create Support Ticket ---
    def create_support_ticket(
        self,
        user_id: str,
        user_name: str,
        issue_type: str,
        priority: str,
        description: str,
        assigned_agent: str = "Technical Resolution Agent"
    ) -> Dict[str, Any]:
        """Creates an enterprise support ticket in the simulated IT Service Desk database."""
        ticket_id = f"INC-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now().isoformat()
        prio = priority.upper() if priority.upper() in ["LOW", "MEDIUM", "HIGH", "CRITICAL"] else "MEDIUM"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO support_tickets (ticket_id, user_id, user_name, issue_type, priority, status, description, created_at, assigned_agent)
                VALUES (?, ?, ?, ?, ?, 'OPEN', ?, ?, ?)
            """, (ticket_id, user_id, user_name, issue_type, prio, description, now, assigned_agent))
            conn.commit()

        self.audit_logger.log_event(
            event_type="TOOL_EXECUTION",
            agent_name="Tool Execution Agent",
            user_id=user_id,
            severity="INFO",
            details={"tool": "create_support_ticket", "ticket_id": ticket_id, "priority": prio}
        )

        return {
            "status": "SUCCESS",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - ServiceNow Adapter]",
            "ticket_id": ticket_id,
            "user_id": user_id,
            "issue_type": issue_type,
            "priority": prio,
            "ticket_status": "OPEN",
            "assigned_agent": assigned_agent,
            "created_at": now,
            "message": f"Incident {ticket_id} created successfully and routed to Level-2 Support Queue."
        }

    # --- Tool 2: Search Existing Tickets ---
    def search_existing_tickets(self, user_id: str, ticket_id: Optional[str] = None) -> Dict[str, Any]:
        """Queries tickets for the specified user or ticket ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if ticket_id:
                cursor.execute("SELECT * FROM support_tickets WHERE ticket_id = ?", (ticket_id.upper(),))
            else:
                cursor.execute("SELECT * FROM support_tickets WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (user_id,))
            rows = cursor.fetchall()
            tickets = [dict(r) for r in rows]

        return {
            "status": "SUCCESS",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - ServiceNow Query API]",
            "query_user_id": user_id,
            "match_count": len(tickets),
            "tickets": tickets
        }

    # --- Tool 3: Search IT Knowledge Base ---
    def search_it_knowledge_base(self, query: str, category: Optional[str] = None) -> Dict[str, Any]:
        """Searches curated enterprise IT documentation using semantic retrieval."""
        matches = self.kb_engine.search(query, category=category, top_k=2)
        if not matches:
            return {
                "status": "NO_MATCH",
                "tool_source": "[SIMULATED ENTERPRISE TOOL - Confluence KB Indexer]",
                "query": query,
                "confidence": 0.0,
                "message": "No verified knowledge base articles found matching the query."
            }

        top_match = matches[0]
        article = top_match["article"]
        return {
            "status": "SUCCESS",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - Confluence KB Indexer]",
            "article_id": article.id,
            "title": article.title,
            "category": article.category,
            "relevance_score": top_match["relevance_score"],
            "matched_keywords": top_match["matched_keywords"],
            "solution_steps": article.content,
            "verified": article.verified,
            "last_reviewed": article.last_reviewed
        }

    # --- Tool 4: Check Simulated System Status ---
    def check_system_status(self, service_name: str) -> Dict[str, Any]:
        """Checks real-time operational health of corporate network gateways, SSO, and portals."""
        # Exact or partial match
        matched_key = None
        for key in SIMULATED_SERVICES:
            if service_name.lower() in key.lower() or key.lower() in service_name.lower():
                matched_key = key
                break

        if not matched_key:
            return {
                "status": "UNKNOWN_SERVICE",
                "tool_source": "[SIMULATED ENTERPRISE TOOL - Datadog Synthetic Monitor]",
                "requested_service": service_name,
                "available_services": list(SIMULATED_SERVICES.keys()),
                "message": f"Service '{service_name}' is not monitored in the enterprise telemetry matrix."
            }

        service_data = SIMULATED_SERVICES[matched_key]
        return {
            "status": "SUCCESS",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - Datadog Synthetic Monitor]",
            "service_name": matched_key,
            "operational_status": service_data["status"],
            "latency_ms": service_data["latency_ms"],
            "telemetry_details": service_data["details"],
            "timestamp": datetime.now().isoformat()
        }

    # --- Tool 5: Retrieve Troubleshooting Information ---
    def retrieve_troubleshooting_info(self, issue_code_or_device: str) -> Dict[str, Any]:
        """Retrieves diagnostic checklists and hardware diagnostic codes."""
        code = issue_code_or_device.upper()
        diagnostics = {
            "WIFI-DROP": {
                "category": "Wireless Telemetry",
                "check_points": [
                    "Validate 802.1x RADIUS timeout threshold",
                    "Check roaming aggressiveness in Intel Wi-Fi adapter properties",
                    "Verify machine certificate revocation list (CRL) reachability"
                ],
                "recommended_action": "Flush DNS, refresh DHCP lease, re-sync company certificate."
            },
            "VPN-LATENCY": {
                "category": "Tunneling Telemetry",
                "check_points": [
                    "Ping gateway US-East-02 vs US-East-01",
                    "MTU size mismatch (default 1406 vs standard 1500)",
                    "ISP UDP 4500 encapsulation throttle"
                ],
                "recommended_action": "Failover to alternate gateway 'vpn-backup.enterprise.internal'."
            },
            "DELL LATITUDE 7420": {
                "category": "Hardware Profile Diagnostics",
                "check_points": [
                    "Intel Wi-Fi 6 AX201 driver revision 22.190.0 or higher",
                    "Dell Command | Update BIOS version 1.28.0",
                    "Thunderbolt dock firmware WD19S"
                ],
                "recommended_action": "Verify driver package via Intune Endpoint Manager."
            }
        }

        for k, v in diagnostics.items():
            if k in code or code in k:
                return {
                    "status": "SUCCESS",
                    "tool_source": "[SIMULATED ENTERPRISE TOOL - Endpoint Diagnostic Engine]",
                    "target": k,
                    "diagnostic_data": v
                }

        return {
            "status": "PARTIAL",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - Endpoint Diagnostic Engine]",
            "target": issue_code_or_device,
            "message": f"Standard hardware diagnostics query returned generic Windows 11 Enterprise checklist."
        }

    # --- Tool 6: Escalate for Human Approval ---
    def escalate_for_human_approval(
        self,
        action_type: str,
        required_role: str,
        context: Dict[str, Any],
        justification: str
    ) -> Dict[str, Any]:
        """Creates a pending human-in-the-loop escalation approval request."""
        approval_id = f"APPRV-{uuid.uuid4().hex[:6].upper()}"
        now = datetime.now().isoformat()

        self.audit_logger.log_event(
            event_type="HUMAN_IN_THE_LOOP_ESCALATION",
            agent_name="Security & Compliance Agent",
            user_id=context.get("user_id", "UNKNOWN"),
            severity="WARNING",
            details={
                "approval_id": approval_id,
                "action_type": action_type,
                "required_role": required_role,
                "justification": justification
            },
            risk_mitigation="Execution halted; awaiting authorized human signature"
        )

        return {
            "status": "PENDING_HUMAN_APPROVAL",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - Governance Approval Workflow]",
            "approval_id": approval_id,
            "action_type": action_type,
            "required_role": required_role,
            "justification": justification,
            "submitted_at": now,
            "verdict": "ACTION_BLOCKED_PENDING_APPROVAL",
            "instructions": f"A notification has been dispatched to {required_role} for review. Automated execution suspended."
        }

    # --- Privileged Action Demonstrator (For Safety Testing) ---
    def restart_enterprise_service(self, service_name: str, user_role: str) -> Dict[str, Any]:
        """Privileged administrative tool to demonstrate RBAC rejection."""
        if not self._check_permission(user_role, "restart_enterprise_service"):
            self.audit_logger.log_event(
                event_type="UNAUTHORIZED_TOOL_ATTEMPT",
                agent_name="Security and Compliance Agent",
                user_id=user_role,
                severity="HIGH",
                details={"tool": "restart_enterprise_service", "service": service_name, "user_role": user_role},
                risk_mitigation="Access Denied by RBAC Policy Rule SEC-04"
            )
            return {
                "status": "DENIED",
                "tool_source": "[SIMULATED ENTERPRISE TOOL - Enterprise Hypervisor Gateway]",
                "error": "HTTP 403 Forbidden: Caller lacks SYS_ADMIN authorization to restart enterprise services.",
                "policy_violation": "Least-Privilege Enforcement (RBAC-SEC-04)",
                "action_taken": "Execution blocked and reported to Security Operations Center (SOC)."
            }

        return {
            "status": "SUCCESS",
            "tool_source": "[SIMULATED ENTERPRISE TOOL - Enterprise Hypervisor Gateway]",
            "service_name": service_name,
            "message": f"Service '{service_name}' gracefully restarted by authorized SYS_ADMIN."
        }

