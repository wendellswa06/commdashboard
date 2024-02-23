import commune as c
import json

Vali = c.module('vali')
class ValiTextRealfake(Vali):
    def __init__(self, config=None, **kwargs):
        config = self.set_config(config=config, kwargs=kwargs)   
        self.dataset =  c.module(config.dataset)()
        self.init_vali(config)

    def create_prompt(self, sample: dict) -> str:
        # format the prompt
    
        prompt = f'''
        INPUT (JSON):
        ```{sample}```
        QUESTION: 
        WAS THE INPUT REAL (1) OR TAMPERED (0)? -> :
        GIVE THE ANSWER AS AN INDEX -> {{answer:int}} ?
        EXAMPLE: {{answer:0}}
        json```
        '''

        return prompt
        

    def score_module(self, module, **kwargs):
        w = 0
        module = c.connect(module) if isinstance(module, str) else module

        sample = self.dataset.sample()
        t = c.time()

        
        
        target = sample.pop(self.config.target) # a list of correct answers
        prompt = self.create_prompt(sample)
        output = module.generate(prompt)
        prediction = str(output)
        w = int(str(target) in str(prediction))
        response = {
            'sample': sample,
            'target': target, 
            'prediction': prediction,
            'output': output,
            'w' : w,
            }



        return response


    @classmethod
    def test(cls, module='model.openai', **kwargs):
        vali = cls(start=False)
        return vali.score_module(module=module, **kwargs)

