"""
Enterprise IT Knowledge Base & Semantic Search Engine
Multi-Agent Enterprise AI Service Desk
"""

import json
import re
import math
from typing import List, Dict, Any, Optional
from collections import Counter
from core.config import KB_PATH
from core.models import KBArticle


class KnowledgeBaseEngine:
    def __init__(self, kb_file=KB_PATH):
        self.kb_file = kb_file
        self.articles: List[KBArticle] = []
        self._load_articles()

    def _load_articles(self):
        if not self.kb_file.exists():
            self.articles = []
            return
        with open(self.kb_file, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            self.articles = [KBArticle(**item) for item in raw_data]

    def _tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
        # Filter common stopwords
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
            "this", "that", "these", "those", "it", "its", "as", "can", "if", "not"
        }
        return [t for t in tokens if t not in stopwords]

    def search(self, query: str, category: Optional[str] = None, top_k: int = 3, threshold: float = 0.15) -> List[Dict[str, Any]]:
        """
        Semantic cosine/term-frequency retrieval with keyword weighting.
        Returns top matching verified articles with confidence scores.
        """
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        query_counts = Counter(query_tokens)
        results = []

        for article in self.articles:
            if category and article.category.lower() != category.lower():
                continue

            # Combine article title (x3), keywords (x4), and content (x1)
            doc_tokens = (
                self._tokenize(article.title) * 3 +
                [k.lower() for k in article.keywords] * 4 +
                self._tokenize(article.content)
            )
            doc_counts = Counter(doc_tokens)

            # Cosine similarity calculation
            dot_product = sum(query_counts[t] * doc_counts[t] for t in query_counts if t in doc_counts)
            query_norm = math.sqrt(sum(v ** 2 for v in query_counts.values()))
            doc_norm = math.sqrt(sum(v ** 2 for v in doc_counts.values()))

            if query_norm == 0 or doc_norm == 0:
                score = 0.0
            else:
                score = dot_product / (query_norm * doc_norm)

            # Boost if exact keyword is present
            for kw in article.keywords:
                if kw.lower() in query.lower():
                    score = min(1.0, score + 0.15)

            if score >= threshold:
                results.append({
                    "article": article,
                    "relevance_score": round(score, 3),
                    "matched_keywords": [k for k in article.keywords if k.lower() in query.lower()]
                })

        # Sort by relevance score descending
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]

    def get_article_by_id(self, article_id: str) -> Optional[KBArticle]:
        for a in self.articles:
            if a.id.upper() == article_id.upper():
                return a
        return None

    def list_all_categories(self) -> List[str]:
        return sorted(list(set(a.category for a in self.articles)))

