import commune as c
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import gradio as gr
from functools import lru_cache

class ModelImage2text(c.Module):
    def __init__(self, config = None, **kwargs):
        self.set_config(config, kwargs=kwargs)
        self.processor, self.model = self.initialize_model()

    @lru_cache(maxsize=2)
    def initialize_model(self):
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return processor, model
    
    def call(self, x:int = 1, y:int = 2) -> int:
        c.print(self.config.sup)
        c.print(self.config, 'This is the config, it is a Munch object')
        return x + y
    
    @lru_cache(maxsize=8)
    def image2text(self, img_url='https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'):
        raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

        # conditional image captioning
        # text = "a photography of"
        # inputs = processor(raw_image, text, return_tensors="pt")

        # out = model.generate(**inputs)
        # print(processor.decode(out[0], skip_special_tokens=True))
        # >>> a photography of a woman and her dog

        # unconditional image captioning
        inputs = self.processor(raw_image, return_tensors="pt")

        out = self.model.generate(**inputs)
        print(self.processor.decode(out[0], skip_special_tokens=True))

        return self.processor.decode(out[0], skip_special_tokens=True)

    
    def gradio(self, share=False):
        demo = gr.Interface(
            fn=self.image2text,
            inputs=["text"],
            outputs="text",
            allow_flagging="never",
        )
        demo.launch(share=True)
