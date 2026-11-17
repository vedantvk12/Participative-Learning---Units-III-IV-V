"""
Memory Management System
Short-Term (Conversational) and Long-Term (Persistent SQLite) Memory
Multi-Agent Enterprise AI Service Desk
"""

import sqlite3
import re
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.config import DB_PATH, SENSITIVE_DATA_PATTERNS
from core.models import ChatMessage, MessageRole, MemoryRecord


class MemoryManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        # Short-term memory: in-memory conversation buffer
        self.short_term_context: List[ChatMessage] = []
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Long-term persistent memory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS long_term_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    memory_key TEXT NOT NULL,
                    memory_value TEXT NOT NULL,
                    sanitized INTEGER DEFAULT 1,
                    consent_granted INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    UNIQUE(user_id, memory_key)
                )
            """)
            conn.commit()

    # --- Short-Term Memory Methods ---

    def add_short_term_message(self, role: MessageRole, sender: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> ChatMessage:
        msg = ChatMessage(
            id=f"MSG-{len(self.short_term_context) + 1:04d}",
            role=role,
            sender=sender,
            content=self.sanitize_content(content),
            metadata=metadata or {}
        )
        self.short_term_context.append(msg)
        return msg

    def get_short_term_history(self, limit: int = 10) -> List[ChatMessage]:
        return self.short_term_context[-limit:]

    def clear_short_term_memory(self):
        self.short_term_context = []

    # --- Sanitization & Privacy Safeguards ---

    def sanitize_content(self, text: str) -> str:
        """Removes or masks passwords, tokens, SSNs, credit cards before saving to memory."""
        sanitized = text
        for pattern in SENSITIVE_DATA_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED_SENSITIVE_DATA]", sanitized, flags=re.IGNORECASE)
        return sanitized

    # --- Long-Term Memory (Persistent) Methods ---

    def save_long_term_record(self, user_id: str, category: str, key: str, value: str, consent: bool = True) -> bool:
        """Stores approved user preference or historical device configuration into persistent SQLite."""
        if not consent:
            return False
        sanitized_value = self.sanitize_content(value)
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO long_term_memory (user_id, category, memory_key, memory_value, sanitized, consent_granted, created_at, last_accessed)
                VALUES (?, ?, ?, ?, 1, ?, ?, ?)
                ON CONFLICT(user_id, memory_key) DO UPDATE SET
                    memory_value=excluded.memory_value,
                    last_accessed=excluded.last_accessed
            """, (user_id, category, key, sanitized_value, 1 if consent else 0, now, now))
            conn.commit()
            return True

    def get_long_term_records(self, user_id: str, category: Optional[str] = None) -> List[MemoryRecord]:
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if category:
                cursor.execute("""
                    SELECT * FROM long_term_memory WHERE user_id = ? AND category = ?
                """, (user_id, category))
            else:
                cursor.execute("""
                    SELECT * FROM long_term_memory WHERE user_id = ?
                """, (user_id,))
            rows = cursor.fetchall()

            # Update last accessed timestamp
            cursor.execute("""
                UPDATE long_term_memory SET last_accessed = ? WHERE user_id = ?
            """, (now, user_id))
            conn.commit()

            records = []
            for r in rows:
                records.append(MemoryRecord(
                    key=r["memory_key"],
                    user_id=r["user_id"],
                    category=r["category"],
                    value=r["memory_value"],
                    sanitized=bool(r["sanitized"]),
                    created_at=r["created_at"],
                    last_accessed=r["last_accessed"],
                    consent_granted=bool(r["consent_granted"])
                ))
            return records

    def delete_user_memories(self, user_id: str) -> int:
        """Right to be forgotten: removes all persistent memory for a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM long_term_memory WHERE user_id = ?", (user_id,))
            deleted = cursor.rowcount
            conn.commit()
            return deleted

    def seed_default_memories(self, users: List[Dict[str, Any]]):
        """Seeds standard user hardware profiles and preferences into persistent SQLite."""
        for u in users:
            uid = u["user_id"]
            self.save_long_term_record(uid, "hardware", "assigned_device", u.get("assigned_device", "Standard Corporate Laptop"))
            self.save_long_term_record(uid, "hardware", "os_version", u.get("os_version", "Windows 11 Enterprise"))
            self.save_long_term_record(uid, "network", "assigned_subnet", u.get("ip_subnet", "10.14.0.0/16"))
            self.save_long_term_record(uid, "preference", "preferred_vpn_gateway", "vpn.enterprise.internal")
            self.save_long_term_record(uid, "preference", "notification_channel", "Teams and Email")
            self.save_long_term_record(uid, "history", "previous_resolved_issues", "Wi-Fi certificate auto-renewed in August 2026")

