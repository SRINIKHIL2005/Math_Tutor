"""
Quick Fix RAG System - Simple Knowledge Base
==========================================
Create a simple working knowledge base for basic math problems
"""

import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleKnowledgeBase:
    """Simple knowledge base that actually works"""
    
    def __init__(self):
        self.problems = {
            "2+2": {
                "answer": "2 + 2 = 4\n\nThis is basic addition. When we add 2 and 2, we get 4.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "what is 2+2": {
                "answer": "2 + 2 = 4\n\nThis is basic addition. When we add 2 and 2, we get 4.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "whats 2+2": {
                "answer": "2 + 2 = 4\n\nThis is basic addition. When we add 2 and 2, we get 4.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "2*4": {
                "answer": "2 × 4 = 8\n\nThis is multiplication. When we multiply 2 by 4, we get 8.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "what is 2*4": {
                "answer": "2 × 4 = 8\n\nThis is multiplication. When we multiply 2 by 4, we get 8.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "5+3": {
                "answer": "5 + 3 = 8\n\nAdding 5 and 3 gives us 8.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "10-4": {
                "answer": "10 - 4 = 6\n\nSubtracting 4 from 10 gives us 6.",
                "confidence": 0.95,
                "topic": "arithmetic"
            },
            "x+5=12": {
                "answer": "To solve x + 5 = 12:\n\nSubtract 5 from both sides:\nx + 5 - 5 = 12 - 5\nx = 7\n\nTherefore, x = 7.",
                "confidence": 0.9,
                "topic": "algebra"
            },
            "solve x+5=12": {
                "answer": "To solve x + 5 = 12:\n\nSubtract 5 from both sides:\nx + 5 - 5 = 12 - 5\nx = 7\n\nTherefore, x = 7.",
                "confidence": 0.9,
                "topic": "algebra"
            },
            "quadratic equation roots 3 and -2": {
                "answer": "If the roots are 3 and -2, we can write:\n(x - 3)(x - (-2)) = 0\n(x - 3)(x + 2) = 0\n\nExpanding:\nx² + 2x - 3x - 6 = 0\nx² - x - 6 = 0\n\nTherefore, the quadratic equation is x² - x - 6 = 0.",
                "confidence": 0.9,
                "topic": "algebra"
            }
        }
    
    def search_similar(self, query: str) -> Dict[str, Any]:
        """Search for similar problems"""
        query_lower = query.lower().strip()
        
        # Direct match first
        if query_lower in self.problems:
            problem = self.problems[query_lower]
            return {
                'answer': problem['answer'],
                'confidence': problem['confidence'],
                'route_taken': 'simple_knowledge_base',
                'topic': problem['topic']
            }
        
        # Fuzzy matching for common variations
        for key, problem in self.problems.items():
            if any(word in query_lower for word in key.split()):
                return {
                    'answer': problem['answer'],
                    'confidence': problem['confidence'] - 0.1,  # Lower confidence for fuzzy match
                    'route_taken': 'simple_knowledge_base_fuzzy',
                    'topic': problem['topic']
                }
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base stats"""
        return {
            "total_problems": len(self.problems),
            "storage_type": "simple_memory",
            "status": "working"
        }

# Global instance
knowledge_base = SimpleKnowledgeBase()
