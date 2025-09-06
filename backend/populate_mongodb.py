"""
MongoDB Atlas Data Population Script
===================================
Populate MongoDB Atlas with data from JSON files if needed
"""

import os
import json
import logging
from real_mongodb_atlas_fixed import RealMongoDBAtlasFixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_mongodb_from_json():
    """Populate MongoDB Atlas with data from JSON files"""
    
    # Initialize MongoDB Atlas
    mongodb_rag = RealMongoDBAtlasFixed()
    
    # Check current stats
    stats = mongodb_rag.get_stats()
    logger.info(f"Current MongoDB stats: {stats}")
    
    current_count = stats.get('total_problems', 0)
    
    if current_count > 0:
        logger.info(f"✅ MongoDB already has {current_count} problems. Skipping population.")
        return stats
    
    logger.info("📚 MongoDB is empty. Populating with JSON data...")
    
    # Load data from JSON files
    data_folder = "../data"
    knowledge_files = [
        "enhanced_math_dataset.json",
        "sample_math_qa.json",
        "data/data/dataset.json"  # The large JEE dataset
    ]
    
    # Add GPT response files with high-quality solutions
    response_files = [
        "data/data/responses/GPT4_normal_responses/responses.json",
        "data/data/responses/GPT4_CoT_responses/responses.json", 
        "data/data/responses/GPT4_CoT_self_refine_responses/responses.json",
        "data/data/responses/GPT4_CoT+SC_responses/responses.json",
        "data/data/responses/GPT4_CoT+OneShot_responses/responses.json"
    ]
    
    knowledge_files.extend(response_files)
    
    total_added = 0
    
    for filename in knowledge_files:
        filepath = os.path.join(data_folder, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                logger.info(f"📖 Processing {filename}...")
                
                # Handle different file formats
                if "responses/" in filename:
                    # GPT response files have rich question-answer pairs
                    for item in data:
                        question = item.get('question', '')
                        
                        # Extract the best available solution from GPT responses
                        solution = ""
                        response_type = ""
                        
                        # Priority order: CoT+SC > CoT_self_refine > CoT > normal
                        if 'GPT4_CoT+SC_response' in item:
                            choices = item['GPT4_CoT+SC_response'].get('choices', [])
                            if choices:
                                solution = choices[0].get('message', {}).get('content', '')
                                response_type = "CoT+SC"
                        elif 'GPT4_CoT_self_refine_response' in item:
                            choices = item['GPT4_CoT_self_refine_response'].get('choices', [])
                            if choices:
                                solution = choices[0].get('message', {}).get('content', '')
                                response_type = "CoT_self_refine"
                        elif 'GPT4_CoT_response' in item:
                            choices = item['GPT4_CoT_response'].get('choices', [])
                            if choices:
                                solution = choices[0].get('message', {}).get('content', '')
                                response_type = "CoT"
                        elif 'GPT4_normal_response' in item:
                            choices = item['GPT4_normal_response'].get('choices', [])
                            if choices:
                                solution = choices[0].get('message', {}).get('content', '')
                                response_type = "normal"
                        
                        if question and solution:
                            metadata = {
                                'topic': item.get('subject', 'unknown'),
                                'difficulty': 'JEE Advanced',
                                'question_type': item.get('type', 'unknown'),
                                'source_file': filename,
                                'response_type': response_type,
                                'gold_answer': item.get('gold', ''),
                                'description': item.get('description', ''),
                                'solution_quality': 'high'  # GPT-4 solutions are high quality
                            }
                            
                            success = mongodb_rag.store_problem(question, solution, metadata)
                            if success:
                                total_added += 1
                            
                            if total_added % 50 == 0:  # Less frequent logging for large datasets
                                logger.info(f"   Added {total_added} problems so far...")
                
                else:
                    # Regular dataset files 
                    for item in data:
                        question = item.get('question', '')
                        solution = item.get('solution', '') or item.get('answer', '')
                        
                        if question and solution:
                            metadata = {
                                'topic': item.get('topic', 'unknown'),
                                'difficulty': item.get('difficulty', 'unknown'),
                                'source_file': filename,
                                'solution_quality': 'standard'
                            }
                            
                            success = mongodb_rag.store_problem(question, solution, metadata)
                            if success:
                                total_added += 1
                            
                            if total_added % 10 == 0:
                                logger.info(f"   Added {total_added} problems so far...")
                
                logger.info(f"✅ Completed {filename}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process {filename}: {e}")
        else:
            logger.warning(f"⚠️ File not found: {filepath}")
    
    # Get final stats
    final_stats = mongodb_rag.get_stats()
    logger.info(f"🎉 Population complete! Final stats: {final_stats}")
    
    return final_stats

def check_mongodb_status():
    """Check MongoDB Atlas status and data"""
    try:
        mongodb_rag = RealMongoDBAtlasFixed()
        
        # Test connection
        connection_result = mongodb_rag.test_connection()
        print(f"📡 Connection Status: {connection_result}")
        
        # Get stats
        stats = mongodb_rag.get_stats()
        print(f"📊 Database Stats: {stats}")
        
        # Test search if we have data
        if stats.get('total_problems', 0) > 0:
            print("\n🔍 Testing search functionality...")
            test_query = "solve quadratic equation"
            results = mongodb_rag.search_similar_problems(test_query, limit=3)
            print(f"Search results for '{test_query}':")
            for i, result in enumerate(results, 1):
                print(f"  {i}. Similarity: {result.get('similarity', 0):.3f}")
                print(f"     Question: {result.get('question', 'N/A')[:100]}...")
                print()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MongoDB check failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MongoDB Atlas Data Population and Status Check")
    print("=" * 60)
    
    # First check status
    if check_mongodb_status():
        # Populate if needed
        populate_mongodb_from_json()
        print("\n" + "=" * 60)
        print("✅ Process complete! MongoDB Atlas should be ready for RAG.")
    else:
        print("❌ MongoDB connection failed. Please check your MONGODB_URI environment variable.")
