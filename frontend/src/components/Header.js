import React from 'react';

const Header = ({ isDemo = false }) => {
  return (
    <>
      {/* Demo Mode Banner */}
      {isDemo && (
        <div className="bg-yellow-500 text-black text-center py-2 px-4">
          <div className="flex items-center justify-center space-x-2">
            <span>🚀</span>
            <span className="font-semibold">DEMO MODE</span>
            <span>•</span>
            <span>GitHub Pages Deployment</span>
            <span>•</span>
            <span>Connect locally for full backend features</span>
          </div>
        </div>
      )}
      
      <header className="bg-gradient-to-r from-gray-800 to-gray-900 text-white shadow">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-white bg-opacity-20 rounded-lg p-3">
                <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold">Real Math Tutor</h1>
                <p className="text-gray-300 text-sm">
                  {isDemo ? 'AI-Powered Mathematics Learning Platform (Demo)' : 'AI-Powered Mathematics Learning Platform'}
                </p>
              </div>
            </div>
            
            <div className="hidden md:flex items-center space-x-6">
              <div className="bg-white bg-opacity-10 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full animate-pulse ${isDemo ? 'bg-yellow-400' : 'bg-green-400'}`}></div>
                  <span className="text-sm font-medium">
                    {isDemo ? 'Demo Mode Active' : 'AI Agent Active'}
                  </span>
                </div>
              </div>
              
              <div className="text-right">
                <div className="text-xs text-gray-400">Powered by</div>
                <div className="text-sm font-semibold">
                  {isDemo ? 'GitHub Pages Demo' : 'LangGraph + MongoDB Atlas'}
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-4 flex flex-wrap gap-2">
            <span className="bg-gray-100 bg-opacity-10 text-xs px-3 py-1 rounded-full">Vector Search</span>
            <span className="bg-gray-100 bg-opacity-10 text-xs px-3 py-1 rounded-full">Agentic AI</span>
            <span className="bg-gray-100 bg-opacity-10 text-xs px-3 py-1 rounded-full">12K+ Problems</span>
            <span className="bg-gray-100 bg-opacity-10 text-xs px-3 py-1 rounded-full">Real-time Learning</span>
          </div>
        </div>
      </header>
    </>
  );
};

export default Header;
