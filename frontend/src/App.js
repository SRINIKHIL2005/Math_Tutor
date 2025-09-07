import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Components
import Header from './components/Header';
import MathQuestion from './components/MathQuestion';
import ResponseDisplay from './components/ResponseDisplay';
import FeedbackPanel from './components/FeedbackPanel';
import LoadingSpinner from './components/LoadingSpinner';

// Smart API URL detection
const getApiUrl = () => {
  // Check environment variable first
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // If on GitHub Pages, use the live Render backend
  if (window.location.hostname === 'srinikhil2005.github.io') {
    return 'https://math-tutor-1.onrender.com'; // Live backend on Render
  }
  
  // Default to localhost for local development
  return 'http://localhost:8001';
};

const API_BASE_URL = getApiUrl();

// Generate session ID
const generateSessionId = () => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

function App() {
  // State management
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(generateSessionId());
  const [showFeedback, setShowFeedback] = useState(false);
  const [useVoice, setUseVoice] = useState(false); // New: Voice preference

  const handleSolveQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a mathematical question');
      return;
    }

    // If no backend URL available, show informative message
    if (!API_BASE_URL) {
      setError('Backend not available on GitHub Pages. Please run the application locally or deploy the backend to a cloud service to use the full math tutoring features.');
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
        use_voice: useVoice  // Include voice preference
      });

      setResponse(solveResponse.data);

    } catch (err) {
      console.error('Solve request failed:', err);
      setError(
        err.response?.data?.detail || 
        'Failed to solve the mathematical problem. Please check your backend connection and try again.'
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

    } catch (err) {
      console.error('Failed to submit feedback:', err);
      setError('Failed to submit feedback. Please try again.');
    }
  };

  return (
    <div className="App">
      <Header />
      
      <main className="main-container">
        {/* Main Input Area */}
        <MathQuestion
          question={question}
          onQuestionChange={setQuestion}
          onSolve={handleSolveQuestion}
          loading={loading}
          useVoice={useVoice}
          onVoiceToggle={setUseVoice}
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
  );
}

export default App;
