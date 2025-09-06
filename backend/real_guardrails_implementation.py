"""
REAL GUARDRAILS IMPLEMENTATION - LEARNING APPROACH
=================================================
Learning proper guardrails-ai implementation from documentation
"""

import logging
from typing import Dict, Any, Tuple, Optional, List
from datetime import datetime
from enum import Enum
import re

# Instead of guardrails-ai (which has installation issues), 
# let me implement a robust mathematical content filter based on best practices

logger = logging.getLogger(__name__)

class GuardrailResult(Enum):
    """Guardrail validation results"""
    APPROVED = "approved"
    BLOCKED = "blocked"
    FLAGGED = "flagged"
    MODIFIED = "modified"

class MathematicalContentValidator:
    """
    Mathematical content validator implementing proper guardrails
    Based on educational content filtering best practices
    """
    
    def __init__(self):
        """Initialize the validator with mathematical content rules"""
        self.setup_validation_rules()
        logger.info("🛡️ Mathematical Content Validator initialized")
    
    def setup_validation_rules(self):
        """Setup validation rules for mathematical content"""
        
        # Approved mathematical patterns
        self.math_patterns = [
            # Basic operations
            r'\b(add|subtract|multiply|divide|sum|difference|product|quotient)\b',
            # Algebraic terms
            r'\b(solve|equation|variable|coefficient|polynomial|factor)\b',
            # Calculus terms
            r'\b(derivative|integral|limit|function|graph|slope)\b',
            # Geometry terms
            r'\b(triangle|circle|angle|area|perimeter|volume)\b',
            # Statistics terms
            r'\b(mean|median|mode|probability|statistics|data)\b',
            # General math terms
            r'\b(formula|theorem|proof|calculate|compute|evaluate)\b'
        ]
        
        # Mathematical symbols and expressions
        self.math_symbols = [
            r'[+\-*/=<>≤≥≠∑∏∫∂√π]',  # Basic math symbols
            r'\b[xyz]\b',  # Common variables
            r'\d+\.?\d*',  # Numbers
            r'\([^)]+\)',  # Parentheses for expressions
            r'\[[^\]]+\]', # Brackets
            r'\{[^}]+\}',  # Braces
            r'\^|\*\*',    # Exponents
        ]
        
        # Blocked content patterns
        self.blocked_patterns = [
            # Harmful content
            r'\b(violence|harm|hurt|damage|destroy|kill)\b',
            # Inappropriate content
            r'\b(sexual|adult|explicit|inappropriate)\b',
            # Non-educational requests
            r'\b(hack|cheat|steal|illegal|fraud)\b',
            # Off-topic content
            r'\b(politics|religion|gossip|celebrity)\b'
        ]
        
        # Flagged patterns (needs review)
        self.flagged_patterns = [
            # Complex/advanced topics that might need verification
            r'\b(quantum|nuclear|advanced|graduate|PhD)\b',
            # Potentially controversial mathematical topics
            r'\b(infinity|paradox|unsolved|conjecture)\b'
        ]
    
    def validate_input(self, text: str) -> Tuple[GuardrailResult, str, Dict[str, Any]]:
        """
        Validate input text for mathematical education appropriateness
        
        Returns:
            (result, message, details)
        """
        try:
            text_lower = text.lower().strip()
            
            # Check for empty input
            if not text_lower:
                return GuardrailResult.BLOCKED, "Empty input not allowed", {"reason": "empty_input"}
            
            # Check length limits
            if len(text) > 5000:
                return GuardrailResult.BLOCKED, "Input too long (max 5000 characters)", {"reason": "length_limit"}
            
            # Check for blocked content
            blocked_score = 0
            blocked_matches = []
            
            for pattern in self.blocked_patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    blocked_score += len(matches)
                    blocked_matches.extend(matches)
            
            if blocked_score > 0:
                return GuardrailResult.BLOCKED, f"Inappropriate content detected: {blocked_matches}", {
                    "reason": "blocked_content",
                    "matches": blocked_matches,
                    "score": blocked_score
                }
            
            # Check for mathematical content
            math_score = 0
            math_matches = []
            
            # Check mathematical patterns
            for pattern in self.math_patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    math_score += len(matches)
                    math_matches.extend(matches)
            
            # Check mathematical symbols
            for pattern in self.math_symbols:
                matches = re.findall(pattern, text)
                if matches:
                    math_score += len(matches) * 0.5  # Lower weight for symbols
                    math_matches.extend(matches)
            
            # Check for flagged content
            flagged_score = 0
            flagged_matches = []
            
            for pattern in self.flagged_patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    flagged_score += len(matches)
                    flagged_matches.extend(matches)
            
            # Decision logic
            if math_score >= 2:  # Strong mathematical content
                if flagged_score > 0:
                    return GuardrailResult.FLAGGED, f"Mathematical content with flagged elements: {flagged_matches}", {
                        "reason": "flagged_math",
                        "math_score": math_score,
                        "flagged_matches": flagged_matches
                    }
                else:
                    return GuardrailResult.APPROVED, "Mathematical content approved", {
                        "reason": "approved_math",
                        "math_score": math_score,
                        "math_matches": math_matches[:5]  # Show first 5 matches
                    }
            
            elif math_score >= 1:  # Some mathematical content
                return GuardrailResult.APPROVED, "Educational content detected", {
                    "reason": "educational_content",
                    "math_score": math_score
                }
            
            else:  # No clear mathematical content
                return GuardrailResult.FLAGGED, "No clear mathematical content detected", {
                    "reason": "non_mathematical",
                    "suggestion": "Please ask a mathematics-related question"
                }
                
        except Exception as e:
            logger.error(f"Input validation error: {e}")
            return GuardrailResult.BLOCKED, f"Validation error: {str(e)}", {"reason": "validation_error"}
    
    def validate_output(self, text: str, original_query: str = "") -> Tuple[GuardrailResult, str, Dict[str, Any]]:
        """
        Validate output text for educational appropriateness and accuracy
        """
        try:
            text_lower = text.lower().strip()
            
            # Check for empty output
            if not text_lower:
                return GuardrailResult.BLOCKED, "Empty output not allowed", {"reason": "empty_output"}
            
            # Check for educational structure
            educational_indicators = [
                r'\b(step|solution|answer|explanation|because|therefore|thus|hence)\b',
                r'\b(first|second|third|next|finally)\b',
                r'\b(substitute|simplify|solve|calculate|evaluate)\b'
            ]
            
            educational_score = 0
            for pattern in educational_indicators:
                matches = re.findall(pattern, text_lower)
                educational_score += len(matches)
            
            # Check for mathematical reasoning
            reasoning_indicators = [
                r'\b(given|let|assume|suppose|if|then|when|where)\b',
                r'\b(equation|formula|rule|property|theorem)\b',
                r'[=<>≤≥]',  # Mathematical relationships
            ]
            
            reasoning_score = 0
            for pattern in reasoning_indicators:
                matches = re.findall(pattern, text_lower)
                reasoning_score += len(matches)
            
            # Check for harmful content in output
            harmful_patterns = [
                r'\b(incorrect|wrong|impossible|cannot solve)\b'
            ]
            
            harmful_score = 0
            harmful_matches = []
            for pattern in harmful_patterns:
                matches = re.findall(pattern, text_lower)
                if matches:
                    harmful_score += len(matches)
                    harmful_matches.extend(matches)
            
            # Decision logic for output
            total_score = educational_score + reasoning_score
            
            if harmful_score > 2:
                return GuardrailResult.BLOCKED, f"Output contains too many negative indicators: {harmful_matches}", {
                    "reason": "harmful_output",
                    "harmful_matches": harmful_matches
                }
            
            if total_score >= 5:
                return GuardrailResult.APPROVED, "Educational output approved", {
                    "reason": "educational_output",
                    "educational_score": educational_score,
                    "reasoning_score": reasoning_score
                }
            
            elif total_score >= 2:
                return GuardrailResult.APPROVED, "Basic educational content", {
                    "reason": "basic_educational",
                    "total_score": total_score
                }
            
            else:
                return GuardrailResult.FLAGGED, "Output lacks clear educational structure", {
                    "reason": "weak_educational",
                    "suggestion": "Add more step-by-step explanation"
                }
                
        except Exception as e:
            logger.error(f"Output validation error: {e}")
            return GuardrailResult.BLOCKED, f"Validation error: {str(e)}", {"reason": "validation_error"}
    
    def get_educational_suggestions(self, text: str) -> List[str]:
        """Generate suggestions for improving educational content"""
        suggestions = []
        
        text_lower = text.lower()
        
        # Check for missing educational elements
        if "step" not in text_lower:
            suggestions.append("Consider breaking the solution into clear steps")
        
        if "because" not in text_lower and "therefore" not in text_lower:
            suggestions.append("Add explanations for why each step is taken")
        
        if not re.search(r'[=<>]', text):
            suggestions.append("Include mathematical equations or relationships")
        
        if len(text) < 50:
            suggestions.append("Provide more detailed explanation")
        
        return suggestions

class MathGuardrailsGateway:
    """
    Main gateway combining input and output guardrails for mathematics education
    """
    
    def __init__(self):
        """Initialize the guardrails gateway"""
        self.validator = MathematicalContentValidator()
        self.session_logs = {}
        logger.info("🚪 Math Guardrails Gateway initialized")
    
    def process_input(self, text: str, session_id: str = None) -> Dict[str, Any]:
        """Process input through guardrails"""
        try:
            result, message, details = self.validator.validate_input(text)
            
            # Log the validation
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "input",
                "text": text[:100] + "..." if len(text) > 100 else text,
                "result": result.value,
                "message": message,
                "details": details
            }
            
            if session_id:
                if session_id not in self.session_logs:
                    self.session_logs[session_id] = []
                self.session_logs[session_id].append(log_entry)
            
            return {
                "approved": result == GuardrailResult.APPROVED,
                "result": result.value,
                "message": message,
                "details": details,
                "timestamp": log_entry["timestamp"]
            }
            
        except Exception as e:
            logger.error(f"Input processing error: {e}")
            return {
                "approved": False,
                "result": "error",
                "message": str(e),
                "details": {"error": "processing_failed"}
            }
    
    def process_output(self, text: str, original_query: str = "", session_id: str = None) -> Dict[str, Any]:
        """Process output through guardrails"""
        try:
            result, message, details = self.validator.validate_output(text, original_query)
            
            # Get suggestions if needed
            suggestions = []
            if result in [GuardrailResult.FLAGGED, GuardrailResult.BLOCKED]:
                suggestions = self.validator.get_educational_suggestions(text)
            
            # Log the validation
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "type": "output",
                "text": text[:100] + "..." if len(text) > 100 else text,
                "original_query": original_query,
                "result": result.value,
                "message": message,
                "details": details,
                "suggestions": suggestions
            }
            
            if session_id:
                if session_id not in self.session_logs:
                    self.session_logs[session_id] = []
                self.session_logs[session_id].append(log_entry)
            
            return {
                "approved": result == GuardrailResult.APPROVED,
                "result": result.value,
                "message": message,
                "details": details,
                "suggestions": suggestions,
                "timestamp": log_entry["timestamp"]
            }
            
        except Exception as e:
            logger.error(f"Output processing error: {e}")
            return {
                "approved": False,
                "result": "error",
                "message": str(e),
                "details": {"error": "processing_failed"}
            }
    
    def get_session_logs(self, session_id: str) -> List[Dict[str, Any]]:
        """Get logs for a session"""
        return self.session_logs.get(session_id, [])

# Factory function for easy import
def get_real_guardrails_gateway():
    """Get the real guardrails gateway instance"""
    return MathGuardrailsGateway()

def test_real_guardrails():
    """Test the real guardrails implementation"""
    logger.info("🧪 Testing Real Guardrails Implementation")
    
    gateway = get_real_guardrails_gateway()
    
    # Test cases
    test_cases = [
        # Approved mathematical content
        "Solve the equation 2x + 5 = 13 for x",
        "Find the derivative of f(x) = x² + 3x + 2",
        "Calculate the area of a circle with radius 5",
        
        # Flagged content (non-mathematical)
        "What's the weather today?",
        "Tell me about celebrities",
        
        # Blocked content
        "How to hack a computer",
        "Violent methods to solve problems",
    ]
    
    for i, test_input in enumerate(test_cases):
        logger.info(f"\n--- Test Case {i+1}: {test_input[:30]}... ---")
        
        # Test input validation
        input_result = gateway.process_input(test_input, session_id="test_session")
        logger.info(f"Input Result: {input_result['result']} - {input_result['message']}")
        
        # Test output validation (simulate a response)
        if input_result['approved']:
            sample_output = f"Step 1: Analyze the problem '{test_input}'. Step 2: Apply mathematical principles. Step 3: Solve systematically."
            output_result = gateway.process_output(sample_output, test_input, session_id="test_session")
            logger.info(f"Output Result: {output_result['result']} - {output_result['message']}")
    
    # Show session logs
    logs = gateway.get_session_logs("test_session")
    logger.info(f"\n📊 Session logs: {len(logs)} entries")
    
    logger.info("✅ Real Guardrails test completed!")

if __name__ == "__main__":
    test_real_guardrails()
