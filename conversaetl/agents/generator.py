from conversaetl.agents.base import BaseAgent
from conversaetl.models import PipelineSpecification
from typing import Dict, Any, List

class GeneratorAgent(BaseAgent):
    def __init__(self, api_key: str = None):
        super().__init__('Generator', 'You are a Python expert. Generate ETL code.', api_key)
    
    def execute(self, spec: PipelineSpecification, plan: str = '', examples: List[Dict] = None) -> Dict[str, Any]:
        prompt = f'''Generate Python ETL for: {spec.name}
Source: {spec.source.location}
Target: {spec.target.table}
Transformations: {', '.join(spec.transformations)}
Plan: {plan}
Include imports, logging, error handling, main block.'''
        
        code = self.call_llm(prompt, temperature=0.2, max_tokens=2500)
        if '`python' in code:
            code = code.split('`python')[1].split('`')[0].strip()
        return {'status': 'success', 'code': code, 'language': 'python', 'lines': len(code.split('\n'))}
