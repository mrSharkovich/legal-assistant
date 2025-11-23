import torch
from transformers import T5ForConditionalGeneration, GPT2Tokenizer


_model = None
_tokenizer = None
_device = None

def load_model():
    global _model, _tokenizer, _device
    if _model is None:
        model_name = "RussianNLP/FRED-T5-Summarizer"
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _tokenizer = GPT2Tokenizer.from_pretrained(model_name, eos_token='</s>')
        _model = T5ForConditionalGeneration.from_pretrained(model_name).to(_device)
        print(f"Модель загружена на устройство: {_device}")


def simple_summary_no_tags(text):
    global _model, _tokenizer, _device
    if _model is None:
        load_model()
    num_token = round((len(text)//200)*40)
    prefix = "<LM> Сократи текст.\n "
    input_text = prefix + text
    input_ids = torch.tensor([_tokenizer.encode(input_text)]).to(_device)
    outputs = _model.generate(
        input_ids,
        eos_token_id=_tokenizer.eos_token_id,
        num_beams=3,
        min_new_tokens=17,
        max_new_tokens=num_token,
        do_sample=False,
        no_repeat_ngram_size=4,
        top_p=0.9,
        early_stopping=True)
    summary = _tokenizer.decode(outputs[0][1:], skip_special_tokens=True)
    return summary

def summary_with_tags(text, keyword):
    global _model, _tokenizer, _device
    if _model is None:
        load_model()
    num_token = round((len(text)//200)*20)
    prefix = (f"<LM> Проанализируй текст и выдели информацию, относящуюся к '{keyword}'. Если в тексте нет упоминаний или смысловой связи с этим словом, "
            f"верни строго 'нет информации'. В противном случае предоставь краткую выжимку (1-2 предложения) только по заданной теме. Текст:")
    input_text = prefix + text[:2000]  # Ограничиваем входной текст
    input_ids = torch.tensor([_tokenizer.encode(input_text)]).to(_device)
    outputs = _model.generate(
        input_ids,
        eos_token_id=_tokenizer.eos_token_id,
        num_beams=3,
        min_new_tokens=17,
        max_new_tokens=num_token,
        do_sample=False,
        no_repeat_ngram_size=4,
        top_p=0.9,
        early_stopping=True)
    summary = _tokenizer.decode(outputs[0][1:], skip_special_tokens=True)
    return summary

