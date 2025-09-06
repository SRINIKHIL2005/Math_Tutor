import React from 'react';

const LoadingSpinner = ({ message = "Loading...", size = "medium" }) => {
  const sizeClasses = {
    small: "w-4 h-4",
    medium: "w-8 h-8", 
    large: "w-12 h-12"
  };

  const containerClasses = {
    small: "p-2",
    medium: "p-4",
    large: "p-6"
  };

  return (
    <div className={`flex flex-col items-center justify-center ${containerClasses[size]}`}>
      <div className={`animate-spin rounded-full border-4 border-gray-200 border-t-blue-600 ${sizeClasses[size]}`}></div>
      {message && (
        <p className="mt-2 text-gray-600 text-sm font-medium">{message}</p>
      )}
    </div>
  );
};

// Alternative spinner styles
export const PulseLoader = ({ message = "Processing...", color = "blue" }) => {
  const colorClasses = {
    blue: "bg-blue-500",
    green: "bg-green-500",
    purple: "bg-purple-500",
    red: "bg-red-500"
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="flex space-x-1">
        <div className={`w-2 h-2 ${colorClasses[color]} rounded-full animate-pulse`} style={{animationDelay: '0ms'}}></div>
        <div className={`w-2 h-2 ${colorClasses[color]} rounded-full animate-pulse`} style={{animationDelay: '150ms'}}></div>
        <div className={`w-2 h-2 ${colorClasses[color]} rounded-full animate-pulse`} style={{animationDelay: '300ms'}}></div>
      </div>
      {message && (
        <p className="mt-2 text-gray-600 text-sm">{message}</p>
      )}
    </div>
  );
};

// Math-specific loading animation
export const MathLoader = ({ message = "Solving mathematical problem..." }) => {
  return (
    <div className="flex flex-col items-center justify-center p-6">
      <div className="relative">
        <div className="w-16 h-16 border-4 border-blue-200 rounded-full"></div>
        <div className="absolute top-0 left-0 w-16 h-16 border-4 border-blue-600 rounded-full animate-spin border-t-transparent"></div>
        
        {/* Math symbols floating around */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-blue-600 font-bold text-lg animate-pulse">∑</div>
        </div>
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-gray-700 font-medium">{message}</p>
        <div className="flex justify-center mt-2 space-x-1">
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '100ms'}}></div>
          <div className="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '200ms'}}></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingSpinner;
