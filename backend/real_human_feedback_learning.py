"""
REAL HUMAN FEEDBACK LEARNING SYSTEM
=================================
Implementing genuine human-in-the-loop learning
Using feedback to improve system performance over time
Based on RLHF (Reinforcement Learning from Human Feedback) principles
"""

import sqlite3
import json
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path
import asyncio
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FeedbackEntry:
    """Structure for feedback entries"""
    question_id: str
    question_text: str
    answer_text: str
    rating: int  # 1-5 scale
    feedback_text: Optional[str]
    timestamp: datetime
    session_id: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class LearningMetrics:
    """Learning system performance metrics"""
    avg_rating: float
    total_feedback: int
    improvement_trend: float
    confidence_accuracy: float
    last_updated: datetime

class FeedbackDatabase:
    """Database manager for feedback storage"""
    
    def __init__(self, db_path: str = "feedback_learning.db"):
        """Initialize feedback database"""
        self.db_path = db_path
        self.setup_database()
        logger.info(f"📊 Feedback database initialized: {db_path}")
    
    def setup_database(self):
        """Create database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    answer_text TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    feedback_text TEXT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    user_id TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS learning_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS question_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_pattern TEXT NOT NULL,
                    avg_rating REAL NOT NULL,
                    total_responses INTEGER NOT NULL,
                    last_updated TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    def store_feedback(self, feedback: FeedbackEntry):
        """Store feedback in database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO feedback 
                (question_id, question_text, answer_text, rating, feedback_text, timestamp, session_id, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                feedback.question_id,
                feedback.question_text,
                feedback.answer_text,
                feedback.rating,
                feedback.feedback_text,
                feedback.timestamp.isoformat(),
                feedback.session_id,
                feedback.user_id
            ))
            conn.commit()
    
    def get_feedback_by_pattern(self, pattern: str, limit: int = 100) -> List[FeedbackEntry]:
        """Get feedback entries matching a pattern"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT question_id, question_text, answer_text, rating, feedback_text, timestamp, session_id, user_id
                FROM feedback 
                WHERE question_text LIKE ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (f"%{pattern}%", limit))
            
            return [
                FeedbackEntry(
                    question_id=row[0],
                    question_text=row[1],
                    answer_text=row[2],
                    rating=row[3],
                    feedback_text=row[4],
                    timestamp=datetime.fromisoformat(row[5]),
                    session_id=row[6],
                    user_id=row[7]
                )
                for row in cursor.fetchall()
            ]
    
    def get_recent_metrics(self, days: int = 7) -> Dict[str, float]:
        """Get recent performance metrics"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT AVG(rating), COUNT(*), MIN(rating), MAX(rating)
                FROM feedback 
                WHERE timestamp > ?
            """, (cutoff_date,))
            
            result = cursor.fetchone()
            if result and result[0] is not None:
                return {
                    "avg_rating": float(result[0]),
                    "total_feedback": int(result[1]),
                    "min_rating": float(result[2]),
                    "max_rating": float(result[3])
                }
            
            return {"avg_rating": 0.0, "total_feedback": 0, "min_rating": 0.0, "max_rating": 0.0}

class PatternLearningSystem:
    """System to learn from question patterns and feedback"""
    
    def __init__(self, db: FeedbackDatabase):
        """Initialize pattern learning system"""
        self.db = db
        self.pattern_cache = {}
        self.update_cache()
        logger.info("🧠 Pattern learning system initialized")
    
    def update_cache(self):
        """Update pattern cache with latest data"""
        try:
            patterns = self._extract_question_patterns()
            self.pattern_cache = patterns
            logger.info(f"Updated pattern cache with {len(patterns)} patterns")
        except Exception as e:
            logger.error(f"Failed to update pattern cache: {e}")
    
    def _extract_question_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Extract patterns from questions and their ratings"""
        patterns = defaultdict(lambda: {"ratings": [], "questions": [], "avg_rating": 0.0})
        
        # Get all feedback from last 30 days
        recent_feedback = self._get_recent_feedback(30)
        
        for feedback in recent_feedback:
            # Extract key mathematical terms
            key_terms = self._extract_key_terms(feedback.question_text)
            
            for term in key_terms:
                patterns[term]["ratings"].append(feedback.rating)
                patterns[term]["questions"].append(feedback.question_text)
        
        # Calculate averages
        for pattern, data in patterns.items():
            if data["ratings"]:
                data["avg_rating"] = np.mean(data["ratings"])
                data["total_count"] = len(data["ratings"])
        
        return dict(patterns)
    
    def _get_recent_feedback(self, days: int) -> List[FeedbackEntry]:
        """Get feedback from recent days"""
        with sqlite3.connect(self.db.db_path) as conn:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            cursor = conn.execute("""
                SELECT question_id, question_text, answer_text, rating, feedback_text, timestamp, session_id, user_id
                FROM feedback 
                WHERE timestamp > ?
                ORDER BY timestamp DESC
            """, (cutoff_date,))
            
            return [
                FeedbackEntry(
                    question_id=row[0],
                    question_text=row[1],
                    answer_text=row[2],
                    rating=row[3],
                    feedback_text=row[4],
                    timestamp=datetime.fromisoformat(row[5]),
                    session_id=row[6],
                    user_id=row[7]
                )
                for row in cursor.fetchall()
            ]
    
    def _extract_key_terms(self, question: str) -> List[str]:
        """Extract key mathematical terms from question"""
        math_terms = [
            'algebra', 'calculus', 'geometry', 'trigonometry', 'statistics',
            'derivative', 'integral', 'equation', 'function', 'matrix',
            'probability', 'limit', 'theorem', 'proof', 'solve',
            'calculate', 'find', 'determine', 'evaluate', 'simplify',
            'linear', 'quadratic', 'polynomial', 'exponential', 'logarithm'
        ]
        
        question_lower = question.lower()
        found_terms = []
        
        for term in math_terms:
            if term in question_lower:
                found_terms.append(term)
        
        # Add question length category
        if len(question) < 50:
            found_terms.append("short_question")
        elif len(question) > 150:
            found_terms.append("long_question")
        else:
            found_terms.append("medium_question")
        
        return found_terms if found_terms else ["general_math"]
    
    def predict_difficulty(self, question: str) -> Dict[str, Any]:
        """Predict question difficulty based on learned patterns"""
        key_terms = self._extract_key_terms(question)
        
        # Get average ratings for terms (higher rating = easier question)
        term_scores = []
        for term in key_terms:
            if term in self.pattern_cache:
                # Invert rating (5-rating) so higher score = harder
                difficulty_score = 5 - self.pattern_cache[term]["avg_rating"]
                term_scores.append(difficulty_score)
        
        if term_scores:
            avg_difficulty = np.mean(term_scores)
            confidence = min(len(term_scores) / len(key_terms), 1.0)
            
            # Convert to difficulty level
            if avg_difficulty < 1.5:
                level = "easy"
            elif avg_difficulty < 3.0:
                level = "medium"
            else:
                level = "hard"
            
            return {
                "predicted_level": level,
                "difficulty_score": avg_difficulty,
                "confidence": confidence,
                "matching_terms": key_terms
            }
        
        return {
            "predicted_level": "medium",
            "difficulty_score": 2.5,
            "confidence": 0.1,
            "matching_terms": []
        }
    
    def get_improvement_suggestions(self, question: str, rating: int) -> List[str]:
        """Get suggestions for improvement based on low ratings"""
        if rating >= 4:
            return ["Great job! The answer was well received."]
        
        key_terms = self._extract_key_terms(question)
        suggestions = []
        
        # Check for problematic patterns
        for term in key_terms:
            if term in self.pattern_cache:
                pattern_rating = self.pattern_cache[term]["avg_rating"]
                if pattern_rating < 3.0:
                    suggestions.append(
                        f"Questions involving '{term}' tend to get lower ratings. "
                        f"Consider providing more detailed explanations for {term} problems."
                    )
        
        # General improvement suggestions based on rating
        if rating <= 2:
            suggestions.extend([
                "Consider breaking down the solution into more detailed steps",
                "Add more context and explanation for each step",
                "Include verification or checking steps",
                "Provide alternative solution methods if applicable"
            ])
        elif rating == 3:
            suggestions.extend([
                "The answer is adequate but could be improved",
                "Consider adding more examples or analogies",
                "Explain the reasoning behind each step more clearly"
            ])
        
        return suggestions if suggestions else ["Continue providing clear, step-by-step solutions"]

class AdaptiveLearningSystem:
    """Main system that adapts based on human feedback"""
    
    def __init__(self, db_path: str = "adaptive_learning.db"):
        """Initialize adaptive learning system"""
        self.db = FeedbackDatabase(db_path)
        self.pattern_system = PatternLearningSystem(self.db)
        self.confidence_calibrator = ConfidenceCalibrator(self.db)
        logger.info("🎯 Adaptive Learning System initialized")
    
    async def process_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process new feedback and update learning systems"""
        try:
            # Create feedback entry
            feedback = FeedbackEntry(
                question_id=feedback_data["question_id"],
                question_text=feedback_data["question_text"],
                answer_text=feedback_data["answer_text"],
                rating=feedback_data["rating"],
                feedback_text=feedback_data.get("feedback_text"),
                timestamp=datetime.now(),
                session_id=feedback_data.get("session_id"),
                user_id=feedback_data.get("user_id")
            )
            
            # Store feedback
            self.db.store_feedback(feedback)
            
            # Update pattern learning
            self.pattern_system.update_cache()
            
            # Update confidence calibration
            await self.confidence_calibrator.update_calibration()
            
            # Get improvement suggestions
            suggestions = self.pattern_system.get_improvement_suggestions(
                feedback.question_text, feedback.rating
            )
            
            logger.info(f"Processed feedback for question {feedback.question_id} (rating: {feedback.rating})")
            
            return {
                "status": "success",
                "feedback_processed": True,
                "suggestions": suggestions,
                "pattern_updated": True,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_question_guidance(self, question: str) -> Dict[str, Any]:
        """Get guidance for answering a question based on learned patterns"""
        try:
            # Predict difficulty
            difficulty_prediction = self.pattern_system.predict_difficulty(question)
            
            # Get confidence calibration
            confidence_guidance = await self.confidence_calibrator.get_confidence_guidance(question)
            
            # Get recent performance metrics
            recent_metrics = self.db.get_recent_metrics(7)
            
            return {
                "difficulty_prediction": difficulty_prediction,
                "confidence_guidance": confidence_guidance,
                "recent_performance": recent_metrics,
                "recommendations": self._generate_recommendations(difficulty_prediction, recent_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting question guidance: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, difficulty: Dict, metrics: Dict) -> List[str]:
        """Generate recommendations based on difficulty and performance"""
        recommendations = []
        
        # Difficulty-based recommendations
        if difficulty["predicted_level"] == "hard":
            recommendations.append("This appears to be a challenging question. Provide extra detail in explanations.")
        elif difficulty["predicted_level"] == "easy":
            recommendations.append("This seems like a straightforward question. Keep explanations clear but concise.")
        
        # Performance-based recommendations
        if metrics["avg_rating"] < 3.0:
            recommendations.append("Recent ratings are below average. Focus on clearer explanations and more steps.")
        elif metrics["avg_rating"] > 4.0:
            recommendations.append("Recent performance is excellent. Continue with current approach.")
        
        # Confidence-based recommendations
        if difficulty["confidence"] < 0.3:
            recommendations.append("Limited data for this question type. Be extra careful and detailed.")
        
        return recommendations
    
    def get_learning_dashboard(self) -> Dict[str, Any]:
        """Get dashboard data for learning system performance"""
        try:
            recent_metrics = self.db.get_recent_metrics(30)
            
            # Get top performing patterns
            top_patterns = sorted(
                [(k, v) for k, v in self.pattern_system.pattern_cache.items() 
                 if v.get("total_count", 0) > 5],
                key=lambda x: x[1]["avg_rating"],
                reverse=True
            )[:10]
            
            # Get improvement areas
            improvement_patterns = sorted(
                [(k, v) for k, v in self.pattern_system.pattern_cache.items() 
                 if v.get("total_count", 0) > 3],
                key=lambda x: x[1]["avg_rating"]
            )[:5]
            
            return {
                "overall_metrics": recent_metrics,
                "top_performing_patterns": [
                    {"pattern": p[0], "avg_rating": p[1]["avg_rating"], "count": p[1]["total_count"]}
                    for p in top_patterns
                ],
                "areas_for_improvement": [
                    {"pattern": p[0], "avg_rating": p[1]["avg_rating"], "count": p[1]["total_count"]}
                    for p in improvement_patterns
                ],
                "total_patterns_learned": len(self.pattern_system.pattern_cache),
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating dashboard: {e}")
            return {"error": str(e)}

class ConfidenceCalibrator:
    """System to calibrate confidence scores based on feedback"""
    
    def __init__(self, db: FeedbackDatabase):
        """Initialize confidence calibrator"""
        self.db = db
        self.calibration_data = {}
        logger.info("📊 Confidence calibrator initialized")
    
    async def update_calibration(self):
        """Update confidence calibration based on feedback"""
        try:
            # Get feedback with confidence scores (if available)
            # This would require storing predicted confidence with each answer
            # For now, we'll create a simple calibration based on rating patterns
            
            recent_feedback = self._get_calibration_data()
            self.calibration_data = self._calculate_calibration(recent_feedback)
            
            logger.info("Updated confidence calibration")
            
        except Exception as e:
            logger.error(f"Calibration update error: {e}")
    
    def _get_calibration_data(self) -> List[Tuple[float, int]]:
        """Get data for confidence calibration (predicted_confidence, actual_rating)"""
        # This is a simplified version - in a real system, you'd store
        # predicted confidence with each answer and compare to actual ratings
        
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.execute("""
                SELECT rating, COUNT(*) 
                FROM feedback 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY rating
            """)
            
            calibration_data = []
            for rating, count in cursor.fetchall():
                # Simulate confidence based on rating distribution
                simulated_confidence = (rating - 1) / 4.0  # Convert 1-5 to 0-1
                calibration_data.extend([(simulated_confidence, rating)] * count)
            
            return calibration_data
    
    def _calculate_calibration(self, data: List[Tuple[float, int]]) -> Dict[str, float]:
        """Calculate calibration metrics"""
        if not data:
            return {"calibration_error": 0.0, "confidence_accuracy": 0.0}
        
        # Calculate simple calibration metrics
        total_error = 0.0
        for conf, rating in data:
            # Expected rating based on confidence
            expected_rating = (conf * 4) + 1  # Convert 0-1 to 1-5
            total_error += abs(expected_rating - rating)
        
        avg_error = total_error / len(data)
        accuracy = max(0.0, 1.0 - (avg_error / 4.0))  # Normalize to 0-1
        
        return {
            "calibration_error": avg_error,
            "confidence_accuracy": accuracy,
            "sample_size": len(data)
        }
    
    async def get_confidence_guidance(self, question: str) -> Dict[str, Any]:
        """Get guidance for setting confidence scores"""
        return {
            "calibration_metrics": self.calibration_data,
            "recommendation": "Base confidence on pattern match strength and historical performance",
            "current_accuracy": self.calibration_data.get("confidence_accuracy", 0.5)
        }

def get_learning_system(db_path: str = "adaptive_learning.db") -> AdaptiveLearningSystem:
    """Factory function to get learning system instance"""
    return AdaptiveLearningSystem(db_path)

async def test_learning_system():
    """Test the learning system"""
    logger.info("🧪 Testing Human Feedback Learning System")
    
    system = get_learning_system("test_learning.db")
    
    # Test feedback processing
    test_feedback = {
        "question_id": "test_001",
        "question_text": "Solve the quadratic equation x^2 + 5x + 6 = 0",
        "answer_text": "The solutions are x = -2 and x = -3",
        "rating": 4,
        "feedback_text": "Good explanation, could use more steps"
    }
    
    result = await system.process_feedback(test_feedback)
    logger.info(f"Feedback processing result: {result['status']}")
    
    # Test question guidance
    guidance = await system.get_question_guidance("Find the derivative of x^2 + 3x + 1")
    logger.info(f"Question guidance: {guidance}")
    
    # Test dashboard
    dashboard = system.get_learning_dashboard()
    logger.info(f"Dashboard generated with {len(dashboard.get('top_performing_patterns', []))} patterns")
    
    logger.info("✅ Learning system test completed")

# Alias for API compatibility
class HumanFeedbackLearning(AdaptiveLearningSystem):
    """Alias for API compatibility"""
    pass

if __name__ == "__main__":
    asyncio.run(test_learning_system())
