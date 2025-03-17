import gradio as gr
from PIL import Image
import os

def input_changed(image):
    if image == None:
        return gr.update(value=None), gr.update(value=None, visible=False), gr.update(visible=False)
    dim = f'{image.width} x {image.height}'
    return gr.update(value=image), gr.update(value=dim, visible=True), gr.update()

def quality_changed(quality, image):
    print(quality)
    image.save("compressed.jpg", "JPEG", quality=quality)
    compressed_image = Image.open('compressed.jpg')
    
    return gr.update(value=compressed_image), gr.update(value='compressed.jpg', visible=True)
    
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            input = gr.Image(label='input', type='pil', height=500)
            quality = gr.Slider(label='quality', minimum=0, maximum=100, value=100)
        with gr.Column():
            preview = gr.Image(label='preview', height=500)
            with gr.Row():
                dim = gr.Text(label='Image dimension', interactive=False, visible=False)
                download = gr.File(label='download compressed image', value=None, visible=False)
        
    input.change(fn=input_changed, inputs=[input], outputs=[preview, dim, download])
    quality.change(fn=quality_changed, inputs=[quality, input], outputs=[preview, download])

demo.launch()