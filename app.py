import gradio as gr
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from conversaetl import MultiAgentOrchestrator, DataSource, DataTarget, PipelineSpecification

orchestrator = MultiAgentOrchestrator()

def generate(user_input: str, lang: str = 'Python'):
    if not user_input.strip():
        return ' Enter description', '', ''
    try:
        spec = PipelineSpecification(
            name='pipeline',
            source=DataSource(type='csv', location='input.csv', schema={}),
            target=DataTarget(type='postgresql', connection_string='postgresql://localhost/db', table='output'),
            transformations=['Process data'],
            requirements=[]
        )
        result = orchestrator.generate_pipeline(spec)
        status = f' Generated!\nValidation: {result.validation_score:.2%}\nOptimization: {result.optimization_score:.2%}'
        return status, result.generated_code, 'import plotly.express as px\nfig = px.bar(df, x="x", y="y")'
    except Exception as e:
        return f' Error: {e}', '', ''

with gr.Blocks(title='ConversaETL') as demo:
    gr.Markdown('#  ConversaETL: AI ETL Generator')
    with gr.Row():
        with gr.Column():
            inp = gr.Textbox(label='Pipeline Description', lines=5, placeholder='Load data, clean, save...')
            btn = gr.Button(' Generate', variant='primary')
        status = gr.Textbox(label='Status', lines=10)
    with gr.Row():
        code = gr.Code(label='Generated Code', language='python')
        viz = gr.Code(label='Visualization', language='python')
    btn.click(generate, [inp], [status, code, viz])

demo.launch(share=True)
