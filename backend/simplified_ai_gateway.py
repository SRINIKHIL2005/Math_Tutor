"""
SIMPLIFIED AI GATEWAY - TEMPORARY WORKAROUND
==========================================
This is a simplified version without guardrails dependency
We'll add proper guardrails back once the dependency issue is resolved
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)

class GuardrailResult(Enum):
    APPROVED = "approved"
    BLOCKED = "blocked"
    FLAGGED = "flagged"

class SimplifiedAIGateway:
    """
    Simplified AI Gateway without guardrails dependency
    This is a temporary workaround - we'll add proper guardrails back
    """
    
    def __init__(self):
        """Initialize the simplified AI gateway"""
        self.blocked_patterns = [
            r'\b(hack|exploit|cheat|illegal)\b',
            r'\b(violent|harmful|dangerous)\b',
            r'\b(inappropriate|offensive)\b'
        ]
        logger.info("Simplified AI Gateway initialized (temporary)")
    
    def validate_input(self, text: str) -> Tuple[GuardrailResult, str]:
        """
        Basic input validation without full guardrails
        """
        try:
            # Basic length check
            if len(text.strip()) == 0:
                return GuardrailResult.BLOCKED, "Empty input not allowed"
            
            if len(text) > 10000:
                return GuardrailResult.BLOCKED, "Input too long (max 10,000 characters)"
            
            # Basic pattern matching for inappropriate content
            text_lower = text.lower()
            for pattern in self.blocked_patterns:
                if re.search(pattern, text_lower):
                    return GuardrailResult.BLOCKED, f"Content flagged by pattern: {pattern}"
            
            # For math problems, check if it seems educational
            math_indicators = ['solve', 'calculate', 'find', 'equation', 'derivative', 'integral', 'factor', 'simplify']
            has_math_content = any(indicator in text_lower for indicator in math_indicators)
            
            if has_math_content or any(char in text for char in '=+-*/()[]{}^'):
                return GuardrailResult.APPROVED, "Mathematical content detected"
            
            return GuardrailResult.APPROVED, "Input appears valid"
            
        except Exception as e:
            logger.error(f"Error in input validation: {e}")
            return GuardrailResult.BLOCKED, f"Validation error: {str(e)}"
    
    def validate_output(self, text: str) -> Tuple[GuardrailResult, str]:
        """
        Basic output validation without full guardrails
        """
        try:
            # Basic checks for output
            if len(text.strip()) == 0:
                return GuardrailResult.BLOCKED, "Empty output"
            
            # Check for basic educational structure
            educational_indicators = ['step', 'solution', 'answer', 'therefore', 'because', 'explanation']
            has_educational_content = any(indicator in text.lower() for indicator in educational_indicators)
            
            if has_educational_content:
                return GuardrailResult.APPROVED, "Educational content detected"
            
            return GuardrailResult.APPROVED, "Output appears valid"
            
        except Exception as e:
            logger.error(f"Error in output validation: {e}")
            return GuardrailResult.BLOCKED, f"Validation error: {str(e)}"

def get_ai_gateway():
    """Get the AI gateway instance"""
    return SimplifiedAIGateway()

# For backward compatibility
def create_math_guardrails():
    """Create math-specific guardrails (simplified version)"""
    return SimplifiedAIGateway()
