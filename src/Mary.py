import transformers as tr
import time

def summarization(file_name, answer_len):
    with open(file_name, "r", encoding="utf-8", errors='ignore') as file:
        text = file.readlines()

    # Создаем pipeline для текстовой генерации
    summarizer = tr.pipeline(
        "text-generation",
        model="Qwen/Qwen3-14B",
        device_map="cpu",
        torch_dtype="auto")

    # Запрос
    messages = [
        {"role": "user", "content": f"Сделай краткое содержание этого текста на русском языке. После своих размышления сделай отступ в 2 перевода строки, а затем сразу выведи краткое содержание. Краткое содержание должно быть не более 300 слов: {text}"}]

    result = summarizer(
        messages,
        max_new_tokens=answer_len, #150
        temperature=0.7,
    )
    res_text = result[0]["generated_text"][-1]["content"]
    return res_text

#print(summarization("../docs/text1.txt", 300))

otsup = "---------------------------------------------------------------------------"
for i in range (2, 3):
    name = f"../docs/text{i}.txt"
    text_len = 0
    with open(name, "r", encoding="utf-8", errors='ignore') as file:
        for line in file:
            text_len += len(line)
    start_time = time.time()
    result = summarization(name, 1500)
    end_time = time.time()
    res_time = str(round(end_time - start_time)//60) + "min, " + str(round(end_time - start_time)%60) + "sec"
    result_plus = f"File text{i}.txt:\n{result}\n\nLead time: {res_time}\nText Length: {text_len}\n{otsup}\n\n\n"
    with open("../docs/summarization.txt", "a", encoding="utf-8", errors='ignore') as file:
        file.write(result_plus)
file.close()

