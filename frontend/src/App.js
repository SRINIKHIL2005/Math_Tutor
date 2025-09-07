import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Components
import Header from './components/Header';
import MathQuestion from './components/MathQuestion';
import ResponseDisplay from './components/ResponseDisplay';
import FeedbackPanel from './components/FeedbackPanel';
import SystemStatus from './components/SystemStatus';
import LoadingSpinner from './components/LoadingSpinner';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// Demo mode for GitHub Pages (when backend is not available)
const DEMO_MODE = process.env.NODE_ENV === 'production' && !process.env.REACT_APP_API_URL;

// Demo responses for different question types
const getDemoResponse = (question) => {
  const lowerQ = question.toLowerCase();
  
  if (lowerQ.includes('2+2') || lowerQ.includes('2 + 2')) {
    return {
      question: question,
      answer: "**Step-by-step solution:**\n\n1. We need to add 2 and 2\n2. 2 + 2 = 4\n\n**Final Answer:** 4\n\nThis is a basic addition problem. When we combine 2 units with another 2 units, we get a total of 4 units.",
      confidence: 0.95,
      route_taken: "demo_mode",
      component_used: "Demo Math Solver",
      timestamp: new Date().toISOString()
    };
  }
  
  if (lowerQ.includes('derivative') || lowerQ.includes('differentiate')) {
    return {
      question: question,
      answer: "**Calculus Problem - Derivative:**\n\n*This is a demo response showing the type of mathematical solutions our system provides.*\n\nFor derivative problems, our system would:\n1. Parse the mathematical expression\n2. Apply differentiation rules\n3. Simplify the result\n4. Provide step-by-step explanation\n\n**Note:** Connect to the full backend system for complete calculus solutions.",
      confidence: 0.85,
      route_taken: "demo_mode", 
      component_used: "Demo Math Solver",
      timestamp: new Date().toISOString()
    };
  }
  
  if (lowerQ.includes('quadratic') || lowerQ.includes('x^2')) {
    return {
      question: question,
      answer: "**Quadratic Equation Demo:**\n\nFor quadratic equations like ax² + bx + c = 0, our system uses:\n\n1. **Quadratic Formula:** x = (-b ± √(b²-4ac)) / 2a\n2. **Factoring methods** when applicable\n3. **Graphical analysis** for visual learners\n\n*This is a demo response. The full system provides complete step-by-step solutions with multiple approaches.*",
      confidence: 0.88,
      route_taken: "demo_mode",
      component_used: "Demo Math Solver", 
      timestamp: new Date().toISOString()
    };
  }
  
  return {
    question: question,
    answer: `**Demo Mode Response:**\n\nYou asked: "${question}"\n\n*This is a demonstration of our Math Tutor system deployed on GitHub Pages.*\n\n**Our Full System Includes:**\n- 🧠 Advanced RAG with MongoDB Atlas vector search\n- 🔍 Web search integration via MCP protocol\n- 🤖 Google Gemini AI for complex problem solving\n- 📚 Human-in-the-loop learning system\n- ⚡ Real-time mathematical reasoning\n\n**To experience the full system:** Run the backend server locally and connect to localhost:8001\n\n**Available Routes:**\n1. MongoDB Atlas Knowledge Base\n2. Web Search + MCP Integration  \n3. Google Gemini API Fallback`,
    confidence: 0.75,
    route_taken: "demo_mode",
    component_used: "GitHub Pages Demo",
    timestamp: new Date().toISOString()
  };
};

// Generate session ID
const generateSessionId = () => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

function App() {
  // State management
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(generateSessionId());
  const [systemStatus, setSystemStatus] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [settings, setSettings] = useState({
    useDspy: false,
    includeVerification: true
  });

  // Fetch system status on component mount
  useEffect(() => {
    fetchSystemStatus();
  }, []);

  const fetchSystemStatus = async () => {
    if (DEMO_MODE) {
      // Demo system status for GitHub Pages
      setSystemStatus({
        status: "Demo Mode",
        components: {
          "Demo Math Solver": "✅ ACTIVE",
          "GitHub Pages": "✅ DEPLOYED", 
          "Frontend": "✅ WORKING",
          "Backend": "⚠️ DEMO MODE - Connect locally for full features"
        },
        timestamp: new Date().toISOString(),
        demo_mode: true
      });
      return;
    }
    
    try {
      const statusResponse = await axios.get(`${API_BASE_URL}/status`);
      setSystemStatus(statusResponse.data);
    } catch (err) {
      console.error('Failed to fetch system status:', err);
      // Fallback to demo mode if backend is not available
      setSystemStatus({
        status: "Backend Unavailable",
        components: {
          "Demo Math Solver": "✅ ACTIVE",
          "Backend Connection": "❌ FAILED - Using demo mode"
        },
        timestamp: new Date().toISOString(),
        demo_mode: true
      });
    }
  };

  const handleSolveQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a mathematical question');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);
    setShowFeedback(false);

    // Demo mode handling
    if (DEMO_MODE) {
      // Simulate loading delay for realistic feel
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
      
      const demoResponse = getDemoResponse(question);
      setResponse(demoResponse);
      setLoading(false);
      return;
    }

    try {
      const solveResponse = await axios.post(`${API_BASE_URL}/solve`, {
        question: question,
        session_id: sessionId,
        use_dspy: settings.useDspy,
        include_verification: settings.includeVerification
      });

      setResponse(solveResponse.data);
      
      // Don't automatically show feedback - user will click button when ready
      // setTimeout(() => {
      //   setShowFeedback(true);
      // }, 1000);

    } catch (err) {
      console.error('Solve request failed:', err);
      
      // Fallback to demo mode if backend fails
      console.log('Falling back to demo mode...');
      const demoResponse = getDemoResponse(question);
      setResponse({
        ...demoResponse,
        answer: `**Backend Connection Failed - Demo Response:**\n\n${demoResponse.answer}\n\n⚠️ *Note: This is a demo response because the backend server is not accessible.*`,
        route_taken: "demo_fallback"
      });
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedbackData) => {
    if (!response) return;

    try {
      await axios.post(`${API_BASE_URL}/feedback`, {
        question: response.question,
        generated_answer: response.answer,
        human_rating: feedbackData.rating,
        human_feedback: feedbackData.feedback,
        corrected_answer: feedbackData.correctedAnswer,
        session_id: sessionId
      });

      setShowFeedback(false);
      
      // Show success message briefly
      // setTimeout(() => alert('Feedback submitted successfully!'), 100);

    } catch (err) {
      console.error('Failed to submit feedback:', err);
      setError('Failed to submit feedback. Please try again.');
    }
  };

  const handleNewSession = () => {
    setSessionId(generateSessionId());
    setQuestion('');
    setResponse(null);
    setError(null);
    setShowFeedback(false);
  };

  const handleOptimizeModel = async () => {
    try {
      const optimizeResponse = await axios.post(`${API_BASE_URL}/optimize-model`);
      alert(`Model optimization started: ${optimizeResponse.data.message}`);
      
      // Refresh status after optimization
      setTimeout(fetchSystemStatus, 1000);
      
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to start model optimization';
      alert(`Optimization failed: ${errorMsg}`);
    }
  };

  return (
    <div className="App">
      <Header 
        isDemo={DEMO_MODE || (systemStatus && systemStatus.demo_mode)}
        sidebarOpen={sidebarOpen} 
        toggleSidebar={() => setSidebarOpen(!sidebarOpen)} 
      />
      
      <div className="app-container">
        {/* Sidebar */}
        <div className={`sidebar ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
          <div className="sidebar-header">
            <h2>Dashboard</h2>
            <button onClick={() => setSidebarOpen(false)} className="close-sidebar-btn">
              &times;
            </button>
          </div>
          
          {/* System Status */}
          <SystemStatus 
            status={systemStatus} 
            onRefresh={fetchSystemStatus}
            onOptimizeModel={handleOptimizeModel}
          />

          {/* Settings Panel */}
          <div className="settings-panel">
            <h3>🔧 Settings</h3>
            <div className="settings-grid">
              <label className="setting-item">
                <input
                  type="checkbox"
                  checked={settings.useDspy}
                  onChange={(e) => setSettings(prev => ({...prev, useDspy: e.target.checked}))}
                />
                <span>Use DSPy Optimization 🧠</span>
              </label>
              <label className="setting-item">
                <input
                  type="checkbox"
                  checked={settings.includeVerification}
                  onChange={(e) => setSettings(prev => ({...prev, includeVerification: e.target.checked}))}
                />
                <span>Include Verification ✅</span>
              </label>
            </div>
            <button onClick={handleNewSession} className="new-session-btn">
              🆕 New Session
            </button>
          </div>
        </div>
        
        <main className={`main-container ${sidebarOpen ? 'main-shifted' : ''}`}>
          {/* Main Input Area */}
          <MathQuestion
            question={question}
            onQuestionChange={setQuestion}
            onSolve={handleSolveQuestion}
            loading={loading}
            placeholder="Enter your mathematical question (e.g., 'Solve the quadratic equation x² + 5x + 6 = 0')"
          />

        {/* Error Display */}
        {error && (
          <div className="error-container">
            <div className="error-message">
              ⚠️ {error}
            </div>
          </div>
        )}

        {/* Loading Spinner */}
        {loading && <LoadingSpinner message="🤖 Processing with AI pipeline..." />}

        {/* Response Display */}
        {response && (
          <ResponseDisplay 
            response={response}
            onShowSimilar={() => {}}
            onShowFeedback={() => setShowFeedback(true)}
          />
        )}

        {/* Feedback Panel */}
        {showFeedback && response && (
          <FeedbackPanel
            question={response.question}
            answer={response.answer}
            onSubmitFeedback={handleFeedback}
            onClose={() => setShowFeedback(false)}
          />
        )}
      </main>
    </div>
  </div>
  );
}

export default App;
