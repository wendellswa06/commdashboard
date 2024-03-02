import commune as c
import gradio as gr
import requests
import torch
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
from functools import lru_cache

class ModelImage2image(c.Module):
    def __init__(self,  model_id_or_path = "runwayml/stable-diffusion-v1-5", **kwargs):
        device = f"cuda:{c.most_free_gpu()}"
        self.model_id_or_path = model_id_or_path
        self.device = device

    @lru_cache(maxsize=2)  # Cache model initialization
    def initialize_model(self, model_id_or_path, device):
        pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            model_id_or_path, torch_dtype=torch.get_default_dtype())
        pipe = pipe.to(device)
        pipe.enable_attention_slicing()
        return pipe

    def call(self, x: int = 1, y: int = 2) -> int:
        c.print(self.config.sup)
        c.print(self.config, 'This is the config, it is a Munch object')
        return x + y

    @lru_cache(maxsize=8)
    def transform(self, init_image, textPrompt, strength=0.5, guidance_scale=15, module=None):
        if module != None:
            return c.connect(module).transform(textPrompt=textPrompt, 
                                               strength=strength, 
                                               guidance_scale=guidance_scale)
        init_image = Image.open(init_image).convert("RGB")
        init_image = init_image.resize((768, 512))
        pipe = self.initialize_model(self.model_id_or_path, self.device)
        images = pipe(prompt=textPrompt, image=init_image,
                      strength=strength, guidance_scale=guidance_scale).images
        image = images[0]
        return image

    def gradio(self, share=False):
        demo = gr.Interface(
            fn=self.transform,
            inputs=[gr.Image(type='filepath'), "text",
                    gr.Slider(0, 1), gr.Slider(1, 30)],
            outputs=["image"],
            allow_flagging="never",
        )
        demo.launch(share=True)
