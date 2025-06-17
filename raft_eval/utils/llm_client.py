# llm_client.py
import os, json, re
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"
TEMPERATURE = 0.5
MAX_TOKENS = 512

def generate_answer(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[generate_answer] Ошибка: {e}")
        return "[ошибка LLM]"

def call_llm(prompt: str, parse_score: bool = True) -> dict | str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты эксперт по оценке качества ответов LLM / RAG систем. "
                        "Ты оцениваешь ответы по заданным метрикам. "
                        "Отвечай только числом от 0 до 1 или в формате {\"score\": <значение>}."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        message = response.choices[0].message.content.strip()
        return parse_llm_score(message) if parse_score else message

    except Exception as e:
        print(f"[call_llm] Ошибка: {e}")
        return {"score": 0.0} if parse_score else "[ошибка LLM]"

def parse_llm_score(text: str) -> dict:
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "score" in data:
            return {"score": float(data["score"])}
    except Exception:
        pass

    match = re.search(r"([0-9]+(\.[0-9]+)?)", text)
    if match:
        return {"score": float(match.group(1))}

    return {"score": 0.0}
