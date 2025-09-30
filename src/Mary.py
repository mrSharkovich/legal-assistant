import transformers as tr

with open("text.txt", "r", encoding="utf-8", errors='ignore') as file:
    text = file.readlines()


# Создаем pipeline для текстовой генерации
summarizer = tr.pipeline(
    "text-generation",
    model="openai/gpt-oss-20b",
    device_map="cpu",
    torch_dtype="auto")

#Запрос
messages = [
    {"role": "user", "content": f"Сделай краткий пересказ этого текста: {text}"}]

result = summarizer(
    messages,
    max_new_tokens=150,
    temperature=0.7,
)

# Печатаем результат
print(result[0]["generated_text"][-1]["content"])