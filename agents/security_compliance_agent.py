"""
Security and Compliance Agent
Multi-Agent Enterprise AI Service Desk
"""

import re
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.models import AgentResponse, RiskLevel, SecurityValidationResult
from core.config import PROMPT_INJECTION_PATTERNS, SENSITIVE_DATA_PATTERNS
from core.audit_logger import AuditLogger


class SecurityComplianceAgent(BaseAgent):
    def __init__(self, audit_logger: AuditLogger):
        super().__init__(
            name="Security and Compliance Agent",
            role="Guardrails, Prompt-Injection Defense, RBAC, and Data Privacy",
            description="Inspects user requests and agent communications to detect injection, unauthorized tool use, PII exposure, and policy violations."
        )
        self.audit_logger = audit_logger

    def validate_request(self, text: str, user_profile: Dict[str, Any], requested_target_user: str = None) -> SecurityValidationResult:
        flags = []
        risk = RiskLevel.LOW
        reason = None
        requires_escalation = False

        # 1. Prompt Injection Detection
        lower_text = text.lower()
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, lower_text):
                flags.append("PROMPT_INJECTION_DETECTED")
                risk = RiskLevel.CRITICAL
                reason = f"Security rule violation: Input triggered prompt injection signature matching '{pattern}'."
                break

        # 2. Cross-User Privacy Breach Check
        user_id = user_profile.get("user_id", "")
        user_role = user_profile.get("role", "EMPLOYEE")
        if requested_target_user and requested_target_user != user_id:
            if user_role not in ["IT_SPECIALIST", "SYS_ADMIN"]:
                flags.append("CROSS_USER_DATA_ACCESS_VIOLATION")
                risk = RiskLevel.HIGH
                reason = f"Privacy violation: Employee {user_id} attempted unauthorized access to data belonging to {requested_target_user}."

        # Check if text tries to query another employee's records
        emp_match = re.search(r"\b(emp-\d{4}|admin-\d{4})\b", lower_text)
        if emp_match:
            targeted = emp_match.group(1).upper()
            if targeted != user_id.upper() and user_role not in ["IT_SPECIALIST", "SYS_ADMIN"]:
                flags.append("UNAUTHORIZED_PEER_LOOKUP")
                risk = RiskLevel.HIGH
                reason = f"Data minimization violation: User {user_id} is not permitted to query records of {targeted}."

        # 3. Sensitive Data / Credential Leakage Check
        for p in SENSITIVE_DATA_PATTERNS:
            if re.search(p, text, re.IGNORECASE):
                flags.append("SENSITIVE_CREDENTIAL_PATTERN")
                if risk != RiskLevel.CRITICAL:
                    risk = RiskLevel.MEDIUM
                reason = (reason or "") + " Warning: Sensitive credential/key pattern identified in message."

        # 4. Privileged Administrative Operation Attempt
        admin_keywords = ["restart server", "restart service", "drop table", "format drive", "override rbac", "grant admin", "elevate privilege"]
        for ak in admin_keywords:
            if ak in lower_text and user_role != "SYS_ADMIN":
                flags.append("UNAUTHORIZED_PRIVILEGED_ACTION")
                risk = RiskLevel.HIGH
                requires_escalation = True
                reason = f"Access Control: Operation '{ak}' requires elevated SYS_ADMIN privileges."

        # Sanitize text
        sanitized = text
        for p in SENSITIVE_DATA_PATTERNS:
            sanitized = re.sub(p, "[REDACTED_BY_SECURITY_AGENT]", sanitized, flags=re.IGNORECASE)

        is_safe = (risk == RiskLevel.LOW or risk == RiskLevel.MEDIUM and not requires_escalation)
        if "PROMPT_INJECTION_DETECTED" in flags or "CROSS_USER_DATA_ACCESS_VIOLATION" in flags:
            is_safe = False

        # Log event if risk is medium, high, or critical
        if risk != RiskLevel.LOW:
            self.audit_logger.log_event(
                event_type="SECURITY_RISK_DETECTED",
                agent_name=self.name,
                user_id=user_id,
                severity=risk.value,
                details={"flags": flags, "reason": reason, "raw_snippet": text[:100]},
                risk_mitigation="Blocked by Security Guardrail Policy SEC-01"
            )

        return SecurityValidationResult(
            is_safe=is_safe,
            risk_level=risk,
            flags=flags,
            reason=reason,
            sanitized_input=sanitized,
            requires_escalation=requires_escalation
        )

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        text = context.get("user_input", "")
        user_profile = context.get("user_profile", {})
        requested_target = context.get("target_user_id")

        val = self.validate_request(text, user_profile, requested_target)

        if not val.is_safe:
            return AgentResponse(
                agent_name=self.name,
                status="BLOCKED",
                summary="Request blocked by security guardrails.",
                data={
                    "is_safe": False,
                    "risk_level": val.risk_level.value,
                    "flags": val.flags,
                    "reason": val.reason
                },
                confidence=1.0,
                recommendations=["Reject execution", "Log security alert", "Notify incident response team"],
                risk_assessment=val.risk_level,
                requires_escalation=val.requires_escalation
            )

        return AgentResponse(
            agent_name=self.name,
            status="APPROVED",
            summary="Request cleared security inspection. No injection, privacy violations, or privilege escalation detected.",
            data={
                "is_safe": True,
                "risk_level": val.risk_level.value,
                "sanitized_text": val.sanitized_input,
                "flags": val.flags
            },
            confidence=0.98,
            recommendations=["Proceed with standard workflow"],
            risk_assessment=val.risk_level,
            requires_escalation=val.requires_escalation
        )

