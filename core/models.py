"""
Data Models & Schemas
Multi-Agent Enterprise AI Service Desk
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    IT_SPECIALIST = "IT_SPECIALIST"
    SYS_ADMIN = "SYS_ADMIN"


class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    role: UserRole
    department: str
    assigned_device: str
    os_version: str
    ip_subnet: str
    allowed_tools: List[str] = Field(default_factory=list)


class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    AGENT = "AGENT"


class ChatMessage(BaseModel):
    id: str
    role: MessageRole
    sender: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Ticket(BaseModel):
    ticket_id: str
    user_id: str
    user_name: str
    issue_type: str
    priority: TicketPriority
    status: TicketStatus
    description: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    resolution_notes: Optional[str] = None
    assigned_agent: Optional[str] = None
    requires_human_approval: bool = False
    approved_by: Optional[str] = None


class KBArticle(BaseModel):
    id: str
    category: str
    title: str
    keywords: List[str]
    content: str
    verified: bool = True
    last_reviewed: str


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SecurityValidationResult(BaseModel):
    is_safe: bool
    risk_level: RiskLevel
    flags: List[str] = Field(default_factory=list)
    reason: Optional[str] = None
    sanitized_input: str
    requires_escalation: bool = False


class ToolCallRecord(BaseModel):
    call_id: str
    tool_name: str
    parameters: Dict[str, Any]
    authorized: bool
    result: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    user_id: str
    executed_by_agent: str


class AgentResponse(BaseModel):
    agent_name: str
    status: str
    summary: str
    data: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    recommendations: List[str] = Field(default_factory=list)
    risk_assessment: RiskLevel = RiskLevel.LOW
    requires_escalation: bool = False
    execution_time_ms: float = 0.0


class ExecutionTraceStep(BaseModel):
    step_number: int
    agent_name: str
    action_type: str
    description: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    status: str = "SUCCESS"


class ExecutionTrace(BaseModel):
    trace_id: str
    request_text: str
    user_id: str
    steps: List[ExecutionTraceStep] = Field(default_factory=list)
    supervisor_verdict: str = ""
    conflict_detected: bool = False
    conflict_details: Optional[str] = None
    final_output: str = ""
    total_time_ms: float = 0.0


class MemoryRecord(BaseModel):
    key: str
    user_id: str
    category: str  # 'preference', 'hardware', 'historical_issue', 'device_config'
    value: str
    sanitized: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    last_accessed: str = Field(default_factory=lambda: datetime.now().isoformat())
    consent_granted: bool = True

