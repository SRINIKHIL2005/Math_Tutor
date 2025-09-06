
import os
from typing import List, Dict, Any
import logging
from real_mongodb_atlas_fixed import RealMongoDBAtlasFixed
from quick_fix_rag import knowledge_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealMathematicalRAG:
    """
    A RAG system for mathematical problem solving that uses working knowledge base
    """
    
    def __init__(self):
        """Initialize the Mathematical RAG system"""
        try:
            self.knowledge_base = knowledge_base
            self.available = True
            logger.info("✅ Mathematical RAG initialized with Quick Fix Knowledge Base")
        except Exception as e:
            logger.error(f"❌ Failed to initialize RAG: {e}")
            self.knowledge_base = None
            self.available = False
    
    def generate_solution_with_rag(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Generate solution using RAG with knowledge base
        
        Args:
            question: The mathematical question to solve
            top_k: Number of similar problems to retrieve
        
        Returns:
            Dictionary with answer, confidence, and route_taken
        """
        try:
            if not self.available or not self.knowledge_base:
                return {
                    'answer': 'RAG system not available',
                    'confidence': 0.0,
                    'route_taken': 'rag_unavailable'
                }
            
            logger.info(f"🔍 Searching knowledge base for: {question[:100]}...")
            
            # Search the simple knowledge base
            result = self.knowledge_base.search_similar(question)
            
            if result:
                logger.info(f"✅ Found match in knowledge base with confidence: {result['confidence']}")
                return {
                    'answer': result['answer'],
                    'confidence': result['confidence'],
                    'route_taken': result['route_taken'],
                    'topic': result.get('topic', 'unknown')
                }
            
            logger.info("No matches found in knowledge base")
            return {
                'answer': 'No similar problems found in knowledge base',
                'confidence': 0.1,
                'route_taken': 'rag_no_matches'
            }
                
        except Exception as e:
            logger.error(f"❌ RAG search failed: {e}")
            return {
                'answer': f'RAG search failed: {str(e)}',
                'confidence': 0.0,
                'route_taken': 'rag_error'
            }
            similar_problems = self.simple_kb.search_similar_problems(question, limit=top_k)
            
            if not similar_problems and self.mongodb_rag:
                # Fallback to MongoDB Atlas vector search
                try:
                    similar_problems = self.mongodb_rag.search_similar_problems(question, limit=top_k)
                except Exception as e:
                    logger.warning(f"MongoDB search failed: {e}")
                    similar_problems = []
            
            if not similar_problems:
                logger.info("No similar problems found in vector database")
                return {
                    'answer': 'No similar problems found in knowledge base',
                    'confidence': 0.1,
                    'route_taken': 'rag_no_matches'
                }
            
            # Get the best match
            best_match = similar_problems[0]
            similarity_score = best_match.get('similarity', 0.0)
            
            logger.info(f"Best match similarity: {similarity_score}")
            
            # If we have a high-quality match, use it
            if similarity_score > 0.6:  # High similarity threshold
                solution = best_match.get('solution', 'Solution not available')
                
                # Create a comprehensive answer using the similar problem
                answer = f"""Based on a similar problem from our knowledge base:

**Similar Question:** {best_match.get('question', 'N/A')}

**Solution:**
{solution}

**Your Question:** {question}

This solution approach should be applicable to your problem with similar mathematical concepts.
"""
                
                # Convert similarity to confidence score
                confidence = min(0.95, similarity_score + 0.1)  # Cap at 0.95, boost by 0.1
                
                return {
                    'answer': answer,
                    'confidence': confidence,
                    'route_taken': 'rag_vector_search',
                    'similar_problems_found': len(similar_problems),
                    'best_match_similarity': similarity_score
                }
            
            # Medium quality match - provide context but lower confidence
            elif similarity_score > 0.4:
                solution = best_match.get('solution', 'Solution not available')
                
                answer = f"""Found a potentially related problem in our knowledge base:

**Related Question:** {best_match.get('question', 'N/A')}
**Similarity:** {similarity_score:.2f}

**Related Solution:**
{solution}

**Your Question:** {question}

Note: This is a related but not identical problem. The solution approach may need to be adapted for your specific question.
"""
                
                confidence = similarity_score * 0.8  # Lower confidence for medium matches
                
                return {
                    'answer': answer,
                    'confidence': confidence,
                    'route_taken': 'rag_moderate_match',
                    'similar_problems_found': len(similar_problems),
                    'best_match_similarity': similarity_score
                }
            
            else:
                # Low quality match
                logger.info(f"Low similarity match ({similarity_score}), returning low confidence")
                return {
                    'answer': f'Found some related problems but similarity too low ({similarity_score:.2f})',
                    'confidence': similarity_score * 0.5,
                    'route_taken': 'rag_low_match',
                    'similar_problems_found': len(similar_problems),
                    'best_match_similarity': similarity_score
                }
                
        except Exception as e:
            logger.error(f"❌ Error in RAG generation: {e}")
            return {
                'answer': f'RAG system error: {str(e)}',
                'confidence': 0.0,
                'route_taken': 'rag_error',
                'error': str(e)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the RAG system"""
        if self.available and self.mongodb_rag:
            mongodb_status = self.mongodb_rag.get_status()
            return {
                'status': 'available',
                'mongodb_atlas': mongodb_status,
                'message': 'RAG system ready with MongoDB Atlas vector search'
            }
        else:
            return {
                'status': 'unavailable',
                'error': 'MongoDB Atlas not initialized',
                'message': 'RAG system not available'
            }

# Keep backward compatibility with the old class name
class MathematicalRAG(RealMathematicalRAG):
    """Alias for backward compatibility"""
    pass

# Factory functions for backward compatibility
def create_rag_system():
    """Factory function to create RAG system"""
    return RealMathematicalRAG()

def get_math_rag():
    """Factory function for backward compatibility with main API"""
    return RealMathematicalRAG()
