"""
Add Basic Math Problems to MongoDB
=================================
Add simple arithmetic and basic math problems that the RAG should handle
"""

import logging
from real_mongodb_atlas_fixed import RealMongoDBAtlasFixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_basic_math_problems():
    """Add fundamental math problems that should be in the knowledge base"""
    
    mongodb_rag = RealMongoDBAtlasFixed()
    
    basic_problems = [
        {
            "problem": "What is 2+2?",
            "solution": "2 + 2 = 4\n\nThis is basic addition. When we add 2 and 2, we get 4.",
            "topic": "arithmetic",
            "difficulty": "elementary"
        },
        {
            "problem": "What is 5+3?", 
            "solution": "5 + 3 = 8\n\nTo add 5 and 3, we combine the quantities to get 8.",
            "topic": "arithmetic",
            "difficulty": "elementary"
        },
        {
            "problem": "What is 10-4?",
            "solution": "10 - 4 = 6\n\nSubtracting 4 from 10 gives us 6.",
            "topic": "arithmetic", 
            "difficulty": "elementary"
        },
        {
            "problem": "What is 3×4?",
            "solution": "3 × 4 = 12\n\nMultiplying 3 by 4 means adding 3 four times: 3 + 3 + 3 + 3 = 12.",
            "topic": "arithmetic",
            "difficulty": "elementary"
        },
        {
            "problem": "What is 15÷3?",
            "solution": "15 ÷ 3 = 5\n\nDividing 15 by 3 gives us 5, since 3 × 5 = 15.",
            "topic": "arithmetic",
            "difficulty": "elementary"
        },
        {
            "problem": "Solve x + 5 = 12",
            "solution": "To solve x + 5 = 12:\n\nSubtract 5 from both sides:\nx + 5 - 5 = 12 - 5\nx = 7\n\nTherefore, x = 7.",
            "topic": "algebra",
            "difficulty": "basic"
        },
        {
            "problem": "Find the quadratic equation whose roots are 3 and -2",
            "solution": "If the roots are 3 and -2, we can write:\n(x - 3)(x - (-2)) = 0\n(x - 3)(x + 2) = 0\n\nExpanding:\nx² + 2x - 3x - 6 = 0\nx² - x - 6 = 0\n\nTherefore, the quadratic equation is x² - x - 6 = 0.",
            "topic": "algebra",
            "difficulty": "intermediate"
        },
        {
            "problem": "Solve the system: 2x + 3y = 7, x - y = 1",
            "solution": "System of equations:\n2x + 3y = 7 ... (1)\nx - y = 1 ... (2)\n\nFrom equation (2): x = y + 1\n\nSubstitute into equation (1):\n2(y + 1) + 3y = 7\n2y + 2 + 3y = 7\n5y = 5\ny = 1\n\nThen x = y + 1 = 1 + 1 = 2\n\nSolution: x = 2, y = 1",
            "topic": "algebra",
            "difficulty": "intermediate"
        },
        {
            "problem": "What is the derivative of x²?",
            "solution": "The derivative of x² with respect to x is:\n\nd/dx(x²) = 2x\n\nUsing the power rule: if f(x) = xⁿ, then f'(x) = nxⁿ⁻¹",
            "topic": "calculus",
            "difficulty": "basic"
        },
        {
            "problem": "What is ∫x dx?",
            "solution": "The integral of x with respect to x is:\n\n∫x dx = x²/2 + C\n\nWhere C is the constant of integration.",
            "topic": "calculus", 
            "difficulty": "basic"
        }
    ]
    
    logger.info(f"📚 Adding {len(basic_problems)} basic math problems to knowledge base...")
    
    added_count = 0
    for problem_data in basic_problems:
        success = mongodb_rag.store_problem(
            problem_data["problem"],
            problem_data["solution"],
            {
                "topic": problem_data["topic"],
                "difficulty": problem_data["difficulty"],
                "source": "basic_math_curriculum"
            }
        )
        
        if success:
            added_count += 1
    
    logger.info(f"✅ Successfully added {added_count}/{len(basic_problems)} problems")
    
    # Get updated stats
    stats = mongodb_rag.get_stats()
    logger.info(f"📊 Updated database stats: {stats}")
    
    return stats

if __name__ == "__main__":
    add_basic_math_problems()
