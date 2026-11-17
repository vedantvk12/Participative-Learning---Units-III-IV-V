"""
Service Desk Orchestrator & System Initializer
Multi-Agent Enterprise AI Service Desk
"""

import json
from typing import Dict, Any, List
from core.config import DB_PATH, SYNTHETIC_USERS_PATH, KB_PATH
from core.models import UserProfile
from core.memory import MemoryManager
from core.knowledge_base import KnowledgeBaseEngine
from core.tools import ToolExecutionEngine
from core.audit_logger import AuditLogger
from agents.user_interaction_agent import UserInteractionAgent
from agents.security_compliance_agent import SecurityComplianceAgent
from agents.memory_agent import MemoryKnowledgeAgent
from agents.technical_resolution_agent import TechnicalResolutionAgent
from agents.tool_execution_agent import ToolExecutionAgent
from agents.supervisor_agent import SupervisorAgent


class ServiceDeskSystem:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.audit_logger = AuditLogger(db_path)
        self.kb_engine = KnowledgeBaseEngine(KB_PATH)
        self.memory_manager = MemoryManager(db_path)
        self.tool_engine = ToolExecutionEngine(db_path)

        # Load synthetic users
        self.users: Dict[str, UserProfile] = {}
        self._load_users()

        # Seed long-term memory for users
        self._seed_memories()

        # Initialize Specialized Agents
        self.user_agent = UserInteractionAgent()
        self.security_agent = SecurityComplianceAgent(self.audit_logger)
        self.memory_agent = MemoryKnowledgeAgent(self.memory_manager, self.kb_engine)
        self.tech_agent = TechnicalResolutionAgent()
        self.tool_agent = ToolExecutionAgent(self.tool_engine)

        # Initialize Supervisor Agent
        self.supervisor = SupervisorAgent(
            user_agent=self.user_agent,
            security_agent=self.security_agent,
            memory_agent=self.memory_agent,
            tech_agent=self.tech_agent,
            tool_agent=self.tool_agent,
            audit_logger=self.audit_logger
        )

    def _load_users(self):
        if not SYNTHETIC_USERS_PATH.exists():
            return
        with open(SYNTHETIC_USERS_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            for item in raw:
                u = UserProfile(**item)
                self.users[u.user_id] = u

    def _seed_memories(self):
        user_dicts = [u.model_dump() for u in self.users.values()]
        self.memory_manager.seed_default_memories(user_dicts)

    def get_user(self, user_id: str) -> UserProfile:
        return self.users.get(user_id, list(self.users.values())[0])

    def list_users(self) -> List[UserProfile]:
        return list(self.users.values())
