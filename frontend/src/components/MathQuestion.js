import React from 'react';

const MathQuestion = ({ 
  question, 
  onQuestionChange, 
  onSubmit, 
  onSolve,  // Add support for both prop names
  isLoading, 
  loading,  // Add support for both prop names
  placeholder = "Enter your math question here..."
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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="math-question-container">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800 mb-2">Ask Your Math Question</h2>
        <p className="text-gray-600 text-sm">
          Type your mathematical problem below. You can use LaTeX notation like $x^2 + 3x - 4 = 0$ for equations.
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <textarea
            value={typeof question === 'string' ? question : String(question || '')}
            onChange={handleQuestionChange}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            disabled={isActuallyLoading}
            className={`w-full px-4 py-3 border-2 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 
                       resize-none transition-all duration-200 min-h-[120px] ${
                         isActuallyLoading 
                           ? 'bg-gray-50 border-gray-300 text-gray-500 cursor-not-allowed' 
                           : 'bg-white border-gray-300 text-gray-900 hover:border-gray-400'
                       }`}
            rows={4}
          />
          
          <div className="absolute bottom-3 right-3 flex items-center space-x-2">
            <span className="text-xs text-gray-400">
              Press Ctrl+Enter to submit
            </span>
          </div>
        </div>
        
        <div className="flex justify-between items-center">
          <div className="flex space-x-2">
            <button
              type="button"
              onClick={() => onQuestionChange('Solve: 2x + 5 = 13')}
              className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
              disabled={isActuallyLoading}
            >
              Example 1
            </button>
            <button
              type="button"
              onClick={() => onQuestionChange('Find the derivative of f(x) = x³ + 2x² - 5x + 1')}
              className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
              disabled={isActuallyLoading}
            >
              Example 2
            </button>
            <button
              type="button"
              onClick={() => onQuestionChange('Factor: x² - 9x + 20')}
              className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
              disabled={isActuallyLoading}
            >
              Example 3
            </button>
          </div>
          
          <button
            type="submit"
            disabled={!String(question || '').trim() || isActuallyLoading}
            className={`px-6 py-2 rounded-lg font-medium transition-all duration-200 ${
              String(question || '').trim() && !isActuallyLoading
                ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-md hover:shadow-lg transform hover:-translate-y-0.5'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            {isActuallyLoading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                <span>Solving...</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                <span>Solve Problem</span>
              </div>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default MathQuestion;
