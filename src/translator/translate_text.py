from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading translation model... ")
model_name = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Language mapping
LANG_MAP = {
    "en":"eng_Latn",
    "hi":"hin_Deva",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
    "ru": "rus_Cyrl"
}

class TextTranslator:
    def __init__(self, src_lang="en", tgt_lang="hi"):
        self.src = LANG_MAP.get(src_lang)
        self.tgt = LANG_MAP.get(tgt_lang)
    
    def translate(self, text: str) -> str:
        if not text.strip():
            return ""
        
        # Setting up src lang
        tokenizer.src_lang = self.src
        inputs = tokenizer(text, return_tensors="pt")

        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id = tokenizer.convert_tokens_to_ids(self.tgt)
        )

        translated_text = tokenizer.decode(
            translated_tokens[0],
            skip_special_tokens=True
        )
        return translated_text
    
