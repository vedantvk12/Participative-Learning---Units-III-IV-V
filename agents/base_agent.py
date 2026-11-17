"""
Base Agent Definition & Communication Protocols
Multi-Agent Enterprise AI Service Desk
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from core.models import AgentResponse, RiskLevel, ExecutionTraceStep


class BaseAgent(ABC):
    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """Processes the assigned sub-task and returns an AgentResponse."""
        pass

    def create_trace_step(
        self,
        step_number: int,
        action_type: str,
        description: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        status: str = "SUCCESS"
    ) -> ExecutionTraceStep:
        return ExecutionTraceStep(
            step_number=step_number,
            agent_name=self.name,
            action_type=action_type,
            description=description,
            inputs=inputs,
            outputs=outputs,
            status=status,
            timestamp=datetime.now().isoformat()
        )

