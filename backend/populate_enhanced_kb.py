"""
🚀 Enhanced Knowledge Base Populator
Populates MongoDB Atlas with 7500+ math problems from all datasets
"""

import json
import os
import sys
from datetime import datetime
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def load_all_datasets():
    """Load all available math datasets"""
    datasets = []
    data_root = "f:/Internships/Maths_Pofessor/Real_Math_tutor/data"
    
    # Dataset files to load
    dataset_files = [
        "converted_datasets/external_datasets_combined.json",
        "converted_datasets/gsm8k_converted.json", 
        "enhanced_math_dataset.json",
        "sample_math_qa.json",
        "data/data/dataset.json"
    ]
    
    total_loaded = 0
    
    for dataset_file in dataset_files:
        file_path = os.path.join(data_root, dataset_file)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if isinstance(data, list):
                    datasets.extend(data)
                    loaded_count = len(data)
                    total_loaded += loaded_count
                    logger.info(f"✅ Loaded {loaded_count} problems from {dataset_file}")
                else:
                    logger.warning(f"⚠️ {dataset_file} does not contain a list format")
                    
            except Exception as e:
                logger.error(f"❌ Failed to load {dataset_file}: {e}")
        else:
            logger.warning(f"⚠️ File not found: {file_path}")
    
    logger.info(f"📚 Total problems loaded from all datasets: {total_loaded}")
    return datasets

def normalize_problem_format(problem):
    """Normalize problem format for consistent storage"""
    
    # Create normalized problem structure
    normalized = {
        "id": problem.get("id", f"prob_{hash(str(problem))}")[:50],
        "question": problem.get("question", problem.get("problem", "")),
        "solution": problem.get("solution", problem.get("explanation", "")),
        "answer": problem.get("answer", problem.get("final_answer", "")),
        "topic": problem.get("topic", problem.get("subject", "General Math")),
        "difficulty": problem.get("difficulty", "medium"),
        "subject": problem.get("subject", "Mathematics"),
        "source": problem.get("source", "Unknown"),
        "created_at": datetime.now().isoformat(),
        "tags": problem.get("tags", []),
        "metadata": {
            "original_keys": list(problem.keys()),
            "data_quality": "processed"
        }
    }
    
    # Ensure all text fields are strings
    for field in ["question", "solution", "answer"]:
        if field in normalized:
            normalized[field] = str(normalized[field]) if normalized[field] else ""
    
    return normalized

def create_mongodb_indexes(collection):
    """Create indexes for efficient searching"""
    try:
        # Text search indexes
        collection.create_index([
            ("question", "text"),
            ("solution", "text"),
            ("answer", "text"),
            ("topic", "text")
        ], name="full_text_search")
        
        # Individual field indexes
        collection.create_index("topic")
        collection.create_index("difficulty") 
        collection.create_index("subject")
        collection.create_index("source")
        
        logger.info("✅ Created MongoDB indexes for efficient searching")
        
    except Exception as e:
        logger.error(f"❌ Failed to create indexes: {e}")

def populate_knowledge_base():
    """Main function to populate MongoDB Atlas with all math problems"""
    
    # Load MongoDB connection
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        logger.error("❌ MONGODB_URI not found in environment variables")
        return False
    
    try:
        # Connect to MongoDB
        client = MongoClient(mongodb_uri)
        db = client.math_tutor
        collection = db.enhanced_problems
        
        logger.info("✅ Connected to MongoDB Atlas")
        
        # Load all datasets
        logger.info("📂 Loading all available datasets...")
        all_problems = load_all_datasets()
        
        if not all_problems:
            logger.error("❌ No problems loaded from datasets")
            return False
        
        # Clear existing data (optional - comment out to append)
        logger.info("🗑️ Clearing existing data...")
        collection.delete_many({})
        
        # Normalize and insert problems
        logger.info("🔄 Normalizing and inserting problems...")
        normalized_problems = []
        
        for i, problem in enumerate(all_problems):
            try:
                normalized = normalize_problem_format(problem)
                
                # Skip problems without question or solution
                if not normalized["question"] or not normalized["solution"]:
                    continue
                    
                normalized_problems.append(normalized)
                
                if (i + 1) % 1000 == 0:
                    logger.info(f"📊 Processed {i + 1}/{len(all_problems)} problems")
                    
            except Exception as e:
                logger.error(f"❌ Failed to normalize problem {i}: {e}")
                continue
        
        # Insert in batches
        batch_size = 1000
        inserted_count = 0
        
        for i in range(0, len(normalized_problems), batch_size):
            batch = normalized_problems[i:i + batch_size]
            try:
                result = collection.insert_many(batch, ordered=False)
                inserted_count += len(result.inserted_ids)
                logger.info(f"✅ Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} problems")
            except Exception as e:
                logger.error(f"❌ Failed to insert batch {i//batch_size + 1}: {e}")
        
        # Create indexes
        create_mongodb_indexes(collection)
        
        # Final statistics
        total_in_db = collection.count_documents({})
        
        logger.info("🎉 KNOWLEDGE BASE POPULATION COMPLETE!")
        logger.info(f"📊 Statistics:")
        logger.info(f"   - Total problems processed: {len(normalized_problems)}")
        logger.info(f"   - Successfully inserted: {inserted_count}")
        logger.info(f"   - Total in database: {total_in_db}")
        
        # Sample the data
        sample_problem = collection.find_one()
        if sample_problem:
            logger.info(f"📝 Sample problem:")
            logger.info(f"   - Question: {sample_problem.get('question', 'N/A')[:100]}...")
            logger.info(f"   - Topic: {sample_problem.get('topic', 'N/A')}")
            logger.info(f"   - Source: {sample_problem.get('source', 'N/A')}")
        
        client.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to populate knowledge base: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Enhanced Knowledge Base Population...")
    print("=" * 60)
    
    success = populate_knowledge_base()
    
    print("=" * 60)
    if success:
        print("✅ Knowledge base population completed successfully!")
        print("🚀 Your math tutor now has access to 7500+ problems!")
    else:
        print("❌ Knowledge base population failed. Check logs for details.")
    
    print("=" * 60)
