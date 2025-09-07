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

  return (
    <div className="feedback-overlay">
      <div className="feedback-container">
        <div className="feedback-header">
          <h3>🧠 Help Improve AI Learning</h3>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="feedback-content">
          <form onSubmit={handleSubmit}>
            <div className="rating-section">
              <label>Rate this solution (1-5 stars):</label>
              <div className="star-rating">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    className={`star ${rating >= star ? 'active' : ''}`}
                    onClick={() => setRating(star)}
                    disabled={submitting}
                  >
                    ⭐
                  </button>
                ))}
              </div>
              {rating > 0 && (
                <div className="rating-text">
                  {rating === 1 && "❌ Poor solution"}
                  {rating === 2 && "⚠️ Needs improvement"}
                  {rating === 3 && "🔄 Average solution"}
                  {rating === 4 && "✅ Good solution"}
                  {rating === 5 && "🌟 Excellent solution"}
                </div>
              )}
            </div>

            <div className="feedback-section">
              <label htmlFor="feedback-text">
                What was good or bad about this solution?
              </label>
              <textarea
                id="feedback-text"
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Your feedback helps the AI learn and improve..."
                rows="3"
                required
              />
            </div>

            {rating <= 3 && rating > 0 && (
              <div className="correction-section">
                <label htmlFor="corrected-answer">
                  Provide the correct solution (optional):
                </label>
                <textarea
                  id="corrected-answer"
                  value={correctedAnswer}
                  onChange={(e) => setCorrectedAnswer(e.target.value)}
                  placeholder="What should the correct answer be?"
                  rows="3"
                />
              </div>
            )}

            <div className="feedback-actions">
              <button 
                type="button" 
                onClick={onClose}
                className="skip-btn"
              >
                Skip
              </button>
              <button 
                type="submit" 
                className="submit-feedback-btn"
                disabled={submitting || rating === 0}
              >
                {submitting ? 'Submitting...' : 'Submit Feedback'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default FeedbackPanel;
