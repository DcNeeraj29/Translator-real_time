from transformers import MarianMTModel, MarianTokenizer

Model_name = 'Helsinki-NLP/opus-mt-hi-en'

tokenizer = MarianTokenizer.from_pretrained(Model_name)
model = MarianMTModel.from_pretrained(Model_name)

def translate(text: str) -> str:
    if not text.strip():
        return ""
    
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

if __name__ == "__main__":
    print(translate("मैं कॉलेज जा रहा हूँ")) # Custom input to test the translation function
    