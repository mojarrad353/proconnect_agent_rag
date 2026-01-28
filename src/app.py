import gradio as gr
from dotenv import load_dotenv
from rag_engine import IcebreakerRAG

# Load environment variables
load_dotenv()

def get_icebreaker(name, company):
    if not name:
        return "Error: Please enter a name."
    try:
        # Gradio's default spinner will show while this runs
        bot = IcebreakerRAG()
        result = bot.generate_icebreaker(name=name, company=company)
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Custom CSS
custom_css = """
#component-0 {max_width: 800px; margin: auto;}
.gradio-container {font-family: 'Roboto', sans-serif;}
"""

# Build the Interface
with gr.Blocks() as demo:
    gr.Markdown(
        """
        # 🤝 LinkedIn Icebreaker Generator
        Generated from Google Web Search.
        """
    )
    
    with gr.Row():
        with gr.Column():
            name_input = gr.Textbox(
                label="Full Name", 
                placeholder="e.g. Jensen Huang",
                autofocus=True
            )
            company_input = gr.Textbox(
                label="Company (Optional)", 
                placeholder="e.g. NVIDIA"
            )
            submit_btn = gr.Button("Generate Icebreaker", variant="primary")
            
        with gr.Column():
            output_text = gr.Textbox(
                label="Extracted Role & Message", 
                lines=8,  
                interactive=False
            )

    # Use 'minimal' to show the default spinner without the timer text
    submit_btn.click(
        fn=get_icebreaker, 
        inputs=[name_input, company_input], 
        outputs=output_text,
        show_progress="minimal"
    )
    
    name_input.submit(
        fn=get_icebreaker, 
        inputs=[name_input, company_input], 
        outputs=output_text,
        show_progress="minimal"
    )

if __name__ == "__main__":
    print("--- LAUNCHING APP ---")
    print("If running locally, open: http://127.0.0.1:7860")
    
    demo.launch(css=custom_css, server_name="0.0.0.0")