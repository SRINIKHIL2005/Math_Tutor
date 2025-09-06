

import logging
from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Only import if available - graceful fallback
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    LANGGRAPH_AVAILABLE = True
    print("✅ LangGraph imports successful")
except ImportError as e:
    print(f"❌ LangGraph not available: {e}")
    LANGGRAPH_AVAILABLE = False

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import working components that we know exist
try:
    from real_guardrails_implementation import MathGuardrailsGateway
    from real_mcp_implementation import WebSearchMCP
    COMPONENTS_AVAILABLE = True
    print("✅ Component imports successful")
except ImportError as e:
    print(f"❌ Component imports failed: {e}")
    COMPONENTS_AVAILABLE = False

class MathAgentState(TypedDict):
    """LangGraph state for math agent"""
    question: str
    answer: str
    confidence: float
    route_taken: str
    error_message: Optional[str]

class RealLangGraphAgent:
    """
    🤖 REAL WORKING LANGGRAPH MATH AGENT
    Only uses what actually works - no fake imports
    """
    
    def __init__(self):
        logger.info("🤖 Initializing REAL Working LangGraph Agent")
        
        self.available = LANGGRAPH_AVAILABLE and COMPONENTS_AVAILABLE
        
        if not self.available:
            logger.warning("⚠️ LangGraph agent running in fallback mode")
            return
            
        # Initialize working components
        try:
            self.guardrails = MathGuardrailsGateway()
            self.web_search = WebSearchMCP()
            logger.info("✅ Components initialized")
        except Exception as e:
            logger.error(f"❌ Component init failed: {e}")
            self.available = False
            return
            
        # Initialize LLM if API key available
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    api_key=openai_api_key,
                    temperature=0.1,
                    max_tokens=1000
                )
                logger.info("✅ OpenAI LLM initialized")
            except Exception as e:
                logger.error(f"❌ LLM init failed: {e}")
                self.llm = None
        else:
            logger.warning("⚠️ No OpenAI API key - using fallback")
            self.llm = None
            
        # Create LangGraph workflow
        try:
            self.workflow = self._create_workflow()
            self.memory = MemorySaver()
            self.app = self.workflow.compile(checkpointer=self.memory)
            logger.info("✅ LangGraph workflow created")
        except Exception as e:
            logger.error(f"❌ Workflow creation failed: {e}")
            self.available = False
    
    def _create_workflow(self) -> StateGraph:
        """Create working LangGraph workflow"""
        workflow = StateGraph(MathAgentState)
        
        # Add nodes
        workflow.add_node("process_question", self._process_question)
        workflow.add_node("generate_answer", self._generate_answer)
        workflow.add_node("finalize", self._finalize_response)
        
        # Set up edges
        workflow.set_entry_point("process_question")
        workflow.add_edge("process_question", "generate_answer")
        workflow.add_edge("generate_answer", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow
    
    def _process_question(self, state: MathAgentState) -> MathAgentState:
        """Process and validate the input question"""
        try:
            question = state["question"]
            
            # Use guardrails if available
            if hasattr(self, 'guardrails'):
                guard_result = self.guardrails.process_input(question, "session")
                if not guard_result.get('approved', True):
                    state["error_message"] = f"Guardrails rejected: {guard_result.get('message', 'Invalid content')}"
                    return state
            
            state["route_taken"] = "processed"
            return state
            
        except Exception as e:
            state["error_message"] = f"Processing failed: {str(e)}"
            return state
    
    def _generate_answer(self, state: MathAgentState) -> MathAgentState:
        """Generate answer using LLM or fallback"""
        try:
            if state.get("error_message"):
                return state
                
            question = state["question"]
            
            # Try LLM if available
            if self.llm:
                messages = [
                    SystemMessage(content="You are a helpful math tutor. Provide clear, step-by-step solutions."),
                    HumanMessage(content=f"Please solve this math problem: {question}")
                ]
                response = self.llm.invoke(messages)
                state["answer"] = response.content
                state["confidence"] = 0.8
                state["route_taken"] = "llm"
            else:
                # Fallback response
                state["answer"] = f"I understand you asked: '{question}'. To provide a complete solution, I would need access to advanced mathematical reasoning capabilities."
                state["confidence"] = 0.3
                state["route_taken"] = "fallback"
            
            return state
            
        except Exception as e:
            state["error_message"] = f"Answer generation failed: {str(e)}"
            state["answer"] = "I apologize, but I encountered an error while solving this problem."
            state["confidence"] = 0.0
            return state
    
    def _finalize_response(self, state: MathAgentState) -> MathAgentState:
        """Finalize the response"""
        if not state.get("answer"):
            state["answer"] = "I'm sorry, I couldn't process your question."
            state["confidence"] = 0.0
        
        return state
    
    async def process_question(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Process a math question through LangGraph workflow"""
        
        if not self.available:
            return {
                "answer": "LangGraph agent is not available. Please install required dependencies: langgraph, langchain-core, langchain-openai",
                "confidence": 0.0,
                "route_taken": "unavailable",
                "error": "Missing dependencies"
            }
        
        try:
            # Initial state
            initial_state = {
                "question": question,
                "answer": "",
                "confidence": 0.0,
                "route_taken": "",
                "error_message": None
            }
            
            # Run workflow
            config = {"configurable": {"thread_id": session_id}}
            result = await self.app.ainvoke(initial_state, config=config)
            
            return {
                "answer": result.get("answer", "No answer generated"),
                "confidence": result.get("confidence", 0.0),
                "route_taken": result.get("route_taken", "unknown"),
                "error": result.get("error_message")
            }
            
        except Exception as e:
            logger.error(f"❌ LangGraph processing failed: {e}")
            return {
                "answer": f"Processing failed: {str(e)}",
                "confidence": 0.0,
                "route_taken": "error",
                "error": str(e)
            }
    
    def process_question_sync(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        """Synchronous version of process_question"""
        import asyncio
        return asyncio.run(self.process_question(question, session_id))
    
    def get_status(self) -> Dict[str, Any]:
        """Get component status"""
        return {
            "component": "LangGraph Agent",
            "available": self.available,
            "langgraph_installed": LANGGRAPH_AVAILABLE,
            "components_available": COMPONENTS_AVAILABLE,
            "llm_available": hasattr(self, 'llm') and self.llm is not None,
            "dependencies_needed": [] if self.available else [
                "langgraph",
                "langchain-core", 
                "langchain-openai",
                "langchain-community"
            ]
        }

# Global instance
_langgraph_agent = None

def get_langgraph_agent():
    """Get LangGraph agent instance"""
    global _langgraph_agent
    if _langgraph_agent is None:
        _langgraph_agent = RealLangGraphAgent()
    return _langgraph_agent

if __name__ == "__main__":
    # Test the component
    print("🧪 Testing LangGraph Agent Component...")
    
    agent = get_langgraph_agent()
    status = agent.get_status()
    
    print("📊 Component Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    if agent.available:
        print("\n🤖 Testing question processing...")
        test_question = "What is 2 + 2?"
        result = agent.process_question_sync(test_question)
        
        print(f"Question: {test_question}")
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Route: {result['route_taken']}")
        if result['error']:
            print(f"Error: {result['error']}")
    else:
        print("\n⚠️ Component not available - install dependencies first")
        print("Required dependencies:", status['dependencies_needed'])
