# 🤖 REAL Enterprise Math Tutoring System


[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.0.55+-purple.svg)](https://langchain-ai.github.io/langgraph/)
[![MongoDB Atlas](https://img.shields.io/badge/MongoDB-Atlas-green.svg)](https://www.mongodb.com/atlas)

## 🏢 Enterprise Architecture

This is a **complete enterprise-grade implementation** of the Math Tutor assignment requirements, featuring:

### ✅ **Assignment Requirements Met:**
- **✅ AI Gateway with Guardrails**: Input/output validation and safety checks
- **✅ Real Vector Database**: MongoDB Atlas with sentence-transformers embeddings
- **✅ MCP Integration**: Model Context Protocol server for web search (MANDATORY requirement)
- **✅ Agent Framework**: LangGraph routing pipeline with proper workflow nodes
- **✅ DSPy Optimization**: Human-in-the-loop feedback learning system
- **✅ JEE Benchmarking**: Automated evaluation against JEE entrance exam problems

### 🎯 **Core Features:**
- **Smart Routing**: Intelligent decision between knowledge base search and web search
- **Real Vector Search**: MongoDB Atlas Vector Search with actual embeddings
- **Web Search Integration**: Tavily API through MCP server protocol
- **Human Feedback Loop**: DSPy-powered continuous improvement
- **Enterprise APIs**: Complete FastAPI backend with proper error handling
- **Modern Frontend**: React application with real-time status monitoring

## 🏗️ System Architecture and Design

This project is built on a robust, multi-component architecture designed for scalability, maintainability, and continuous improvement. It follows a microservices-inspired pattern where distinct responsibilities are handled by specialized components.

### High-Level Design

The system's workflow is orchestrated by a central backend that routes requests through an intelligent AI agent. The agent decides the best strategy for solving a math problem, either by consulting its internal knowledge base or by searching the web. A continuous learning loop is established through user feedback, allowing the system to improve over time.

Here is a high-level overview of the request flow:

```text
+-----------------+      +---------------------+      +----------------------+
|  React Frontend |----->|  FastAPI Backend    |----->|  LangGraph Agent     |
| (User Interface)|      |  (API Gateway)      |      | (Orchestrator)       |
+-----------------+      +---------------------+      +----------+-----------+
        ^                                                         |
        | (Solution &                                             | Routing
        |  Processing Path)                                       v
        |                                               +---------+---------+
+-----------------+                                     |   Router Node     |
| DSPy Optimizer  |<----(Feedback)----------------------+---------+---------+
| (Feedback Loop) |                                          /           \
+-----------------+                                         /             \ (KB vs Web)
                                                           v               v
                                                +-----------------+     +----------------+
                                                |  Vector DB      |     |  MCP Server    |
                                                | (MongoDB Atlas) |     | (Tavily Search)|
                                                +-----------------+     +----------------+
                                                        \                   /
                                                         \                 /
                                                          v               v
                                                      +---------------------+
                                                      | Response Generation |
                                                      |      (LLM)          |
                                                      +---------------------+
                                                                |
                                                                v
                                                      (Back to FastAPI)
```

**Workflow Steps:**
1.  **User Interaction**: The user submits a math question through the React frontend.
2.  **API Gateway**: The FastAPI backend receives the request at the `/solve` endpoint.
3.  **Agent Orchestration**: The request is handed off to the LangGraph agent.
4.  **Input Guardrails**: The agent first validates and sanitizes the input question.
5.  **Intelligent Routing**: A router node within the agent analyzes the question. Based on a confidence score, it decides whether the question can be answered using the internal Knowledge Base (for known problem types) or requires external web search (for novel or complex problems).
6.  **Information Retrieval**:
    *   **Knowledge Base Search**: If routed to the KB, a vector search is performed in MongoDB Atlas to find similar, previously solved problems.
    *   **Web Search**: If routed to the web, the agent calls the MCP Server, which uses the Tavily API to perform a targeted mathematical web search.
7.  **Response Generation**: The retrieved context (from either KB or web) is passed to a large language model (e.g., GPT-4) to generate a step-by-step solution.
8.  **Output Guardrails**: The generated answer is checked for safety, correctness, and formatting before being finalized.
9.  **Response to User**: The final answer, along with metadata like the processing path and confidence score, is sent back to the frontend.
10. **Human-in-the-Loop Feedback**: The user can rate the solution. This feedback is sent to the `/feedback` endpoint and processed by the DSPy optimization system, which uses it to improve the agent's performance and enrich the knowledge base over time.

### Low-Level Component Breakdown

The system is composed of several key modules, each with a specific role.

#### 1. Frontend (`frontend/`)
- **Technology**: React.js
- **Role**: Provides the user interface for interacting with the math tutor. Users can submit questions, view solutions with detailed processing steps, and provide feedback (ratings). It communicates with the backend via RESTful API calls.

#### 2. Backend (`backend/main.py`)
- **Technology**: FastAPI
- **Role**: Acts as the central API gateway. It exposes endpoints for solving problems (`/solve`), submitting feedback (`/feedback`), and monitoring system status. It receives requests from the frontend and orchestrates the problem-solving process by invoking the LangGraph agent.

#### 3. Math Agent (`backend/math_agent.py`)
- **Technology**: LangGraph
- **Role**: The core of the system's intelligence. It's implemented as a stateful graph where each node represents a step in the problem-solving workflow (e.g., `input_guardrails`, `routing`, `knowledge_base_search`, `response_generation`). It manages the flow of data and logic, making decisions on how to best handle a given question.

#### 4. Vector Database (`backend/vector_database.py`)
- **Technology**: MongoDB Atlas Vector Search
- **Role**: Serves as the system's long-term memory or Knowledge Base. It stores mathematical problems and their solutions, along with their vector embeddings (generated using `sentence-transformers`). It enables efficient and scalable similarity searches to find relevant examples for new problems.

#### 5. MCP Server (`mcp_server/math_search_mcp.py`)
- **Technology**: Custom server implementing the Model-Context-Protocol (MCP).
- **Role**: A mandatory component that acts as a standardized bridge to external tools. It integrates with the Tavily search API to provide the agent with powerful, math-focused web search capabilities. This allows the agent to find information beyond its internal knowledge base.

#### 6. Feedback & Optimization System (`backend/dspy_feedback.py`)
- **Technology**: DSPy
- **Role**: Implements the Human-in-the-Loop (HITL) learning mechanism. It collects and processes user feedback to continuously improve the system. High-quality solutions are used to fine-tune the AI models (defined by DSPy signatures like `MathTeacher`) and enrich the MongoDB knowledge base.

#### 7. Benchmarking System (`backend/jee_benchmark.py`)
- **Technology**: Python script for automated testing.
- **Role**: Provides an automated evaluation framework to measure the agent's performance against a standardized dataset of JEE (Joint Entrance Examination) math problems. It calculates key metrics like accuracy and processing time, ensuring the system's reliability and effectiveness.

## 📁 Project Structure

```
real_math_tutor/
├── backend/
│   ├── main.py                           # FastAPI application
│   ├── complete_fastapi.py               # FastAPI application entry point
│   ├── vector_database.py                # MongoDB Atlas Vector DB
│   ├── dspy_feedback.py                  # DSPy optimization system
│   ├── jee_benchmark.py                  # JEE evaluation system
│   ├── enterprise_integration_test.py    # Complete system test
│   ├── requirements.txt                  # Enterprise dependencies
│   └── .env.template                     # Configuration template
│   └── .env.template                     # Configuration template
├── mcp_server/
│   └── math_search_mcp.py                # MCP server (MANDATORY)
├── frontend/
│   ├── src/
│   │   ├── App.js                        # Main React application
│   │   ├── components/                   # UI components
│   │   └── App.css                       # Enterprise styling
│   └── package.json                      # Frontend dependencies
└── deploy.py                             # One-click deployment
```

## 🚀 Quick Start (One-Click Deployment)

### 1. **Prerequisites**
- Python 3.8+
- Node.js 16+ (for frontend)
- MongoDB Atlas account
- API keys (OpenAI, Tavily, LangSmith)

### 2. **Clone and Deploy**
```bash
# Clone the repository
git clone <repository-url>
cd real_math_tutor

# One-click deployment
python deploy.py
```

### 3. **Configure Environment**
Edit `backend/.env` with your credentials:
```env
# MongoDB Atlas (provided)
MONGODB_CONNECTION_STRING=mongodb+srv://2320030062_db_user:qxGKi6TvODwi1jHg@cluster0.a5v0jm4.mongodb.net/

### 4. **Start the System**
```bash
# Backend (in backend/ directory)
python start_backend.py

# Frontend (in frontend/ directory)
npm start
```

**Access the application at:** http://localhost:3000

## 🏗️ Enterprise Components

### 🧠 **LangGraph Agent (math_agent.py)**
- **Routing Pipeline**: Intelligent decision making between knowledge base and web search
- **Guardrails**: Input validation, content filtering, output safety checks
- **Workflow Nodes**: Modular processing with proper state management
- **Async Processing**: High-performance concurrent request handling

```python
# Example agent workflow:
User Question → Input Guardrails → Routing Decision → 
(Knowledge Base Search OR Web Search via MCP) → 
Response Generation → Output Guardrails → Human Feedback
```

### 📊 **MongoDB Atlas Vector Database (vector_database.py)**
- **Real Embeddings**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Search**: MongoDB aggregation pipeline with cosine similarity
- **Scalable Storage**: Cloud-hosted with automatic scaling
- **Bulk Operations**: Efficient batch processing for large datasets

### 🔌 **Model Context Protocol Server (mcp_server/math_search_mcp.py)**
- **MANDATORY Requirement**: Proper MCP implementation as required
- **Tavily Integration**: Professional web search with mathematical focus
- **Tool Registry**: web_search_math, verify_math_solution, get_math_examples
- **Agent Integration**: Seamless communication with LangGraph workflow

### 🧠 **DSPy Optimization (dspy_feedback.py)**
- **Human-in-the-Loop Learning**: Continuous improvement from user feedback
- **Feedback Processing**: Rating-based optimization triggers
- **Model Signatures**: MathTeacher and MathVerifier for quality assurance
- **Statistics Tracking**: Performance metrics and optimization readiness

### 📈 **JEE Benchmarking (jee_benchmark.py)**
- **Automated Evaluation**: Test against JEE entrance exam problems
- **Performance Metrics**: Accuracy, similarity scores, processing times
- **Comparative Analysis**: LangGraph vs DSPy performance comparison
- **Topic-wise Breakdown**: Analysis by mathematical topics and difficulty

## 🔧 Advanced Configuration

### **Environment Variables**
```env
# Database Configuration
MONGODB_CONNECTION_STRING=mongodb+srv://...
MONGODB_DATABASE_NAME=math_tutor_enterprise
MONGODB_COLLECTION_NAME=math_problems

# AI Models
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Web Search
TAVILY_API_KEY=tvly-...

# Observability
LANGSMITH_API_KEY=ls__...
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=math-tutor-enterprise

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

### **Vector Database Configuration**
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Dimensions**: 384
- **Similarity Metric**: Cosine similarity
- **Index Type**: MongoDB Atlas Vector Search

### **Agent Configuration**
- **Routing Threshold**: 0.7 (knowledge base vs web search decision)
- **Max Knowledge Results**: 5
- **Confidence Threshold**: 0.8
- **Processing Timeout**: 30 seconds

## 🗂️ Complete Source Code Documentation

### Architecture Overview
- **Entry Point**: `deploy.py` (one-click deployment script)
- **Backend (`backend/`)**
  - `complete_fastapi.py`: CORS setup, API endpoints, middleware configuration
  - `math_agent.py`: LangGraph agent graph definition and orchestration
  - `vector_database.py`: MongoDB Atlas client integration and vector similarity search
  - `dspy_feedback.py`: DSPy human-in-the-loop feedback processing and optimization
  - `jee_benchmark.py`: Automated benchmarking against JEE problem set
  - `enterprise_integration_test.py`: End-to-end integration tests for the full system
  - `requirements.txt`: Python dependency specifications
  - `.env.template`: Environment variable placeholders and configuration schema
- **MCP Server (`mcp_server/`)**
  - `math_search_mcp.py`: Model-Context-Protocol handler and external web search integration
- **Frontend (`frontend/`)**
  - `src/App.js`: React application root and routing logic
  - `src/components/`: UI components (MathQuestion, FeedbackPanel, ResponseDisplay, etc.)
  - `public/`: Static assets, HTML template, and manifest
  - `package.json`: Frontend dependencies and build scripts
- **Configuration & Deployment**
  - `README.md`: Project documentation and setup instructions
  - `deploy.py`: Orchestrates environment setup, service startup, and deployment steps

### Component Interactions
1. **User → Frontend**: Submits math question via React UI
2. **Frontend → Backend**: HTTP POST to `/solve` handled by `complete_fastapi.py`
3. **Backend → Agent**: Invokes LangGraph agent in `math_agent.py`
4. **Agent Workflow**:
   - **Input Guardrails**: Validate and sanitize the user question
   - **Routing Decision**:
     - **Knowledge Base**: Query MongoDB Atlas via `vector_database.py`
     - **Web Search**: Call MCP server (`math_search_mcp.py`) for external information
   - **Response Generation**: Use LLM (OpenAI/Gemini) to create step-by-step solution
   - **Output Guardrails**: Verify formatting, correctness, and safety
5. **Response → Frontend → User**: Return `AnswerResponse` with solution and metadata
6. **Feedback Loop**:
   - User submits rating via POST `/feedback`
   - `dspy_feedback.py` processes feedback, updates knowledge base, and may trigger model optimization

### Observability & Testing
- **Logging**: Python `logging` for structured logs
- **Tracing**: Optional LangSmith integration (`LANGSMITH_TRACING`)
- **Integration Tests**: Run `enterprise_integration_test.py` for end-to-end validation

## 🌐 GitHub Pages Deployment
- The frontend is published via GitHub Pages on the `main` branch, using the repository root as the source.
- You can access the live site at: https://srinikhil2005.github.io/Math_Tutor/
