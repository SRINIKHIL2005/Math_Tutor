import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Real Math Tutor</h1>
          <p>AI-Powered Mathematics Learning Platform</p>
        </div>
        
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '20px',
          fontSize: '0.9rem'
        }}>
          <div style={{
            background: 'rgba(255, 255, 255, 0.2)',
            padding: '8px 16px',
            borderRadius: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              backgroundColor: '#10b981',
              borderRadius: '50%'
            }}></div>
            <span>AI Agent Active</span>
          </div>
          
          <div style={{ textAlign: 'right', opacity: 0.8 }}>
            <div style={{ fontSize: '0.8rem' }}>Powered by</div>
            <div style={{ fontWeight: '600' }}>LangGraph + MongoDB Atlas</div>
            <div style={{ fontSize: '0.8rem' }}>Vector Search • Agentic AI • 12K+ Problems • Real-time Learning</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
