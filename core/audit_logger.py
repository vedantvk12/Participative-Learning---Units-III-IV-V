"""
Audit Logger & Compliance Tracking
Multi-Agent Enterprise AI Service Desk
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.config import DB_PATH


class AuditLogger:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    details TEXT NOT NULL,
                    risk_mitigation TEXT
                )
            """)
            conn.commit()

    def log_event(self, event_type: str, agent_name: str, user_id: str, severity: str, details: Dict[str, Any], risk_mitigation: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_logs (timestamp, event_type, agent_name, user_id, severity, details, risk_mitigation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().isoformat(),
                event_type,
                agent_name,
                user_id,
                severity,
                json.dumps(details, ensure_ascii=False),
                risk_mitigation or ""
            ))
            conn.commit()

    def get_recent_logs(self, limit: int = 50, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if user_id:
                cursor.execute("""
                    SELECT * FROM audit_logs WHERE user_id = ? ORDER BY id DESC LIMIT ?
                """, (user_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM audit_logs ORDER BY id DESC LIMIT ?
                """, (limit,))
            rows = cursor.fetchall()
            logs = []
            for r in rows:
                item = dict(r)
                try:
                    item["details"] = json.loads(item["details"])
                except Exception:
                    pass
                logs.append(item)
            return logs

