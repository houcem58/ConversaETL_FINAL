from conversaetl.agents.base import BaseAgent
import ast
from typing import Dict, Any

class ValidatorAgent(BaseAgent):
    def __init__(self, api_key: str = None):
        super().__init__('Validator', 'You validate code quality.', api_key)
    
    def execute(self, code: str) -> Dict[str, Any]:
        issues = []
        score = 1.0
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(f'Syntax: {e}')
            score -= 0.3
        if 'import pandas' not in code:
            issues.append('Missing pandas')
            score -= 0.1
        if 'try:' not in code:
            issues.append('No error handling')
            score -= 0.15
        return {'status': 'success', 'score': max(0, min(1, score)), 'issues': issues, 'is_valid': score >= 0.7}
