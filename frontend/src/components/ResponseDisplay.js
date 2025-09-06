import React from 'react';
import ReactMarkdown from 'react-markdown';
import Typewriter from './Typewriter';

const ResponseDisplay = ({ response, onShowFeedback }) => {
  // Safety check - ensure response exists
  if (!response) {
    return (
      <div className="response-container error">
        <h2>⚠️ No Response</h2>
        <p>No response data available to display.</p>
      </div>
    );
  }

  const processingPathIcons = {
    'input_guardrails': '🛡️',
    'routing': '🧭', 
    'knowledge_base': '📚',
    'web_search': '🌐',
    'response_generation': '🤖',
    'output_guardrails': '✅',
    'dspy_optimization': '🧠'
  };

  const formatProcessingPath = (routeTaken) => {
    // Handle case where routeTaken is a string, not an array
    if (!routeTaken) return 'Unknown';
    
    // If it's already a string, just format it
    if (typeof routeTaken === 'string') {
      return `${processingPathIcons[routeTaken] || '⚡'} ${routeTaken.replace('_', ' ')}`;
    }
    
    // If it's an array, map through it
    if (Array.isArray(routeTaken)) {
      return routeTaken.map(step => `${processingPathIcons[step] || '⚡'} ${step.replace('_', ' ')}`).join(' → ');
    }
    
    return 'Unknown';
  };

  return (
    <div className="response-container">
      <div className="response-header">
        <h2>🎯 Solution</h2>
        <div className="confidence-badge">
          Confidence: {((response.confidence || 0) * 100).toFixed(1)}%
        </div>
      </div>

      <div className="question-section">
        <h3>📝 Question:</h3>
        <div className="question-text">{response.question || 'Question not available'}</div>
      </div>

      <div className="answer-section">
        <h3>💡 Answer:</h3>
        <div className="answer-content">
          <Typewriter text={response.answer || 'Answer not available'} speed={30} />
        </div>
        
        {/* Add feedback button after answer */}
        <div className="answer-actions">
          <button 
            className="feedback-button"
            onClick={onShowFeedback}
            type="button"
          >
            📝 Give Feedback on this Answer
          </button>
        </div>
      </div>

      {/* Only show verification if it exists */}
      {response.verification_result && (
        <div className="verification-section">
          <h3>✅ Verification:</h3>
          <div className="verification-content">
              <Typewriter text={response.verification_result} speed={30} />
            </div>
        </div>
      )}

      <div className="processing-info">
        <h2>🔍 Processing Details</h2>
        <div className="processing-grid">
          <div className="processing-item">
            <strong>Route Taken:</strong>
            <div className="processing-path">
              {formatProcessingPath(response.route_taken)}
            </div>
          </div>
          
          <div className="processing-item">
            <strong>Component Used:</strong>
            <div className="component-used">
              {response.component_used || 'Unknown'}
            </div>
          </div>
          
          <div className="processing-stats">
            <div className="stat-item">
              <span className="stat-icon">⏱️</span>
              <span>Processed at: {new Date(response.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="stat-item">
              <span className="stat-icon">�</span>
              <span>Confidence: {((response.confidence || 0) * 100).toFixed(1)}%</span>
            </div>
            {response.error && (
              <div className="stat-item error">
                <span className="stat-icon">⚠️</span>
                <span>Error: {response.error}</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Only show similar problems if they exist */}
      {response.similar_problems && Array.isArray(response.similar_problems) && response.similar_problems.length > 0 && (
        <div className="similar-problems-section">
          <h3>🔗 Similar Problems from Knowledge Base</h3>
          <div className="similar-problems-list">
            {response.similar_problems.map((problem, index) => (
              <div key={index} className="similar-problem">
                <div className="similarity-score">
                  {(problem.similarity * 100).toFixed(1)}% similar
                </div>
                <div className="problem-question">{problem.question}</div>
                {problem.topic && (
                  <div className="problem-topic">Topic: {problem.topic}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Only show metadata if it exists */}
      {response.metadata && (
        <div className="metadata-section">
          <details>
            <summary>🔧 Technical Metadata</summary>
            <pre className="metadata-content">
              {JSON.stringify(response.metadata, null, 2)}
            </pre>
          </details>
        </div>
      )}

      <div className="session-info">
        Session: {response.session_id} | {new Date(response.timestamp).toLocaleString()}
      </div>
    </div>
  );
};

export default ResponseDisplay;
