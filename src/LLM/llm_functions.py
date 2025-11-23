import torch
from transformers import T5ForConditionalGeneration, GPT2Tokenizer

def simple_summary_no_tags(text):
    num_token = round((len(text)//200)*40)
    model_name = "RussianNLP/FRED-T5-Summarizer"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    prefix = "<LM> Сократи текст.\n "
    input_text = prefix + text
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, eos_token='</s>')
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
    input_ids = torch.tensor([tokenizer.encode(input_text)]).to(device)
    outputs = model.generate(
        input_ids,
        eos_token_id=tokenizer.eos_token_id,
        num_beams=5,
        min_new_tokens=17,
        max_new_tokens=num_token,
        do_sample=True,
        no_repeat_ngram_size=4,
        top_p=0.9, early_stopping=True)
    summary = tokenizer.decode(outputs[0][1:], skip_special_tokens=True)
    return summary

def summary_with_tags(text, keyword):
    num_token = round((len(text)//200)*20)
    model_name = "RussianNLP/FRED-T5-Summarizer"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    prefix = "<LM> Сократи текст.\n "
    prefix = (f"Проанализируй текст и выдели информацию, относящуюся к '{keyword}'. Если в тексте нет упоминаний или смысловой связи с этим словом, "
              f"верни строго 'нет информации'. В противном случае предоставь краткую выжимку (1-2 предложения) только по заданной теме. Текст:")
    input_text = prefix + text
    tokenizer = GPT2Tokenizer.from_pretrained(model_name, eos_token='</s>')
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)
    input_ids = torch.tensor([tokenizer.encode(input_text)]).to(device)
    outputs = model.generate(
        input_ids,
        eos_token_id=tokenizer.eos_token_id,
        num_beams=5,
        min_new_tokens=17,
        max_new_tokens=num_token,
        do_sample=True,
        no_repeat_ngram_size=4,
        top_p=0.9, early_stopping=True)
    summary = tokenizer.decode(outputs[0][1:], skip_special_tokens=True)
    return summary
