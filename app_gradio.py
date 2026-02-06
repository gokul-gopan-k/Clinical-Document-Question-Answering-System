import gradio as gr
from core.models import load_models
from core.qa import ask_question
from core.retriever import process_pdf
from evaluation.benchmark import run_full_benchmark
# -----------------------------
# Gradio UI (Separated Logic)
# -----------------------------
with gr.Blocks(title="Clinical RAG QA system") as demo:
    gr.Markdown("# 🏥 Clinical RAG QA system")
    
    with gr.Row():
        pdf_input = gr.File(label="1. Upload Clinical PDF")
        process_btn = gr.Button("Process PDF")
    
    status_output = gr.Textbox(label="System Status", interactive=False)
    
    with gr.Tab("Chat"):
        gr.Markdown("### 🔍 Query the Clinical Protocol")
        with gr.Row():
            with gr.Column(scale=2):
                question_input = gr.Textbox(label="2. Ask a Clinical Question")
                ask_btn = gr.Button("Get Answer", variant="primary")
                answer_output = gr.Textbox(label="BioMistral Answer", lines=5)
            
            with gr.Column(scale=1):
                # This box shows the 'Evidence' from the PDF
                context_output = gr.Textbox(label="Retrieved Evidence (Sources)", lines=12)

        # Load models on startup to avoid delay during first query
        demo.load(load_models)
        
        process_btn.click(process_pdf, inputs=[pdf_input], outputs=[status_output])
        # Update the click function to handle TWO outputs
        ask_btn.click(ask_question, inputs=[question_input], outputs=[answer_output, context_output])

    with gr.Tab("Evaluation"):
        gr.Markdown("### Run Automated Benchmark against Gold Standard")
        run_all_btn = gr.Button("🚀 Run Full Evaluation Pipeline", variant="primary")
        
        with gr.Row():
            # Left side for the detailed list of logs
            eval_output = gr.Textbox(label="Per-Question Audit Logs", lines=15)
            # Right side for the final average stats 
            metric_output = gr.Markdown(label="Executive Performance Summary")

    # Both outputs are populated by a single function call
    run_all_btn.click(run_full_benchmark, outputs=[eval_output, metric_output])
if __name__ == "__main__":
    demo.launch()