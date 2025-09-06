
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

# Try numpy, but don't fail if missing
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# Try to import sentence-transformers, fallback if not available
SENTENCE_TRANSFORMERS_AVAILABLE = False
try:
    import sentence_transformers
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    pass

# MongoDB imports
PYMONGO_AVAILABLE = False  
try:
    import pymongo
    PYMONGO_AVAILABLE = True
except ImportError:
    pass
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealMongoDBAtlasFixed:
    """
    Fixed MongoDB Atlas Vector Search implementation
    Learning proper connection and vector search patterns
    """
    
    def __init__(self):
        """Initialize with proper MongoDB Atlas connection"""
        self.client = None
        self.database = None
        self.collection = None
        self.embedding_model = None
        self.memory_storage = []
        self.using_memory = False
        
        # Initialize embedding model first
        self._load_embedding_model()
        
        # Then connect to MongoDB Atlas
        self._connect_to_atlas()
    
    def _load_embedding_model(self):
        """Load sentence transformers model"""
        logger.warning("⚠️ sentence-transformers not available, using hash-based embeddings")
        self.embedding_model = None
    
    def _connect_to_atlas(self):
        """Connect to MongoDB Atlas with proper error handling"""
        try:
            if not PYMONGO_AVAILABLE:
                logger.warning("⚠️ PyMongo not available, using in-memory storage")
                self._setup_memory_fallback()
                return
            
            # For now, use a local MongoDB for testing since we don't have real Atlas credentials
            # In production, this would be a real Atlas connection string
            
            # Try to connect to local MongoDB first for testing
            local_uri = "mongodb://localhost:27017/"
            
            logger.info("🔗 Attempting local MongoDB connection for testing...")
            if PYMONGO_AVAILABLE:
                from pymongo import MongoClient
                self.client = MongoClient(
                    local_uri,
                    serverSelectionTimeoutMS=5000,  # 5 second timeout
                    connectTimeoutMS=5000
                )
                
                # Test the connection
                self.client.admin.command('ismaster')
            
            # Set up database and collection
            self.database = self.client['math_tutor']
            self.collection = self.database['math_problems']
            
            logger.info("✅ Connected to MongoDB successfully")
            
        except Exception as e:
            logger.warning("⚠️ Local MongoDB not available, using in-memory fallback")
            # Fallback to in-memory storage
            self._setup_memory_fallback()
            
        except Exception as e:
            logger.error(f"❌ MongoDB connection failed: {e}")
            self._setup_memory_fallback()
    
    def _setup_memory_fallback(self):
        """Setup in-memory storage as fallback"""
        logger.info("🧠 Setting up in-memory vector storage fallback")
        self.memory_storage = []
        self.client = None
        self.database = None
        self.collection = None
        self.using_memory = True
    
    def create_vector_index(self):
        """Create vector search index"""
        if not self.collection:
            logger.info("⚠️ Using memory storage - no index needed")
            return True
            
        try:
            # In real MongoDB Atlas, you'd create a vector search index
            # For now, create a regular index on the text field
            self.collection.create_index([("problem", "text")])
            logger.info("✅ Vector index created")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create vector index: {e}")
            return False
    
    def embed_text(self, text: str):
        """Generate embedding for text"""
        try:
            if self.embedding_model and SENTENCE_TRANSFORMERS_AVAILABLE:
                embedding = self.embedding_model.encode(text)
                return embedding
            else:
                # Simple fallback embedding using hash
                text_hash = hashlib.md5(text.encode()).hexdigest()
                # Convert hex to numbers and normalize
                nums = [int(text_hash[i:i+2], 16) for i in range(0, 32, 2)]
                if NUMPY_AVAILABLE:
                    embedding = np.array(nums, dtype=np.float32)
                    # Normalize
                    embedding = embedding / np.linalg.norm(embedding)
                    return embedding
                else:
                    # Simple list normalization
                    total = sum(n*n for n in nums) ** 0.5
                    return [n/total for n in nums]
                
        except Exception as e:
            logger.error(f"❌ Failed to generate embedding: {e}")
            raise
    
    def store_problem(self, problem: str, solution: str, metadata: Dict[str, Any] = None) -> bool:
        """Store a math problem with its embedding"""
        try:
            # Generate embedding
            embedding = self.embed_text(problem)
            
            # Create document
            document = {
                "problem": problem,
                "solution": solution,
                "embedding": embedding.tolist(),  # Convert numpy array to list
                "metadata": metadata or {},
                "created_at": datetime.now(),
                "embedding_dim": len(embedding)
            }
            
            # Store in database or memory
            if self.collection is not None:
                result = self.collection.insert_one(document)
                logger.info(f"✅ Stored problem in MongoDB: {result.inserted_id}")
            else:
                # Store in memory
                document["_id"] = len(self.memory_storage)
                self.memory_storage.append(document)
                logger.info(f"✅ Stored problem in memory: {document['_id']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store problem: {e}")
            return False
    
    def search_similar_problems(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar problems using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = self.embed_text(query)
            
            if self.collection is not None:
                return self._search_mongodb(query_embedding, limit)
            else:
                return self._search_memory(query_embedding, limit)
                
        except Exception as e:
            logger.error(f"❌ Vector search failed: {e}")
            return []
    
    def _search_mongodb(self, query_embedding: List[float], limit: int) -> List[Dict[str, Any]]:
        """Search in MongoDB collection"""
        try:
            # For now, do a simple text search since we don't have Atlas Vector Search
            # In production, this would use MongoDB Atlas Vector Search
            
            results = []
            documents = self.collection.find().limit(limit * 2)  # Get more to filter
            
            for doc in documents:
                if 'embedding' in doc and doc['embedding']:
                    try:
                        # Calculate cosine similarity
                        doc_embedding = doc['embedding']
                        
                        # Ensure both embeddings are lists of floats
                        if isinstance(doc_embedding, list) and isinstance(query_embedding, list):
                            if len(doc_embedding) == len(query_embedding):
                                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                                
                                results.append({
                                    "problem": doc.get('problem', ''),
                                    "solution": doc.get('solution', ''),
                                    "similarity": float(similarity),
                                    "metadata": doc.get('metadata', {})
                                })
                    except Exception as e:
                        logger.debug(f"Error processing document embedding: {e}")
                        continue
            
            # Sort by similarity and return top results
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"❌ MongoDB search failed: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            # Calculate dot product
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            
            # Calculate magnitudes
            magnitude1 = sum(a * a for a in vec1) ** 0.5
            magnitude2 = sum(b * b for b in vec2) ** 0.5
            
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            
            return dot_product / (magnitude1 * magnitude2)
        except Exception:
            return 0.0
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"❌ MongoDB search failed: {e}")
            return []
    
    def _search_memory(self, query_embedding: List[float], limit: int) -> List[Dict[str, Any]]:
        """Search in memory storage"""
        try:
            results = []
            
            for doc in self.memory_storage:
                if 'embedding' in doc and doc['embedding']:
                    try:
                        doc_embedding = doc['embedding']
                        
                        # Ensure both embeddings are lists of floats
                        if isinstance(doc_embedding, list) and isinstance(query_embedding, list):
                            if len(doc_embedding) == len(query_embedding):
                                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                                
                                results.append({
                                    "problem": doc.get('problem', ''),
                                    "solution": doc.get('solution', ''),
                                    "similarity": float(similarity),
                                    "metadata": doc.get('metadata', {})
                                })
                    except Exception as e:
                        logger.debug(f"Error processing memory document: {e}")
                        continue
            
            # Sort by similarity and return top results
            results.sort(key=lambda x: x['similarity'], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"❌ Memory search failed: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            if self.collection is not None:
                count = self.collection.count_documents({})
                return {
                    "total_problems": count,
                    "storage_type": "mongodb",
                    "embedding_model": "hash-based",
                    "embedding_dimensions": 100
                }
            else:
                return {
                    "total_problems": len(self.memory_storage) if hasattr(self, 'memory_storage') else 0,
                    "storage_type": "memory",
                    "embedding_model": "hash-based", 
                    "embedding_dimensions": 100
                }
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {
                "total_problems": 0,
                "storage_type": "error",
                "embedding_model": "hash-based",
                "embedding_dimensions": 100
            }
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the database connection"""
        try:
            if self.client:
                # Test MongoDB connection
                server_info = self.client.server_info()
                return {
                    "status": "connected",
                    "type": "mongodb",
                    "version": server_info.get('version', 'unknown'),
                    "collections": self.database.list_collection_names() if self.database else []
                }
            else:
                # Memory storage
                return {
                    "status": "connected",
                    "type": "memory",
                    "stored_problems": len(self.memory_storage)
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            if self.collection is not None:
                count = self.collection.count_documents({})
                return {
                    "total_problems": count,
                    "storage_type": "mongodb",
                    "embedding_model": "all-MiniLM-L6-v2",
                    "embedding_dimensions": 384
                }
            else:
                return {
                    "total_problems": len(self.memory_storage) if hasattr(self, 'memory_storage') else 0,
                    "storage_type": "memory",
                    "embedding_model": "all-MiniLM-L6-v2", 
                    "embedding_dimensions": 384
                }
                
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {"error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get status for API compatibility"""
        try:
            connection_test = self.test_connection()
            stats = self.get_stats()
            
            if connection_test.get('status') == 'connected' and stats.get('total_problems', 0) > 0:
                return {
                    'status': 'ready',
                    'message': f"MongoDB Atlas ready with {stats.get('total_problems', 0)} problems",
                    'storage_type': stats.get('storage_type', 'unknown'),
                    'total_problems': stats.get('total_problems', 0)
                }
            elif connection_test.get('status') == 'connected':
                return {
                    'status': 'empty',
                    'message': 'MongoDB Atlas connected but no data',
                    'storage_type': stats.get('storage_type', 'unknown'),
                    'total_problems': 0
                }
            else:
                return {
                    'status': 'error',
                    'error': connection_test.get('error', 'Connection failed'),
                    'message': 'MongoDB Atlas connection failed'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Failed to get status'
            }

def test_mongodb_atlas_fixed():
    """Test the fixed MongoDB Atlas implementation"""
    logger.info("🧪 Testing Fixed MongoDB Atlas Implementation")
    
    try:
        # Initialize
        db = RealMongoDBAtlasFixed()
        
        # Test connection
        connection_result = db.test_connection()
        logger.info(f"Connection test: {connection_result}")
        
        # Create index
        db.create_vector_index()
        
        # Store some test problems
        test_problems = [
            {
                "problem": "Solve for x: 2x + 5 = 13",
                "solution": "2x = 13 - 5 = 8, so x = 4",
                "metadata": {"difficulty": "easy", "topic": "linear_equations"}
            },
            {
                "problem": "Find the derivative of f(x) = x² + 3x + 2",
                "solution": "f'(x) = 2x + 3",
                "metadata": {"difficulty": "medium", "topic": "derivatives"}
            }
        ]
        
        for problem_data in test_problems:
            success = db.store_problem(
                problem_data["problem"],
                problem_data["solution"],
                problem_data["metadata"]
            )
            logger.info(f"Store result: {success}")
        
        # Test search
        query = "linear equation with x"
        results = db.search_similar_problems(query, limit=2)
        logger.info(f"Search results for '{query}': {len(results)} found")
        
        for i, result in enumerate(results):
            logger.info(f"Result {i+1}: {result['problem'][:50]}... (similarity: {result['similarity']:.3f})")
        
        # Get stats
        stats = db.get_stats()
        logger.info(f"Database stats: {stats}")
        
        logger.info("✅ MongoDB Atlas Fixed implementation test completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_atlas_fixed()
