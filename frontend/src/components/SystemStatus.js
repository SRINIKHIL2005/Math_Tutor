import React from 'react';

const SystemStatus = ({ status, onRefresh, onOptimizeModel }) => {
  if (!status) {
    return (
      <div className="system-status">
        <h3>🔄 Loading System Status...</h3>
      </div>
    );
  }

  const getStatusIcon = (statusValue) => {
    switch (statusValue) {
      case 'healthy':
      case 'ready':
        return '✅';
      case 'error':
        return '❌';
      default:
        return '⚠️';
    }
  };

  const canOptimize = status.dspy_feedback_count >= 5;

  return (
    <div className="system-status">
      <div className="status-header">
        <h3>🏢 System Status</h3>
        <button onClick={onRefresh} className="refresh-btn" title="Refresh Status">
          🔄
        </button>
      </div>
      
      <div className="status-grid">
        <div className="status-item">
          <span className="status-icon">
            {getStatusIcon(status.vector_db_status)}
          </span>
          <div className="status-details">
            <div className="status-name">MongoDB Atlas Vector DB</div>
            <div className="status-value">
              {status.vector_db_problems_count} problems indexed
            </div>
          </div>
        </div>

        <div className="status-item">
          <span className="status-icon">
            {getStatusIcon(status.mcp_server_status)}
          </span>
          <div className="status-details">
            <div className="status-name">MCP Server</div>
            <div className="status-value">{status.mcp_server_status}</div>
          </div>
        </div>

        <div className="status-item">
          <span className="status-icon">
            {status.dspy_feedback_count > 0 ? '🧠' : '💭'}
          </span>
          <div className="status-details">
            <div className="status-name">DSPy Feedback System</div>
            <div className="status-value">
              {status.dspy_feedback_count} feedback entries
            </div>
          </div>
        </div>

        <div className="status-item">
          <span className="status-icon">
            {status.langsmith_tracing ? '📊' : '📋'}
          </span>
          <div className="status-details">
            <div className="status-name">LangSmith Tracing</div>
            <div className="status-value">
              {status.langsmith_tracing ? 'Enabled' : 'Disabled'}
            </div>
          </div>
        </div>
      </div>

      {canOptimize && (
        <div className="optimization-section">
          <button 
            onClick={onOptimizeModel}
            className="optimize-btn"
            title="Optimize DSPy model with collected feedback"
          >
            🚀 Optimize Model ({status.dspy_feedback_count} feedback)
          </button>
        </div>
      )}

      <div className="status-timestamp">
        Last updated: {new Date(status.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
};

export default SystemStatus;
