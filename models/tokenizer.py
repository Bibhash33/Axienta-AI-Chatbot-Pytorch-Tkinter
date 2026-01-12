from transformers import AutoTokenizer

class ChatbotTokenizer:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def encode(self, text: str):
        return self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

    def decode(self, tokens):
        return self.tokenizer.decode(
            tokens,
            skip_special_tokens=True
        )
