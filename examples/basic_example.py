import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversaetl import MultiAgentOrchestrator, DataSource, DataTarget, PipelineSpecification

def main():
    print(' ConversaETL Example')
    orchestrator = MultiAgentOrchestrator()
    
    spec = PipelineSpecification(
        name='customer_pipeline',
        source=DataSource(type='csv', location='data/customers.csv', schema={'id': 'integer'}),
        target=DataTarget(type='postgresql', connection_string='postgresql://localhost/db', table='customers'),
        transformations=['Clean emails', 'Remove duplicates'],
        requirements=['Handle nulls']
    )
    
    result = orchestrator.generate_pipeline(spec)
    print(f'\n Validation: {result.validation_score:.2%}')
    print(f' Optimization: {result.optimization_score:.2%}')
    
    result.save_code(f'{spec.name}.py')
    print(f'\n Preview:\n{"="*60}')
    for i, line in enumerate(result.generated_code.split('\n')[:15], 1):
        print(f'{i:3d} | {line}')
    print("="*60)

if __name__ == '__main__':
    main()
