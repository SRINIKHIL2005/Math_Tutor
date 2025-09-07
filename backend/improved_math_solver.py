"""
🧠 Improved Math Solver with Proper Routing
Architecture: RAG → MCP → Gemini → Simple Fallback
Features: Voice support, source tracking, enhanced knowledge base
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import asyncio
from datetime import datetime
import os
import json
from dotenv import load_dotenv

# Import AI components
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False

# Text-to-Speech for voice output
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="🚀 Improved Math Tutor API",
    description="Complete Math Tutoring System with Voice, Proper Routing & Enhanced KB",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:3001",
        "https://srinikhil2005.github.io",
        "https://srinikhil2005.github.io/Math_Tutor",
        "https://*.onrender.com",
        "https://math-tutor-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    session_id: Optional[str] = "default"
    use_voice: Optional[bool] = False

class AnswerResponse(BaseModel):
    question: str
    answer: str
    confidence: float
    route_taken: str
    component_used: str
    source_info: str  # New: Shows where answer came from
    timestamp: str
    voice_url: Optional[str] = None  # New: For voice output
    error: Optional[str] = None

class FeedbackRequest(BaseModel):
    question: str
    generated_answer: str
    human_rating: int
    human_feedback: Optional[str] = None
    corrected_answer: Optional[str] = None
    session_id: Optional[str] = "default"

# Initialize components with graceful fallbacks
components_status = {}

# Initialize Enhanced Knowledge Base (Local)
try:
    from local_enhanced_kb import get_enhanced_kb
    enhanced_kb = get_enhanced_kb()
    components_status["Enhanced Knowledge Base"] = f"✅ WORKING ({enhanced_kb.get_stats()['total_problems']} problems)"
    logger.info(f"✅ Enhanced Knowledge Base loaded with {enhanced_kb.get_stats()['total_problems']} problems")
except Exception as e:
    enhanced_kb = None
    components_status["Enhanced Knowledge Base"] = f"❌ FAILED: {str(e)[:50]}"
    logger.error(f"❌ Enhanced KB failed: {e}")
    try:
        tts_engine = pyttsx3.init()
        tts_engine.setProperty('rate', 150)
        tts_engine.setProperty('volume', 0.9)
        logger.info("✅ Text-to-Speech engine initialized")
    except Exception as e:
        logger.error(f"❌ TTS initialization failed: {e}")
        tts_engine = None

# Import existing components
components_status = {}

# Load existing components with status
try:
    from real_mathematical_rag_complete import EnhancedMathematicalRAG
    math_rag = EnhancedMathematicalRAG()
    components_status["Mathematical RAG"] = "✅ WORKING"
    logger.info("✅ Mathematical RAG ready")
except Exception as e:
    math_rag = None
    components_status["Mathematical RAG"] = f"❌ FAILED: {str(e)[:50]}"

try:
    from real_mcp_implementation import WebSearchMCP
    web_search = WebSearchMCP()
    components_status["MCP Web Search"] = "✅ WORKING"
    logger.info("✅ MCP Web Search ready")
except Exception as e:
    web_search = None
    components_status["MCP Web Search"] = f"❌ FAILED: {str(e)[:50]}"

try:
    from real_human_feedback_learning import HumanFeedbackLearning
    learning_system = HumanFeedbackLearning()
    components_status["Human Feedback Learning"] = "✅ WORKING"
    logger.info("✅ Human Feedback Learning ready")
except Exception as e:
    learning_system = None
    components_status["Human Feedback Learning"] = f"❌ FAILED: {str(e)[:50]}"

# Calculate system health
working_components = sum(1 for status in components_status.values() if "✅" in status)
total_components = len(components_status)
completion_rate = f"{(working_components/total_components)*100:.1f}%" if total_components > 0 else "0%"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Improved Math Tutor API",
        "knowledge_base_size": enhanced_kb.get_stats()['total_problems'] if enhanced_kb else 0,
        "completion_rate": completion_rate
    }

@app.get("/status")
async def get_system_status():
    """Get detailed system status"""
    return {
        "timestamp": datetime.now().isoformat(),
        "components": components_status,
        "completion_rate": completion_rate,
        "working_components": working_components,
        "total_components": total_components,
        "knowledge_base_size": enhanced_kb.get_stats()['total_problems'] if enhanced_kb else 0,
        "features": {
            "voice_synthesis": TTS_AVAILABLE,
            "gemini_api": GEMINI_AVAILABLE and bool(os.getenv("GEMINI_API_KEY")),
            "enhanced_kb": enhanced_kb is not None and enhanced_kb.get_stats()['total_problems'] > 0
        },
        "api_keys": {
            "GEMINI_API_KEY": "✅ Available" if os.getenv("GEMINI_API_KEY") else "❌ Missing",
            "TAVILY_API_KEY": "✅ Available" if os.getenv("TAVILY_API_KEY") else "❌ Missing"
        }
    }

async def generate_voice_response(text: str, session_id: str) -> Optional[str]:
    """Generate voice output for the answer"""
    if not tts_engine:
        return None
    
    try:
        # Create voice file path
        voice_dir = "f:/Internships/Maths_Pofessor/Real_Math_tutor/voice_output"
        os.makedirs(voice_dir, exist_ok=True)
        
        voice_file = f"{voice_dir}/response_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # Generate speech
        tts_engine.save_to_file(text, voice_file)
        tts_engine.runAndWait()
        
        return voice_file
        
    except Exception as e:
        logger.error(f"Voice generation failed: {e}")
        return None

@app.post("/solve", response_model=AnswerResponse)
async def solve_question(request: QuestionRequest):
    """
    🎯 IMPROVED MATH SOLVER with proper routing:
    1. Enhanced Knowledge Base (7500+ problems)
    2. Mathematical RAG
    3. MCP Web Search
    4. Gemini API
    5. Simple fallback
    """
    
    try:
        logger.info(f"🔍 Processing question: {request.question[:100]}...")
        
        # ROUTE 1: Enhanced Knowledge Base (PRIMARY - 7500+ problems)
        if enhanced_kb:
            try:
                logger.info("📚 Searching Enhanced Knowledge Base...")
                kb_results = enhanced_kb.search_similar(request.question, threshold=0.6, max_results=3)
                
                if kb_results and kb_results[0].get('similarity', 0) > 0.7:
                    best_match = kb_results[0]
                    
                    # Format the solution nicely
                    solution = best_match.get('solution', '')
                    if not solution:
                        solution = best_match.get('answer', 'Solution available in knowledge base')
                    
                    answer = f"**Step-by-Step Solution:**\n\n{solution}"
                    confidence = min(0.95, best_match['similarity'] + 0.1)
                    
                    # Generate voice if requested
                    voice_url = None
                    if request.use_voice:
                        voice_url = await generate_voice_response(answer, request.session_id)
                    
                    logger.info(f"✅ Found high-quality match with {best_match['similarity']:.2f} similarity")
                    
                    return AnswerResponse(
                        question=request.question,
                        answer=answer,
                        confidence=confidence,
                        route_taken="enhanced_knowledge_base",
                        component_used="Enhanced Knowledge Base",
                        source_info=f"Knowledge Base Match (Topic: {best_match.get('topic', 'General')}, Similarity: {best_match['similarity']:.2f})",
                        timestamp=datetime.now().isoformat(),
                        voice_url=voice_url
                    )
                else:
                    similarity = kb_results[0]['similarity'] if kb_results else 0
                    logger.info(f"KB similarity too low: {similarity:.2f}")
            
            except Exception as e:
                logger.error(f"❌ Enhanced KB search failed: {e}")
        
        # ROUTE 2: Mathematical RAG (SECONDARY)
        if math_rag:
            try:
                logger.info("🧮 Trying Mathematical RAG...")
                rag_result = math_rag.generate_solution_with_rag(request.question)
                
                if rag_result.get('confidence', 0) > 0.7:
                    # Generate voice if requested
                    voice_url = None
                    if request.use_voice:
                        voice_url = await generate_voice_response(rag_result['answer'], request.session_id)
                    
                    return AnswerResponse(
                        question=request.question,
                        answer=rag_result['answer'],
                        confidence=rag_result['confidence'],
                        route_taken="mathematical_rag",
                        component_used="Mathematical RAG System",
                        source_info=f"RAG Retrieval (Confidence: {rag_result['confidence']:.2f})",
                        timestamp=datetime.now().isoformat(),
                        voice_url=voice_url
                    )
                else:
                    logger.info(f"RAG confidence too low: {rag_result.get('confidence', 0)}")
            
            except Exception as e:
                logger.error(f"❌ Mathematical RAG failed: {e}")
        
        # ROUTE 3: MCP Web Search (TERTIARY)
        if web_search:
            try:
                logger.info("🌐 Trying MCP Web Search...")
                search_results = await web_search.search(request.question, max_results=3)
                
                if (search_results and 
                    isinstance(search_results, dict) and 
                    search_results.get('results') and 
                    len(search_results['results']) > 0):
                    
                    first_result = search_results['results'][0]
                    if isinstance(first_result, dict):
                        content = first_result.get('content', 
                                 first_result.get('snippet', 
                                 first_result.get('title', 'Search result available')))
                    else:
                        content = str(first_result)[:500]
                    
                    answer = f"**Based on web search:**\n\n{content[:500]}"
                    
                    # Generate voice if requested
                    voice_url = None
                    if request.use_voice:
                        voice_url = await generate_voice_response(answer, request.session_id)
                    
                    return AnswerResponse(
                        question=request.question,
                        answer=answer,
                        confidence=0.8,
                        route_taken="mcp_web_search",
                        component_used="MCP Web Search",
                        source_info="Web Search Results via MCP",
                        timestamp=datetime.now().isoformat(),
                        voice_url=voice_url
                    )
            
            except Exception as e:
                logger.error(f"❌ MCP Web Search failed: {e}")
        
        # ROUTE 4: Gemini API (FINAL AI FALLBACK)
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if GEMINI_AVAILABLE and gemini_api_key and "your-" not in gemini_api_key.lower():
            try:
                logger.info("🤖 Using Gemini API as final fallback...")
                genai.configure(api_key=gemini_api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                You are a mathematics professor and expert tutor. Solve this mathematical problem with clear, step-by-step explanations:
                
                Question: {request.question}
                
                Please provide:
                1. A detailed step-by-step solution with clear mathematical reasoning
                2. Show all calculations and intermediate steps
                3. Explain the key concepts and formulas used
                4. Highlight the final answer clearly
                5. Use proper mathematical notation
                
                Format your response as a comprehensive tutorial that helps students understand both the solution process and underlying concepts.
                """
                
                response = model.generate_content(prompt)
                
                if response and response.text:
                    # Generate voice if requested
                    voice_url = None
                    if request.use_voice:
                        voice_url = await generate_voice_response(response.text, request.session_id)
                    
                    return AnswerResponse(
                        question=request.question,
                        answer=response.text,
                        confidence=0.92,
                        route_taken="gemini_api_fallback",
                        component_used="Google Gemini AI",
                        source_info="Google Gemini 1.5 Flash AI Model",
                        timestamp=datetime.now().isoformat(),
                        voice_url=voice_url
                    )
                
            except Exception as e:
                logger.error(f"❌ Gemini API failed: {e}")
        else:
            logger.warning("⚠️ Gemini API not available - missing or invalid API key")
        
        # ROUTE 5: Simple fallback (LAST RESORT)
        fallback_answer = f"I understand you're asking about: '{request.question}'. I'm unable to provide a complete solution at the moment. Please try rephrasing your question or check if all components are properly configured."
        
        return AnswerResponse(
            question=request.question,
            answer=fallback_answer,
            confidence=0.3,
            route_taken="simple_fallback",
            component_used="Basic Fallback Handler",
            source_info="System Fallback Response",
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Question processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for learning system"""
    
    try:
        if learning_system:
            await learning_system.process_feedback({
                "question_id": f"{request.question[:50]}_{datetime.now().isoformat()}",
                "question_text": request.question,
                "answer_text": request.generated_answer,
                "rating": request.human_rating,
                "feedback_text": request.human_feedback,
                "corrected_answer": request.corrected_answer,
                "session_id": request.session_id
            })
        
        return {
            "message": "Feedback recorded successfully",
            "timestamp": datetime.now().isoformat(),
            "learning_system_available": learning_system is not None
        }
        
    except Exception as e:
        logger.error(f"❌ Feedback recording failed: {e}")
        raise HTTPException(status_code=500, detail=f"Feedback recording failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
