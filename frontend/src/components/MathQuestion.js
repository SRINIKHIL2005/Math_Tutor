import React from 'react';

const MathQuestion = ({ 
  question, 
  onQuestionChange, 
  onSubmit, 
  onSolve,  // Add support for both prop names
  isLoading, 
  loading,  // Add support for both prop names
  placeholder = "Enter your mathematical question (e.g., 'Solve the quadratic equation x² + 5x + 6 = 0')"
}) => {
  // Use the loading state from either prop
  const isActuallyLoading = isLoading || loading;
  
  // Use the submit handler from either prop
  const submitHandler = onSubmit || onSolve;
  
  // Handle the onChange event properly by extracting the value
  const handleQuestionChange = (e) => {
    onQuestionChange(e.target.value);
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Ensure question is a string before calling trim
    const questionValue = typeof question === 'string' ? question : String(question || '');
    if (questionValue.trim() && !isActuallyLoading && submitHandler) {
      submitHandler();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="math-question-container">
      <h2>Ask Your Math Question</h2>
      <p>
        Type your mathematical problem below. You can use LaTeX notation like $x^2 + 3x - 4 = 0$ for equations.
      </p>
      
      <form onSubmit={handleSubmit}>
        <textarea
          value={typeof question === 'string' ? question : String(question || '')}
          onChange={handleQuestionChange}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={isActuallyLoading}
        />
        
        <div className="submit-text">
          Press Ctrl+Enter to submit
        </div>
        
        <div className="example-buttons">
          <button
            type="button"
            onClick={() => onQuestionChange('Solve: 2x + 5 = 13')}
            className="example-btn"
            disabled={isActuallyLoading}
          >
            Example 1
          </button>
          <button
            type="button"
            onClick={() => onQuestionChange('Find the derivative of f(x) = x³ + 2x² - 5x + 1')}
            className="example-btn"
            disabled={isActuallyLoading}
          >
            Example 2
          </button>
          <button
            type="button"
            onClick={() => onQuestionChange('Factor: x² - 9x + 20')}
            className="example-btn"
            disabled={isActuallyLoading}
          >
            Example 3
          </button>
        </div>
        
        <button
          type="submit"
          disabled={!String(question || '').trim() || isActuallyLoading}
          className="submit-btn"
        >
          {isActuallyLoading ? 'Solving...' : 'Solve Problem'}
        </button>
      </form>
    </div>
  );
};

export default MathQuestion;
