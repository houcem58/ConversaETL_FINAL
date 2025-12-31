from conversaetl.agents.base import BaseAgent
from conversaetl.models import PipelineSpecification
from typing import Dict, Any

class PlannerAgent(BaseAgent):
    def __init__(self, api_key: str = None):
        super().__init__('Planner', 'You are an ETL architect. Create execution plans.', api_key)
    
    def execute(self, spec: PipelineSpecification) -> Dict[str, Any]:
        prompt = f'''Create plan for ETL: {spec.name}
Source: {spec.source.type.value} from {spec.source.location}
Target: {spec.target.type.value} to {spec.target.table}
Transformations: {', '.join(spec.transformations)}
Generate numbered steps.'''
        
        plan = self.call_llm(prompt, temperature=0.3)
        steps = [l.strip() for l in plan.split('\n') if l.strip() and l[0].isdigit()]
        return {'status': 'success', 'plan': plan, 'steps': steps, 'step_count': len(steps)}
