import os
from conversaetl.models import PipelineSpecification, PipelineResult
from conversaetl.agents import PlannerAgent, GeneratorAgent, ValidatorAgent, OptimizerAgent

class MultiAgentOrchestrator:
    def __init__(self, api_key: str = None, use_rag: bool = False):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.planner = PlannerAgent(api_key=self.api_key)
        self.generator = GeneratorAgent(api_key=self.api_key)
        self.validator = ValidatorAgent(api_key=self.api_key)
        self.optimizer = OptimizerAgent(api_key=self.api_key)
        self.rag_retriever = None
        if use_rag:
            try:
                from conversaetl.rag.retriever import CodeExampleRetriever
                self.rag_retriever = CodeExampleRetriever()
            except:
                pass
        print(' Orchestrator ready')
    
    def generate_pipeline(self, spec: PipelineSpecification) -> PipelineResult:
        print(f'\n Generating: {spec.name}')
        print('='*50)
        
        print('1 Planning...')
        plan_result = self.planner.execute(spec)
        print(f'    {plan_result["step_count"]} steps')
        
        examples = []
        if self.rag_retriever:
            print('2 Retrieving examples...')
            examples = self.rag_retriever.retrieve(spec.name, top_k=3)
            print(f'    {len(examples)} examples')
        
        print('3 Generating code...')
        gen_result = self.generator.execute(spec, plan_result['plan'], examples)
        print(f'    {gen_result["lines"]} lines')
        
        print('4 Validating...')
        val_result = self.validator.execute(gen_result['code'])
        print(f'    {val_result["score"]:.2%}')
        
        print('5 Optimizing...')
        opt_result = self.optimizer.execute(gen_result['code'])
        print(f'    {opt_result["score"]:.2%}')
        
        print('='*50)
        print(' Done!')
        
        return PipelineResult(
            generated_code=gen_result['code'],
            validation_score=val_result['score'],
            optimization_score=opt_result['score'],
            performance_metrics={'plan_steps': plan_result['step_count'], 'code_lines': gen_result['lines']},
            retrieved_examples=examples
        )
