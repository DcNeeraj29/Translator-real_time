from transformers import MarianMTModel, MarianTokenizer

class TextTranslator:
    def __init__(self, src_lang="en", tgt_lang="hi"):
        self.src = src_lang
        self.tgt = tgt_lang

        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        print(f"Loading translation model: {model_name}...")

        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)

    
    def translate(self, text: str) -> str:
        if not text or not text.strip():
            return ""
        
        inputs = self.tokenizer(text, return_tensors = "pt", padding = True, truncation=True)
        outputs = self.model.generate(**inputs)
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
