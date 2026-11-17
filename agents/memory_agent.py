"""
Memory and Knowledge Agent
Multi-Agent Enterprise AI Service Desk
"""

from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.models import AgentResponse, RiskLevel
from core.memory import MemoryManager
from core.knowledge_base import KnowledgeBaseEngine


class MemoryKnowledgeAgent(BaseAgent):
    def __init__(self, memory_manager: MemoryManager, kb_engine: KnowledgeBaseEngine):
        super().__init__(
            name="Memory and Knowledge Agent",
            role="Context Maintenance, Persistent Memory Retrieval, and KB Search",
            description="Maintains short-term dialog state, recalls long-term user settings and hardware profiles from SQLite, and semantically queries corporate documentation."
        )
        self.memory_manager = memory_manager
        self.kb_engine = kb_engine

    def process(self, context: Dict[str, Any]) -> AgentResponse:
        user_id = context.get("user_id", "")
        query = context.get("user_input", "")

        # 1. Fetch short-term context (recent dialog turns)
        short_term_history = self.memory_manager.get_short_term_history(limit=5)

        # 2. Fetch long-term persistent memories from SQLite
        long_term_records = self.memory_manager.get_long_term_records(user_id=user_id)
        memories_dict = {m.key: m.value for m in long_term_records}

        # 3. Perform semantic KB search
        kb_matches = self.kb_engine.search(query, top_k=2)

        retrieved_articles = []
        confidence = 0.5
        if kb_matches:
            top_match = kb_matches[0]
            confidence = top_match["relevance_score"]
            for m in kb_matches:
                retrieved_articles.append({
                    "id": m["article"].id,
                    "title": m["article"].title,
                    "relevance": m["relevance_score"],
                    "content_snippet": m["article"].content[:200] + "..."
                })

        summary = f"Retrieved {len(short_term_history)} short-term turns, {len(long_term_records)} long-term profile records, and {len(retrieved_articles)} relevant KB articles."

        return AgentResponse(
            agent_name=self.name,
            status="SUCCESS",
            summary=summary,
            data={
                "short_term_turn_count": len(short_term_history),
                "long_term_memories": memories_dict,
                "assigned_device": memories_dict.get("assigned_device", "Corporate Workstation"),
                "preferred_gateway": memories_dict.get("preferred_vpn_gateway", "vpn.enterprise.internal"),
                "kb_matches": retrieved_articles,
                "top_kb_article": kb_matches[0]["article"].model_dump() if kb_matches else None
            },
            confidence=confidence,
            recommendations=[f"Use {memories_dict.get('assigned_device', 'device')} context for targeted diagnostic commands"],
            risk_assessment=RiskLevel.LOW,
            requires_escalation=False
        )
