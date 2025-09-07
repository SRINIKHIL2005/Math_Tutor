import React, { useState } from 'react';

const FeedbackPanel = ({ question, answer, onSubmitFeedback, onClose }) => {
  const [rating, setRating] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [correctedAnswer, setCorrectedAnswer] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (rating === 0) {
      alert('Please provide a rating from 1 to 5 stars');
      return;
    }

    setSubmitting(true);
    
    try {
      await onSubmitFeedback({
        rating,
        feedback,
        correctedAnswer: correctedAnswer.trim() || null
      });
      
      // Reset form
      setRating(0);
      setFeedback('');
      setCorrectedAnswer('');
      
    } catch (error) {
      console.error('Failed to submit feedback:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const renderStars = () => {
    return [1, 2, 3, 4, 5].map((star) => (
      <button
        key={star}
        type="button"
        className={`feedback-star ${rating >= star ? 'active' : ''}`}
        onClick={() => setRating(star)}
        disabled={submitting}
      >
        <span className="star-icon">★</span>
      </button>
    ));
  };

  return (
    <div className="feedback-overlay">
      <div className="feedback-modal">
        <div className="feedback-header">
          <div className="feedback-title">
            <div className="feedback-icon">🧠</div>
            <h3>Human Feedback for Learning</h3>
          </div>
          <button className="feedback-close-btn" onClick={onClose}>
            <span>✕</span>
          </button>
        </div>

        <div className="feedback-content">
          <form onSubmit={handleSubmit} className="feedback-form">
            <div className="feedback-section">
              <label className="feedback-label">Rate the solution quality:</label>
              <div className="stars-container">
                {renderStars()}
              </div>
              <div className="rating-description">
                {rating === 1 && <span className="rating-text error">❌ Completely wrong</span>}
                {rating === 2 && <span className="rating-text warning">⚠️ Mostly incorrect with major errors</span>}
                {rating === 3 && <span className="rating-text neutral">🔄 Partially correct but needs improvement</span>}
                {rating === 4 && <span className="rating-text good">✅ Good solution with minor issues</span>}
                {rating === 5 && <span className="rating-text excellent">🌟 Excellent, perfect solution</span>}
              </div>
            </div>

            <div className="feedback-section">
              <label htmlFor="feedback-text" className="feedback-label">
                Detailed feedback (what was good/bad?):
              </label>
              <textarea
                id="feedback-text"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Explain what was correct or incorrect about the solution. This helps the AI learn..."
                className="feedback-textarea"
                rows="4"
                required
                disabled={submitting}
              />
            </div>

            {rating <= 3 && (
              <div className="feedback-section">
                <label htmlFor="corrected-answer" className="feedback-label">
                  Provide the correct solution (optional but helps training):
                </label>
                <textarea
                  id="corrected-answer"
                  value={correctedAnswer}
                  onChange={(e) => setCorrectedAnswer(e.target.value)}
                  placeholder="What should the correct answer be? Include your working if possible..."
                  className="feedback-textarea"
                  rows="4"
                  disabled={submitting}
                />
              </div>
            )}

            <div className="feedback-benefits">
              <h4 className="benefits-title">🎯 How your feedback helps:</h4>
              <div className="benefits-grid">
                <div className="benefit-item">
                  <span className="benefit-icon">⚡</span>
                  <div className="benefit-text">
                    <strong>Immediate:</strong> High-rated solutions added to knowledge base
                  </div>
                </div>
                <div className="benefit-item">
                  <span className="benefit-icon">🧠</span>
                  <div className="benefit-text">
                    <strong>Learning:</strong> DSPy optimization uses your corrections
                  </div>
                </div>
                <div className="benefit-item">
                  <span className="benefit-icon">📊</span>
                  <div className="benefit-text">
                    <strong>Analytics:</strong> Patterns help improve routing decisions
                  </div>
                </div>
                <div className="benefit-item">
                  <span className="benefit-icon">🔄</span>
                  <div className="benefit-text">
                    <strong>Future:</strong> Model becomes more accurate over time
                  </div>
                </div>
              </div>
            </div>

            <div className="feedback-actions">
              <button 
                type="button" 
                onClick={onClose}
                className="feedback-cancel-btn"
                disabled={submitting}
              >
                Skip Feedback
              </button>
              <button 
                type="submit" 
                className="feedback-submit-btn"
                disabled={submitting || rating === 0}
              >
                <span className="btn-content">
                  {submitting ? (
                    <>
                      <span className="loading-spinner"></span>
                      Submitting...
                    </>
                  ) : (
                    <>
                      <span className="btn-icon">🚀</span>
                      Submit Feedback
                    </>
                  )}
                </span>
              </button>
            </div>
          </form>
        </div>

        <div className="feedback-footer">
          <div className="footer-text">
            💡 Your feedback is anonymous and used solely for improving the AI tutoring system.
          </div>
        </div>
      </div>
    </div>
  );
};

export default FeedbackPanel;
