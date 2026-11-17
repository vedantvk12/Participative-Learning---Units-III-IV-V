"""
System Configuration & Constants
Multi-Agent Enterprise AI Service Desk
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = DATA_DIR / "service_desk.db"
KB_PATH = DATA_DIR / "enterprise_kb.json"
SYNTHETIC_USERS_PATH = DATA_DIR / "synthetic_users.json"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Application Metadata
APP_TITLE = "Multi-Agent Enterprise AI Service Desk"
APP_SUBTITLE = "Units III, IV & V — Memory, Tools, Multi-Agent Collaboration & Governance"
STUDENT_NAME = "Vedant Sattejkumar Kirange"
ROLL_NUMBER = "55"
ENROLLMENT_NO = "ADT23SOCB1294"

# Security & Compliance Constants
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"reveal\s+(all\s+)?(stored|employee|internal|confidential|secret)",
    r"system\s+override",
    r"bypass\s+(security|governance|rbac|guardrail)",
    r"sudo\s+su",
    r"dump\s+(database|credentials|passwords|tokens)",
    r"disregard\s+(your\s+)?guidelines",
    r"you\s+are\s+now\s+in\s+developer\s+mode",
    r"jailbreak",
]

SENSITIVE_DATA_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",       # SSN
    r"\b(?:\d{4}-){3}\d{4}\b",     # Credit card
    r"password\s*[:=]\s*\S+",      # Plaintext password
    r"api[-_]?key\s*[:=]\s*\S+",   # API key
    r"bearer\s+[a-zA-Z0-9_\-\.]+", # Token
    r"private[-_]?key",             # Private keys
]

# Simulated Enterprise Services
SIMULATED_SERVICES = {
    "VPN Gateway": {"status": "DEGRADED", "latency_ms": 284, "details": "High packet loss observed on Node-US-East-02; maintenance scheduled"},
    "Active Directory / SSO": {"status": "OPERATIONAL", "latency_ms": 18, "details": "All domain controllers synchronized and healthy"},
    "Enterprise Wi-Fi (CorpNet-Secure)": {"status": "OPERATIONAL", "latency_ms": 12, "details": "802.1x RADIUS authentication operational"},
    "Office 365 Exchange": {"status": "OPERATIONAL", "latency_ms": 42, "details": "Mail routing and calendar synchronization nominal"},
    "Self-Service Software Portal": {"status": "OPERATIONAL", "latency_ms": 25, "details": "Repository mirror synced"},
    "HR Workday Portal": {"status": "OPERATIONAL", "latency_ms": 65, "details": "SSO federation active"},
}

# Role-Based Access Control (RBAC) Tool Permissions
ROLE_PERMISSIONS = {
    "EMPLOYEE": [
        "search_it_knowledge_base",
        "search_existing_tickets",
        "create_support_ticket",
        "check_system_status",
        "retrieve_troubleshooting_info"
    ],
    "IT_SPECIALIST": [
        "search_it_knowledge_base",
        "search_existing_tickets",
        "create_support_ticket",
        "check_system_status",
        "retrieve_troubleshooting_info",
        "escalate_for_human_approval",
        "reset_network_adapter_remote",
        "reissue_wifi_cert"
    ],
    "SYS_ADMIN": [
        "search_it_knowledge_base",
        "search_existing_tickets",
        "create_support_ticket",
        "check_system_status",
        "retrieve_troubleshooting_info",
        "escalate_for_human_approval",
        "reset_network_adapter_remote",
        "reissue_wifi_cert",
        "modify_user_role",
        "restart_enterprise_service"
    ]
}

