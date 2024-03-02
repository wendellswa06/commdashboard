
import commune as c
import gradio as gr
from functools import lru_cache

class Sentence(c.Module):
    def __init__(self, 
                config=None,
                  **kwargs):
        config = self.set_config(config=config, kwargs=kwargs)
        self.set_model(model=config.model, device=config.device)
    
    @lru_cache(maxsize=2)
    def set_model(self, model:str, device:str):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model, device=device)

    @lru_cache(maxsize=32)
    def forward(self, text, **kwargs):
        initially_string = isinstance(text, str)
        if initially_string:
            text = [text]
        assert isinstance(text, list)
        assert isinstance(text[0], str)
        embeddings = self.model.encode(text, **kwargs)
        if initially_string:
            embeddings = embeddings[0]
        return embeddings
    
    @lru_cache(maxsize=32)
    def test(self):
        sentences = ["This is an example sentence", "Each sentence is converted"]
        embeddings = self.model.encode(sentences)
        c.print(embeddings.shape)
        sentences = "This is an example sentence"
        embeddings = self.model.encode(sentences)
        c.print(embeddings.shape)
        return embeddings
    
    def gradio(self):
        with gr.Blocks() as demo:
            with gr.Row():
                gr.Textbox("Not require UI. This convert text into embeddings.")
        demo.launch(share=True)
    
