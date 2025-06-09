# raft_eval/utils/llm_client.py

import os
import requests
import time
from dotenv import load_dotenv

# Загружаем OPENROUTER_API_KEY из .env
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Можно будет менять модель
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324"

# Call LLM
def call_llm(prompt, model=DEFAULT_MODEL, max_retries=3, temperature=0.0):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openrouter.ai",  # можно заменить на свой сайт
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Ты эксперт по оценке качества ответов LLM / RAG систем. Ты оцениваешь ответы по заданным метрикам. Отвечай только числом от 0 до 1 или в формате {\"score\": <значение>}."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": 512,
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            message = data["choices"][0]["message"]["content"]
            return parse_llm_response(message)
        except Exception as e:
            print(f"[call_llm] Error: {e} | Attempt {attempt + 1}/{max_retries}")
            time.sleep(2)

    # Если не удалось → fallback
    print("[call_llm] Failed after retries.")
    return {"score": 0.0}

# Простая функция парсинга → будем улучшать при необходимости
def parse_llm_response(text):
    """
    Ожидаем от LLM что она вернёт просто число или JSON вида {"score": 0.85}.
    """
    import re
    import json

    # Пробуем сначала распарсить как JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "score" in data:
            return {"score": float(data["score"])}
    except:
        pass

    # Если не JSON → пробуем найти число в тексте
    match = re.search(r"([0-9]+(\.[0-9]+)?)", text)
    if match:
        score = float(match.group(1))
        return {"score": score}

    # Fallback → 0.0
    return {"score": 0.0}

class LLMClient:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name

    def generate_answer(self, prompt, temperature=0.0):
        # Используем твой call_llm, но не парсим score, а возвращаем текст (ответ LLM)
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openrouter.ai",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                # Не нужен system-промт про оценки — мы хотим обычный генеративный ответ!
                {"role": "user", "content": prompt},
            ],
            "temperature": temperature,
            "max_tokens": 512,
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"[LLMClient.generate_answer] Error: {e} | Attempt {attempt+1}/3")
                time.sleep(2)
        return "[ошибка LLM]"

# Для метрик ты можешь оставить свою call_llm (для faithfulness и прочих)
