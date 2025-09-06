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
        className={`star-btn ${rating >= star ? 'active' : ''}`}
        onClick={() => setRating(star)}
        disabled={submitting}
      >
        ⭐
      </button>
    ));
  };

  return (
    <div className="feedback-overlay">
      <div className="feedback-panel">
        <div className="feedback-header">
          <h3>👤 Human Feedback for Learning</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="feedback-description">
          

        <form onSubmit={handleSubmit} className="feedback-form">
          <div className="rating-section">
            <label>Rate the solution quality (1-5 stars):</label>
            <div className="stars-container">
              {renderStars()}
            </div>
            <div className="rating-description">
              {rating === 1 && "❌ Completely wrong"}
              {rating === 2 && "⚠️ Mostly incorrect with major errors"}
              {rating === 3 && "🔄 Partially correct but needs improvement"}
              {rating === 4 && "✅ Good solution with minor issues"}
              {rating === 5 && "🌟 Excellent, perfect solution"}
            </div>
          </div>

          <div className="feedback-section">
            <label htmlFor="feedback-text">
              Detailed feedback (what was good/bad?):
            </label>
            <textarea
              id="feedback-text"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Explain what was correct or incorrect about the solution. This helps the AI learn..."
              rows="4"
              required
              disabled={submitting}
            />
          </div>

          {rating <= 3 && (
            <div className="correction-section">
              <label htmlFor="corrected-answer">
                Provide the correct solution (optional but helps training):
              </label>
              <textarea
                id="corrected-answer"
                value={correctedAnswer}
                onChange={(e) => setCorrectedAnswer(e.target.value)}
                placeholder="What should the correct answer be? Include your working if possible..."
                rows="4"
                disabled={submitting}
              />
            </div>
          )}

          <div className="feedback-benefits">
            <h4>🎯 How your feedback helps:</h4>
            <ul>
              <li>⚡ <strong>Immediate:</strong> High-rated solutions added to knowledge base</li>
              <li>🧠 <strong>Learning:</strong> DSPy optimization uses your corrections</li>
              <li>📊 <strong>Analytics:</strong> Patterns help improve routing decisions</li>
              <li>🔄 <strong>Future:</strong> Model becomes more accurate over time</li>
            </ul>
          </div>

          <div className="feedback-actions">
            <button 
              type="button" 
              onClick={onClose}
              className="cancel-btn"
              disabled={submitting}
            >
              Skip Feedback
            </button>
            <button 
              type="submit" 
              className="submit-btn"
              disabled={submitting || rating === 0}
            >
              {submitting ? '⏳ Submitting...' : '🚀 Submit Feedback'}
            </button>
          </div>
        </form>
        </div>

        <div className="feedback-footer">
          <small>
            💡 Your feedback is anonymous and used solely for improving the AI tutoring system.
          </small>
        </div>
      </div>
    </div>
  );
};

export default FeedbackPanel;
