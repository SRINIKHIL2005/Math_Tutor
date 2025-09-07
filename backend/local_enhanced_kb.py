"""
🧠 Local Enhanced Knowledge Base
Fast local search through 7500+ math problems without requiring MongoDB
"""

import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class LocalEnhancedKnowledgeBase:
    """Local knowledge base with fast search capabilities"""
    
    def __init__(self):
        self.problems = []
        self.topic_index = {}
        self.keyword_index = {}
        self.load_all_datasets()
        self.build_search_indexes()
    
    def load_all_datasets(self):
        """Load all available math datasets"""
        data_root = "f:/Internships/Maths_Pofessor/Real_Math_tutor/data"
        
        dataset_files = [
            "converted_datasets/external_datasets_combined.json",
            "converted_datasets/gsm8k_converted.json", 
            "enhanced_math_dataset.json",
            "sample_math_qa.json"
        ]
        
        total_loaded = 0
        
        for dataset_file in dataset_files:
            file_path = os.path.join(data_root, dataset_file)
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    if isinstance(data, list):
                        # Normalize each problem
                        for problem in data:
                            normalized = self.normalize_problem(problem)
                            if normalized['question'] and normalized['solution']:
                                self.problems.append(normalized)
                                total_loaded += 1
                        
                        logger.info(f"✅ Loaded {len(data)} problems from {dataset_file}")
                        
                except Exception as e:
                    logger.error(f"❌ Failed to load {dataset_file}: {e}")
            else:
                logger.warning(f"⚠️ File not found: {file_path}")
        
        logger.info(f"📚 Total problems in local KB: {total_loaded}")
    
    def normalize_problem(self, problem):
        """Normalize problem format"""
        return {
            "id": problem.get("id", f"prob_{hash(str(problem))}")[:50],
            "question": str(problem.get("question", problem.get("problem", ""))),
            "solution": str(problem.get("solution", problem.get("explanation", problem.get("answer", "")))),
            "answer": str(problem.get("answer", problem.get("final_answer", ""))),
            "topic": problem.get("topic", problem.get("subject", "General Math")),
            "difficulty": problem.get("difficulty", "medium"),
            "source": problem.get("source", "Dataset")
        }
    
    def build_search_indexes(self):
        """Build search indexes for fast retrieval"""
        logger.info("🔍 Building search indexes...")
        
        for i, problem in enumerate(self.problems):
            # Topic index
            topic = problem['topic'].lower()
            if topic not in self.topic_index:
                self.topic_index[topic] = []
            self.topic_index[topic].append(i)
            
            # Keyword index
            text = f"{problem['question']} {problem['solution']}".lower()
            words = re.findall(r'\b\w+\b', text)
            
            for word in set(words):
                if len(word) > 2:  # Skip very short words
                    if word not in self.keyword_index:
                        self.keyword_index[word] = []
                    self.keyword_index[word].append(i)
        
        logger.info(f"✅ Built indexes: {len(self.topic_index)} topics, {len(self.keyword_index)} keywords")
    
    def search_similar(self, query: str, threshold: float = 0.6, max_results: int = 5) -> List[Dict]:
        """Search for similar problems using keyword matching and scoring"""
        if not self.problems:
            return []
        
        query_lower = query.lower()
        query_words = set(re.findall(r'\b\w+\b', query_lower))
        
        # Score each problem
        problem_scores = []
        
        for i, problem in enumerate(self.problems):
            score = self.calculate_similarity_score(query_words, problem, query_lower)
            
            if score >= threshold:
                problem_scores.append({
                    **problem,
                    'similarity': score,
                    'index': i
                })
        
        # Sort by similarity score (highest first)
        problem_scores.sort(key=lambda x: x['similarity'], reverse=True)
        
        return problem_scores[:max_results]
    
    def calculate_similarity_score(self, query_words: set, problem: Dict, query_lower: str) -> float:
        """Calculate similarity score between query and problem"""
        score = 0.0
        
        # Text content matching
        problem_text = f"{problem['question']} {problem['solution']}".lower()
        problem_words = set(re.findall(r'\b\w+\b', problem_text))
        
        # Keyword overlap score
        common_words = query_words.intersection(problem_words)
        if query_words:
            keyword_score = len(common_words) / len(query_words)
            score += keyword_score * 0.6
        
        # Math-specific term boosting
        math_terms = {
            'derivative': 0.3, 'integral': 0.3, 'limit': 0.3, 'solve': 0.2, 
            'find': 0.1, 'calculate': 0.1, 'equation': 0.2, 'factor': 0.2,
            'simplify': 0.2, 'expand': 0.2, 'graph': 0.2, 'domain': 0.2,
            'range': 0.2, 'function': 0.2, 'polynomial': 0.2, 'quadratic': 0.2,
            'linear': 0.2, 'exponential': 0.2, 'logarithm': 0.2, 'trig': 0.2,
            'sine': 0.2, 'cosine': 0.2, 'tangent': 0.2, 'matrix': 0.2,
            'vector': 0.2, 'probability': 0.2, 'statistics': 0.2, 'mean': 0.2,
            'median': 0.2, 'variance': 0.2, 'standard': 0.2, 'deviation': 0.2
        }
        
        for term, boost in math_terms.items():
            if term in query_lower and term in problem_text:
                score += boost
        
        # Exact phrase matching
        if len(query_lower) > 10:
            for phrase_len in range(3, min(8, len(query_words))):
                query_phrases = self.extract_phrases(query_lower, phrase_len)
                for phrase in query_phrases:
                    if phrase in problem_text:
                        score += 0.3
        
        # Topic relevance
        if problem['topic'].lower() in query_lower:
            score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def extract_phrases(self, text: str, length: int) -> List[str]:
        """Extract phrases of given length from text"""
        words = text.split()
        phrases = []
        for i in range(len(words) - length + 1):
            phrase = ' '.join(words[i:i + length])
            phrases.append(phrase)
        return phrases
    
    def search_by_topic(self, topic: str) -> List[Dict]:
        """Search problems by topic"""
        topic_lower = topic.lower()
        results = []
        
        if topic_lower in self.topic_index:
            indices = self.topic_index[topic_lower]
            for idx in indices[:10]:  # Limit results
                results.append({
                    **self.problems[idx],
                    'similarity': 1.0
                })
        
        return results
    
    def get_random_problems(self, count: int = 5) -> List[Dict]:
        """Get random problems for examples"""
        import random
        if len(self.problems) < count:
            return self.problems
        
        random_indices = random.sample(range(len(self.problems)), count)
        return [self.problems[i] for i in random_indices]
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        topics = {}
        sources = {}
        
        for problem in self.problems:
            topic = problem['topic']
            source = problem['source']
            
            topics[topic] = topics.get(topic, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_problems': len(self.problems),
            'topics': len(topics),
            'sources': len(sources),
            'top_topics': sorted(topics.items(), key=lambda x: x[1], reverse=True)[:10],
            'top_sources': sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]
        }

# Global instance
enhanced_kb = None

def get_enhanced_kb():
    """Get or create the enhanced knowledge base instance"""
    global enhanced_kb
    if enhanced_kb is None:
        enhanced_kb = LocalEnhancedKnowledgeBase()
    return enhanced_kb

if __name__ == "__main__":
    # Test the knowledge base
    kb = LocalEnhancedKnowledgeBase()
    
    print("📊 Knowledge Base Statistics:")
    stats = kb.get_stats()
    print(f"Total problems: {stats['total_problems']}")
    print(f"Topics: {stats['topics']}")
    print(f"Sources: {stats['sources']}")
    
    # Test search
    test_query = "Find the derivative of x^3 + 2x^2"
    results = kb.search_similar(test_query)
    
    print(f"\n🔍 Search results for: '{test_query}'")
    for i, result in enumerate(results[:3]):
        print(f"{i+1}. Similarity: {result['similarity']:.3f}")
        print(f"   Question: {result['question'][:100]}...")
        print(f"   Topic: {result['topic']}")
        print()
