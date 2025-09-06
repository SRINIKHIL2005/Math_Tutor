
import json
import logging
import asyncio
import sqlite3
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
import re
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JEEQuestion:
    """Structure for JEE questions"""
    question_id: str
    question_text: str
    correct_answer: str
    options: List[str]
    topic: str
    difficulty: str
    year: Optional[int] = None
    exam_type: str = "JEE_MAIN"  # JEE_MAIN or JEE_ADVANCED

@dataclass
class JEEBenchmarkResult:
    """Result structure for JEE benchmark tests"""
    question_id: str
    question_text: str
    predicted_answer: str
    correct_answer: str
    is_correct: bool
    confidence_score: float
    response_time: float
    error_analysis: str
    topic: str
    difficulty: str

@dataclass
class JEEBenchmarkSummary:
    """Summary of JEE benchmark performance"""
    total_questions: int
    correct_answers: int
    accuracy: float
    avg_confidence: float
    avg_response_time: float
    topic_performance: Dict[str, float]
    difficulty_performance: Dict[str, float]
    timestamp: datetime

class JEEQuestionDatabase:
    """Database for JEE questions and benchmarking results"""
    
    def __init__(self, db_path: str = "jee_benchmark.db"):
        """Initialize JEE question database"""
        self.db_path = db_path
        self.setup_database()
        self._populate_sample_questions()
        logger.info(f"📚 JEE Question database initialized: {db_path}")
    
    def setup_database(self):
        """Create database tables"""
        with sqlite3.connect(self.db_path) as conn:
            # Questions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS jee_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT UNIQUE NOT NULL,
                    question_text TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    options TEXT NOT NULL,  -- JSON string
                    topic TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    year INTEGER,
                    exam_type TEXT NOT NULL
                )
            """)
            
            # Benchmark results table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS benchmark_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id TEXT NOT NULL,
                    predicted_answer TEXT NOT NULL,
                    is_correct INTEGER NOT NULL,
                    confidence_score REAL NOT NULL,
                    response_time REAL NOT NULL,
                    error_analysis TEXT,
                    timestamp TEXT NOT NULL,
                    system_version TEXT
                )
            """)
            
            # Benchmark summaries table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS benchmark_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_questions INTEGER NOT NULL,
                    correct_answers INTEGER NOT NULL,
                    accuracy REAL NOT NULL,
                    avg_confidence REAL NOT NULL,
                    avg_response_time REAL NOT NULL,
                    topic_performance TEXT NOT NULL,  -- JSON string
                    difficulty_performance TEXT NOT NULL,  -- JSON string
                    timestamp TEXT NOT NULL,
                    system_version TEXT
                )
            """)
            
            conn.commit()
    
    def _populate_sample_questions(self):
        """Populate database with sample JEE questions"""
        sample_questions = [
            JEEQuestion(
                question_id="jee_001",
                question_text="If the roots of the equation x² - 2ax + a² - 1 = 0 are real, then find the range of values of 'a'.",
                correct_answer="a ∈ R (all real numbers)",
                options=["a ∈ R", "a > 1", "a < -1", "a ∈ [-1, 1]"],
                topic="Algebra",
                difficulty="Medium",
                year=2023,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_002",
                question_text="Find the derivative of f(x) = (sin x)/(1 + cos x)",
                correct_answer="f'(x) = 1/(1 + cos x)",
                options=["1/(1 + cos x)", "-1/(1 + cos x)", "cos x/(1 + cos x)", "sin x/(1 + cos x)²"],
                topic="Calculus",
                difficulty="Medium",
                year=2023,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_003",
                question_text="In a triangle ABC, if a = 7, b = 8, and c = 9, find the area of the triangle.",
                correct_answer="12√5",
                options=["12√5", "24√5", "6√5", "18√5"],
                topic="Geometry",
                difficulty="Easy",
                year=2022,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_004",
                question_text="Find the limit: lim(x→0) (sin 3x)/(sin 5x)",
                correct_answer="3/5",
                options=["3/5", "5/3", "1", "0"],
                topic="Calculus",
                difficulty="Easy",
                year=2022,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_005",
                question_text="If the coefficient of x³ in the expansion of (1 + 2x)^n is 160, find the value of n.",
                correct_answer="n = 6",
                options=["n = 6", "n = 8", "n = 5", "n = 7"],
                topic="Algebra",
                difficulty="Hard",
                year=2023,
                exam_type="JEE_ADVANCED"
            ),
            JEEQuestion(
                question_id="jee_006",
                question_text="Find the equation of the circle passing through points (0,0), (1,0), and (0,1).",
                correct_answer="x² + y² - x - y = 0",
                options=["x² + y² - x - y = 0", "x² + y² + x + y = 0", "x² + y² - 2x - 2y = 0", "x² + y² = 1"],
                topic="Geometry",
                difficulty="Medium",
                year=2022,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_007",
                question_text="If matrices A and B are such that AB = BA = I, where I is the identity matrix, then B is called the _____ of A.",
                correct_answer="inverse",
                options=["inverse", "transpose", "adjoint", "determinant"],
                topic="Linear Algebra",
                difficulty="Easy",
                year=2023,
                exam_type="JEE_MAIN"
            ),
            JEEQuestion(
                question_id="jee_008",
                question_text="Find the value of ∫₀^π sin²x dx",
                correct_answer="π/2",
                options=["π/2", "π", "π/4", "2π"],
                topic="Calculus",
                difficulty="Medium",
                year=2022,
                exam_type="JEE_MAIN"
            )
        ]
        
        with sqlite3.connect(self.db_path) as conn:
            for question in sample_questions:
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO jee_questions 
                        (question_id, question_text, correct_answer, options, topic, difficulty, year, exam_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        question.question_id,
                        question.question_text,
                        question.correct_answer,
                        json.dumps(question.options),
                        question.topic,
                        question.difficulty,
                        question.year,
                        question.exam_type
                    ))
                except sqlite3.IntegrityError:
                    pass  # Question already exists
            
            conn.commit()
    
    def get_questions_by_criteria(self, topic: Optional[str] = None, 
                                 difficulty: Optional[str] = None,
                                 exam_type: Optional[str] = None,
                                 limit: int = 50) -> List[JEEQuestion]:
        """Get questions based on criteria"""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM jee_questions WHERE 1=1"
            params = []
            
            if topic:
                query += " AND topic = ?"
                params.append(topic)
            
            if difficulty:
                query += " AND difficulty = ?"
                params.append(difficulty)
            
            if exam_type:
                query += " AND exam_type = ?"
                params.append(exam_type)
            
            query += " ORDER BY RANDOM() LIMIT ?"
            params.append(limit)
            
            cursor = conn.execute(query, params)
            
            questions = []
            for row in cursor.fetchall():
                questions.append(JEEQuestion(
                    question_id=row[1],
                    question_text=row[2],
                    correct_answer=row[3],
                    options=json.loads(row[4]),
                    topic=row[5],
                    difficulty=row[6],
                    year=row[7],
                    exam_type=row[8]
                ))
            
            return questions
    
    def save_benchmark_result(self, result: JEEBenchmarkResult, system_version: str = "1.0"):
        """Save benchmark result to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO benchmark_results 
                (question_id, predicted_answer, is_correct, confidence_score, 
                 response_time, error_analysis, timestamp, system_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.question_id,
                result.predicted_answer,
                1 if result.is_correct else 0,
                result.confidence_score,
                result.response_time,
                result.error_analysis,
                datetime.now().isoformat(),
                system_version
            ))
            conn.commit()
    
    def save_benchmark_summary(self, summary: JEEBenchmarkSummary, system_version: str = "1.0"):
        """Save benchmark summary to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO benchmark_summaries 
                (total_questions, correct_answers, accuracy, avg_confidence, avg_response_time,
                 topic_performance, difficulty_performance, timestamp, system_version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.total_questions,
                summary.correct_answers,
                summary.accuracy,
                summary.avg_confidence,
                summary.avg_response_time,
                json.dumps(summary.topic_performance),
                json.dumps(summary.difficulty_performance),
                summary.timestamp.isoformat(),
                system_version
            ))
            conn.commit()

class JEEAnswerEvaluator:
    """Evaluates answers against JEE standards"""
    
    def __init__(self):
        """Initialize JEE answer evaluator"""
        self.math_patterns = self._setup_math_patterns()
        logger.info("🎯 JEE Answer evaluator initialized")
    
    def _setup_math_patterns(self) -> Dict[str, Any]:
        """Setup patterns for mathematical answer evaluation"""
        return {
            'fraction_patterns': [
                r'(\d+)/(\d+)',  # Simple fractions
                r'(\d+)\\?/(\d+)',  # LaTeX fractions
            ],
            'radical_patterns': [
                r'√(\d+)',  # Square roots
                r'sqrt\(([^)]+)\)',  # sqrt() notation
                r'\\sqrt{([^}]+)}',  # LaTeX sqrt
            ],
            'pi_patterns': [
                r'π', r'pi', r'\\pi'
            ],
            'infinity_patterns': [
                r'∞', r'infinity', r'\\infty'
            ]
        }
    
    def evaluate_answer(self, predicted: str, correct: str) -> Tuple[bool, float, str]:
        """
        Evaluate predicted answer against correct answer
        Returns: (is_correct, similarity_score, analysis)
        """
        try:
            # Normalize both answers
            pred_norm = self._normalize_answer(predicted)
            correct_norm = self._normalize_answer(correct)
            
            # Direct match
            if pred_norm == correct_norm:
                return True, 1.0, "Exact match"
            
            # Mathematical equivalence check
            is_equiv, score, analysis = self._check_mathematical_equivalence(
                pred_norm, correct_norm
            )
            
            if is_equiv:
                return True, score, analysis
            
            # Partial match analysis
            similarity = self._calculate_similarity(pred_norm, correct_norm)
            
            if similarity > 0.8:
                return False, similarity, "Very close but not exact"
            elif similarity > 0.6:
                return False, similarity, "Partially correct approach"
            elif similarity > 0.3:
                return False, similarity, "Some correct elements"
            else:
                return False, similarity, "Incorrect answer"
            
        except Exception as e:
            logger.error(f"Error evaluating answer: {e}")
            return False, 0.0, f"Evaluation error: {str(e)}"
    
    def _normalize_answer(self, answer: str) -> str:
        """Normalize mathematical answer for comparison"""
        if not answer:
            return ""
        
        # Convert to lowercase and strip whitespace
        normalized = answer.lower().strip()
        
        # Remove common mathematical formatting
        normalized = normalized.replace(' ', '')
        normalized = normalized.replace('\\', '')
        normalized = normalized.replace('{', '').replace('}', '')
        
        # Standardize common mathematical notation
        replacements = {
            'pi': 'π',
            'infinity': '∞',
            'infty': '∞',
            'sqrt': '√',
            '+-': '±',
            'pm': '±',
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized
    
    def _check_mathematical_equivalence(self, pred: str, correct: str) -> Tuple[bool, float, str]:
        """Check if two mathematical expressions are equivalent"""
        
        # Check fraction equivalence
        if self._check_fraction_equivalence(pred, correct):
            return True, 0.95, "Equivalent fraction"
        
        # Check radical equivalence
        if self._check_radical_equivalence(pred, correct):
            return True, 0.95, "Equivalent radical form"
        
        # Check polynomial equivalence (simplified)
        if self._check_polynomial_equivalence(pred, correct):
            return True, 0.90, "Equivalent polynomial"
        
        return False, 0.0, "Not mathematically equivalent"
    
    def _check_fraction_equivalence(self, pred: str, correct: str) -> bool:
        """Check if two fractions are equivalent"""
        try:
            pred_fractions = re.findall(r'(\d+)/(\d+)', pred)
            correct_fractions = re.findall(r'(\d+)/(\d+)', correct)
            
            if pred_fractions and correct_fractions:
                pred_num, pred_den = map(int, pred_fractions[0])
                correct_num, correct_den = map(int, correct_fractions[0])
                
                # Check if fractions are equivalent
                return pred_num * correct_den == correct_num * pred_den
            
            return False
        except:
            return False
    
    def _check_radical_equivalence(self, pred: str, correct: str) -> bool:
        """Check if two radical expressions are equivalent"""
        try:
            # Simple radical comparison
            pred_radicals = re.findall(r'√(\d+)', pred)
            correct_radicals = re.findall(r'√(\d+)', correct)
            
            if pred_radicals and correct_radicals:
                return pred_radicals[0] == correct_radicals[0]
            
            return False
        except:
            return False
    
    def _check_polynomial_equivalence(self, pred: str, correct: str) -> bool:
        """Simple polynomial equivalence check"""
        # This is a simplified version - real implementation would be more complex
        return False
    
    def _calculate_similarity(self, pred: str, correct: str) -> float:
        """Calculate similarity between two strings"""
        if not pred or not correct:
            return 0.0
        
        # Simple character-based similarity
        common_chars = set(pred) & set(correct)
        total_chars = set(pred) | set(correct)
        
        if not total_chars:
            return 0.0
        
        return len(common_chars) / len(total_chars)

class JEEBenchmarkingSystem:
    """Main JEE benchmarking system"""
    
    def __init__(self, db_path: str = "jee_benchmark.db"):
        """Initialize JEE benchmarking system"""
        self.db = JEEQuestionDatabase(db_path)
        self.evaluator = JEEAnswerEvaluator()
        self.math_system = None  # Will be injected
        logger.info("🏆 JEE Benchmarking System initialized")
    
    def set_math_system(self, math_system):
        """Set the math system to be benchmarked"""
        self.math_system = math_system
        logger.info("Math system registered for benchmarking")
    
    async def run_benchmark(self, criteria: Dict[str, Any] = None) -> JEEBenchmarkSummary:
        """
        Run JEE benchmark test
        
        Args:
            criteria: Dict with 'topic', 'difficulty', 'exam_type', 'limit'
        """
        if not self.math_system:
            raise ValueError("Math system not set. Call set_math_system() first.")
        
        criteria = criteria or {}
        
        logger.info("🎯 Starting JEE Benchmark Test")
        
        # Get questions based on criteria
        questions = self.db.get_questions_by_criteria(
            topic=criteria.get('topic'),
            difficulty=criteria.get('difficulty'),
            exam_type=criteria.get('exam_type'),
            limit=criteria.get('limit', 20)
        )
        
        if not questions:
            raise ValueError("No questions found matching criteria")
        
        logger.info(f"Testing with {len(questions)} questions")
        
        results = []
        total_response_time = 0.0
        total_confidence = 0.0
        
        for i, question in enumerate(questions):
            logger.info(f"Processing question {i+1}/{len(questions)}: {question.question_id}")
            
            # Get answer from math system
            start_time = time.time()
            try:
                response = await self._get_system_answer(question)
                response_time = time.time() - start_time
            except Exception as e:
                logger.error(f"Error getting answer for {question.question_id}: {e}")
                response = {"answer": "Error", "confidence": 0.0}
                response_time = 0.0
            
            # Evaluate answer
            is_correct, similarity, analysis = self.evaluator.evaluate_answer(
                response.get("answer", ""),
                question.correct_answer
            )
            
            # Create result
            result = JEEBenchmarkResult(
                question_id=question.question_id,
                question_text=question.question_text,
                predicted_answer=response.get("answer", ""),
                correct_answer=question.correct_answer,
                is_correct=is_correct,
                confidence_score=response.get("confidence", 0.0),
                response_time=response_time,
                error_analysis=analysis,
                topic=question.topic,
                difficulty=question.difficulty
            )
            
            results.append(result)
            self.db.save_benchmark_result(result)
            
            total_response_time += response_time
            total_confidence += result.confidence_score
        
        # Calculate summary statistics
        correct_count = sum(1 for r in results if r.is_correct)
        accuracy = correct_count / len(results) if results else 0.0
        avg_confidence = total_confidence / len(results) if results else 0.0
        avg_response_time = total_response_time / len(results) if results else 0.0
        
        # Topic performance
        topic_performance = {}
        for topic in set(r.topic for r in results):
            topic_results = [r for r in results if r.topic == topic]
            topic_correct = sum(1 for r in topic_results if r.is_correct)
            topic_performance[topic] = topic_correct / len(topic_results) if topic_results else 0.0
        
        # Difficulty performance
        difficulty_performance = {}
        for difficulty in set(r.difficulty for r in results):
            diff_results = [r for r in results if r.difficulty == difficulty]
            diff_correct = sum(1 for r in diff_results if r.is_correct)
            difficulty_performance[difficulty] = diff_correct / len(diff_results) if diff_results else 0.0
        
        # Create summary
        summary = JEEBenchmarkSummary(
            total_questions=len(results),
            correct_answers=correct_count,
            accuracy=accuracy,
            avg_confidence=avg_confidence,
            avg_response_time=avg_response_time,
            topic_performance=topic_performance,
            difficulty_performance=difficulty_performance,
            timestamp=datetime.now()
        )
        
        # Save summary
        self.db.save_benchmark_summary(summary)
        
        logger.info(f"🎉 Benchmark completed: {accuracy:.2%} accuracy on {len(results)} questions")
        
        return summary
    
    async def _get_system_answer(self, question: JEEQuestion) -> Dict[str, Any]:
        """Get answer from the math system being benchmarked"""
        
        # This is a placeholder - in real implementation, this would call
        # the actual math system (LangGraph agent, etc.)
        
        if hasattr(self.math_system, 'invoke'):
            # LangGraph style
            result = await asyncio.to_thread(
                self.math_system.invoke,
                {"question": question.question_text}
            )
            return {
                "answer": result.get("final_answer", "No answer"),
                "confidence": result.get("confidence", 0.5)
            }
        
        elif hasattr(self.math_system, 'process_question'):
            # Custom system
            result = await self.math_system.process_question(question.question_text)
            return {
                "answer": result.get("answer", "No answer"),
                "confidence": result.get("confidence", 0.5)
            }
        
        else:
            # Fallback - simulate answer
            return {
                "answer": f"Simulated answer for: {question.question_text[:50]}...",
                "confidence": 0.3
            }
    
    def get_benchmark_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get history of benchmark runs"""
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM benchmark_summaries 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    "id": row[0],
                    "total_questions": row[1],
                    "correct_answers": row[2],
                    "accuracy": row[3],
                    "avg_confidence": row[4],
                    "avg_response_time": row[5],
                    "topic_performance": json.loads(row[6]),
                    "difficulty_performance": json.loads(row[7]),
                    "timestamp": row[8],
                    "system_version": row[9]
                })
            
            return history
    
    def get_detailed_analysis(self) -> Dict[str, Any]:
        """Get detailed performance analysis"""
        with sqlite3.connect(self.db.db_path) as conn:
            # Overall statistics
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_attempts,
                    SUM(is_correct) as total_correct,
                    AVG(confidence_score) as avg_confidence,
                    AVG(response_time) as avg_time
                FROM benchmark_results
            """)
            
            overall_stats = cursor.fetchone()
            
            # Performance by topic
            cursor = conn.execute("""
                SELECT 
                    jq.topic,
                    COUNT(*) as attempts,
                    SUM(br.is_correct) as correct,
                    AVG(br.confidence_score) as avg_confidence
                FROM benchmark_results br
                JOIN jee_questions jq ON br.question_id = jq.question_id
                GROUP BY jq.topic
            """)
            
            topic_stats = cursor.fetchall()
            
            # Performance by difficulty
            cursor = conn.execute("""
                SELECT 
                    jq.difficulty,
                    COUNT(*) as attempts,
                    SUM(br.is_correct) as correct,
                    AVG(br.confidence_score) as avg_confidence
                FROM benchmark_results br
                JOIN jee_questions jq ON br.question_id = jq.question_id
                GROUP BY jq.difficulty
            """)
            
            difficulty_stats = cursor.fetchall()
            
            return {
                "overall": {
                    "total_attempts": overall_stats[0],
                    "total_correct": overall_stats[1],
                    "accuracy": overall_stats[1] / overall_stats[0] if overall_stats[0] > 0 else 0,
                    "avg_confidence": overall_stats[2],
                    "avg_response_time": overall_stats[3]
                },
                "by_topic": [
                    {
                        "topic": row[0],
                        "attempts": row[1],
                        "correct": row[2],
                        "accuracy": row[2] / row[1] if row[1] > 0 else 0,
                        "avg_confidence": row[3]
                    }
                    for row in topic_stats
                ],
                "by_difficulty": [
                    {
                        "difficulty": row[0],
                        "attempts": row[1],
                        "correct": row[2],
                        "accuracy": row[2] / row[1] if row[1] > 0 else 0,
                        "avg_confidence": row[3]
                    }
                    for row in difficulty_stats
                ]
            }

def get_jee_benchmark_system(db_path: str = "jee_benchmark.db") -> JEEBenchmarkingSystem:
    """Factory function to get JEE benchmark system"""
    return JEEBenchmarkingSystem(db_path)

async def test_jee_benchmark():
    """Test the JEE benchmarking system"""
    logger.info("🧪 Testing JEE Benchmarking System")
    
    # Create mock math system
    class MockMathSystem:
        async def process_question(self, question: str) -> Dict[str, Any]:
            # Simulate processing
            await asyncio.sleep(0.1)
            return {
                "answer": f"Mock answer for: {question[:30]}...",
                "confidence": 0.7
            }
    
    # Initialize system
    benchmark_system = get_jee_benchmark_system("test_jee_benchmark.db")
    mock_system = MockMathSystem()
    benchmark_system.set_math_system(mock_system)
    
    # Run benchmark
    try:
        summary = await benchmark_system.run_benchmark({
            'topic': 'Algebra',
            'limit': 3
        })
        
        logger.info(f"Benchmark Results:")
        logger.info(f"  Accuracy: {summary.accuracy:.2%}")
        logger.info(f"  Questions: {summary.total_questions}")
        logger.info(f"  Avg Response Time: {summary.avg_response_time:.2f}s")
        logger.info(f"  Topic Performance: {summary.topic_performance}")
        
        # Get detailed analysis
        analysis = benchmark_system.get_detailed_analysis()
        logger.info(f"Overall accuracy: {analysis['overall']['accuracy']:.2%}")
        
    except Exception as e:
        logger.error(f"Benchmark test failed: {e}")
    
    logger.info("✅ JEE benchmark test completed")

if __name__ == "__main__":
    asyncio.run(test_jee_benchmark())
