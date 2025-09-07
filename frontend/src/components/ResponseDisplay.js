import React from 'react';
import Typewriter from './Typewriter';

const ResponseDisplay = ({ response, onShowFeedback }) => {
  // Safety check - ensure response exists
  if (!response) {
    return (
      <div className="solution-container error">
        <div className="error-content">
          <h2>⚠️ No Response Available</h2>
          <p>Unable to display solution. Please try again.</p>
        </div>
      </div>
    );
  }

  // Extract the main solution content
  const solutionText = response.structured_solution || 
                      response.solution || 
                      response.final_answer || 
                      response.answer || 
                      response.explanation || 
                      "Solution not available";

  return (
    <div className="solution-container fade-in">
      <div className="solution-header">
        <h2>✨ Solution</h2>
        {response.confidence && (
          <div className="confidence-indicator">
            {(response.confidence * 100).toFixed(0)}%
          </div>
        )}
      </div>

      <div className="solution-content">
        <div className="solution-text">
          <Typewriter text={solutionText} speed={30} />
        </div>

        {/* Display steps if available */}
        {response.steps && Array.isArray(response.steps) && response.steps.length > 0 && (
          <div className="solution-steps">
            <h3>Steps:</h3>
            {response.steps.map((step, index) => (
              <div key={index} className="step-item">
                <span className="step-number">{index + 1}</span>
                <span className="step-text">{step}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Feedback Section */}
      <div className="solution-footer">
        <button 
          className="feedback-btn"
          onClick={onShowFeedback}
          type="button"
        >
          💭 Share Feedback
        </button>
      </div>
    </div>
  );
};

export default ResponseDisplay;
