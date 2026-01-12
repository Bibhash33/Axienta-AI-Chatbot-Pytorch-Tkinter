import torch

class ChatPredictor:
    def __init__(self, model, tokenizer, config):
        self.model = model
        self.tokenizer = tokenizer
        self.config = config

    def predict(self, prompt: str) -> str:
        encoded = self.tokenizer.encode(prompt)

        input_ids = encoded["input_ids"].to(self.model.device)
        attention_mask = encoded["attention_mask"].to(self.model.device)

        output_ids = self.model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,

            # ✅ Generate new content only
            max_new_tokens=80,

            # ✅ Sampling (important)
            do_sample=True,
            temperature=0.7,
            top_p=0.9,

            # ✅ ANTI-REPETITION (CRITICAL)
            repetition_penalty=1.2,
            no_repeat_ngram_size=3,

            # ✅ Proper termination
            eos_token_id=self.tokenizer.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.tokenizer.eos_token_id,
        )

        # Slice out only the generated part
        generated_tokens = output_ids[0][input_ids.shape[-1]:]

        response = self.tokenizer.decode(
            generated_tokens
        )

        return response.strip()
