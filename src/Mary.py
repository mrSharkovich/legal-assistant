"""
This module for Mary's work, LLM engineer.
"""
import transformers as tr
import torch

model_name = "openai/gpt-oss-20b"
tokenizer = tr.AutoTokenizer.from_pretrained(model_name)
model = tr.AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")
pipe = tr.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer)

prompt = "Напиши краткое объяснение, что такое искусственный интеллект."

messages = [{"content": prompt}]

formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

outputs = pipe(formatted_prompt)
print(outputs[0]['generated_text'])