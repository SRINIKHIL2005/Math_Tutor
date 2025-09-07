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
          gap: '25px',
          fontSize: '0.95rem'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.3) 100%)',
            padding: '10px 18px',
            borderRadius: '25px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 4px 15px rgba(16, 185, 129, 0.1)'
          }}>
            <div style={{
              width: '10px',
              height: '10px',
              backgroundColor: '#10b981',
              borderRadius: '50%',
              animation: 'pulse 2s infinite',
              boxShadow: '0 0 10px rgba(16, 185, 129, 0.5)'
            }}></div>
            <span style={{ fontWeight: '600' }}>AI Agent Active</span>
          </div>
          
          <div style={{ textAlign: 'right', opacity: 0.9 }}>
            <div style={{ fontSize: '0.8rem', opacity: 0.8, marginBottom: '2px' }}>Powered by</div>
            <div style={{ fontWeight: '700', fontSize: '1rem', marginBottom: '4px' }}>LangGraph + MongoDB Atlas</div>
            <div style={{ 
              fontSize: '0.75rem', 
              opacity: 0.8,
              background: 'rgba(255, 255, 255, 0.1)',
              padding: '4px 8px',
              borderRadius: '12px',
              backdropFilter: 'blur(5px)'
            }}>
              Vector Search • Agentic AI • 12K+ Problems • Real-time Learning
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
