import torch
from transformers import AutoModelForCausalLM

class ChatbotModel:
    def __init__(self, model_name: str, device: str):
        self.device = device
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.model.to(self.device)

    def generate(self, input_ids, attention_mask, **gen_kwargs):
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids = input_ids,
            attention_mask = attention_mask,
            **gen_kwargs
            )

        return outputs
