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
    try {
      const statusResponse = await axios.get(`${API_BASE_URL}/status`);
      setSystemStatus(statusResponse.data);
    } catch (err) {
      console.error('Failed to fetch system status:', err);
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
      setError(
        err.response?.data?.detail || 
        'Failed to solve the mathematical problem. Please try again.'
      );
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
      <Header sidebarOpen={sidebarOpen} toggleSidebar={() => setSidebarOpen(!sidebarOpen)} />
      
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
