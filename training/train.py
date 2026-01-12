import torch
from transformers import Trainer, TrainingArguments

def train(model, tokenizer, dataset, output_dir:str):
    args = TrainingArguments(output_dir=output_dir,
                             per_device_train_batch_size=4,
                             learning_rate=5e-5,
                             num_train_epochs=3,
                             fp16=True,
                             gradient_accumulation_steps=8,
                            logging_steps=50,
                            save_steps=500,
                            save_total_limit=2
                             )
    trainer = Trainer(model=model, tokenizer=tokenizer, train_dataset=dataset, args=args)
    trainer.train()
