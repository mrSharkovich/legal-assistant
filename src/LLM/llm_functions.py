import torch
from transformers import T5ForConditionalGeneration, GPT2Tokenizer
import hashlib
import os

_model = None
_tokenizer = None
_device = None
TOKEN_CACHE_FILE = "token_cache.pt"# Файл для сохранения токенов


def load_model():
    global _model, _tokenizer, _device
    if _model is None:
        model_name = "RussianNLP/FRED-T5-Summarizer"
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        _tokenizer = GPT2Tokenizer.from_pretrained(model_name, eos_token='</s>')
        _model = T5ForConditionalGeneration.from_pretrained(model_name).to(_device)
        print(f"Модель загружена на устройство: {_device}")


def save_tokens_to_cache(input_ids, text_hash):
    """Сохраняет токены и хеш текста в файл"""
    cache_data = {
        'input_ids': input_ids.cpu(),
        'text_hash': text_hash
    }
    torch.save(cache_data, TOKEN_CACHE_FILE)


def load_tokens_from_cache(text_hash):
    """Загружает токены из файла, если хеш совпадает"""
    if not os.path.exists(TOKEN_CACHE_FILE):
        return None

    try:
        cache_data = torch.load(TOKEN_CACHE_FILE)
        if cache_data.get('text_hash') == text_hash:
            return cache_data['input_ids'].to(_device if _device else "cpu")
    except:
        pass
    return None


def clear_token_cache():
    """Очищает кэш токенов"""
    if os.path.exists(TOKEN_CACHE_FILE):
        os.remove(TOKEN_CACHE_FILE)


def get_text_hash(text):
    """Вычисляет хеш текста для идентификации"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def simple_summary_no_tags(text):
    global _model, _tokenizer, _device
    if _model is None:
        load_model()
    text_hash = get_text_hash(text)
    input_ids = load_tokens_from_cache(text_hash)
    if input_ids is None: # Токенизируем текст, если нет в кэше
        prefix = "<LM> Сократи текст.\n "
        input_text = prefix + text
        input_ids = torch.tensor([_tokenizer.encode(input_text)]).to(_device)
        save_tokens_to_cache(input_ids, text_hash) # Сохраняем токены в кэш
    num_token = round((len(text) // 200) * 40)
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
    text_hash = get_text_hash(text)
    # Пытаемся загрузить токены из кэша
    input_ids = load_tokens_from_cache(text_hash)
    if input_ids is None:
        prefix = (
            f"<LM> Проанализируй текст и выдели информацию, относящуюся к '{keyword}'. Если в тексте нет упоминаний или смысловой связи с этим словом, "
            f"верни строго 'нет информации'. В противном случае предоставь краткую выжимку (1-2 предложения) только по заданной теме. Текст:")
        input_text = prefix + text[:2000]
        input_ids = torch.tensor([_tokenizer.encode(input_text)]).to(_device)
        save_tokens_to_cache(input_ids, text_hash)
    else:
        prefix = (
            f"<LM> Проанализируй текст и выдели информацию, относящуюся к '{keyword}'. Если в тексте нет упоминаний или смысловой связи с этим словом, "
            f"верни строго 'нет информации'. В противном случае предоставь краткую выжимку (1-2 предложения) только по заданной теме. Текст:")
        prefix_ids = torch.tensor([_tokenizer.encode(prefix)]).to(_device)
        text_ids = torch.tensor([_tokenizer.encode(text)]).to(_device)
        input_ids = torch.cat([prefix_ids, text_ids], dim=1)
    num_token = round((len(text) // 200) * 20)
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