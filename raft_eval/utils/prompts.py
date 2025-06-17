# raft_eval/utils/prompts.py

# raft_eval/utils/prompts.py

def build_prompt_for_metric(metric_name, question, context, answer):
    """
    Build prompt for a given metric.
    Returns full prompt text (str).
    """

    base_templates = {
        'faithfulness': '''
Вопрос:
{question}

Контекст (из базы знаний):
{context}

Ответ модели:
{answer}

Оцени фактологическую корректность (faithfulness) ответа модели с учётом приведённого контекста.
Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
''',

        'answer_relevancy': '''
Вопрос:
{question}

Контекст (из базы знаний):
{context}

Ответ модели:
{answer}

Пожалуйста, оцени _релевантность ответа_ модели по следующей шкале:
- 1.0 — полностью релевантен
- 0.5 — частично релевантен
- 0.0 — нерелевантен

Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
''',

        'style_score': '''
Вопрос:
{question}

Контекст (из базы знаний):
{context}

Ответ модели:
{answer}

Оцени стиль ответа (насколько он хорошо структурирован, грамотно сформулирован, понятен пользователю).
Используй шкалу от 0.0 (очень плохой стиль) до 1.0 (отличный стиль).

Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
''',

        'coverage': '''
Вопрос:
{question}

Контекст (из базы знаний):
{context}

Ответ модели:
{answer}

Оцени, насколько ответ модели покрывает ключевые аспекты из контекста, относящиеся к вопросу.
Если ответ упоминает все важные детали из контекста по данному вопросу — ставь высокий балл.

Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
''',
 'geval': '''
Вопрос:
{question}

Эталонный ответ (Reference):
{context}

Ответ модели:
{answer}

Оцени общую субъективная оценка качества ответа 
(учитывает всё: факты, стиль, полноту, понятность, релевантность).
Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
''',

        'answer_relevancy': '''
Вопрос:
{question}

Контекст (из базы знаний):
{context}

Ответ модели:
{answer}

Пожалуйста, оцени _релевантность ответа_ модели по следующей шкале:
- 1.0 — полностью релевантен
- 0.5 — частично релевантен
- 0.0 — нерелевантен

Ответь строго в формате JSON:
{{ "score": <число от 0 до 1> }}
'''
    }

    template = base_templates.get(metric_name.lower())

    if not template:
        raise ValueError(f"Unknown metric for prompt building: {metric_name}")

    return template.format(
        question=question.strip(),
        context=context.strip(),
        answer=answer.strip()
    )

def build_prompt(question: str, context: str) -> str:
    return DEFAULT_PROMPT_TEMPLATE.format(question=question, context=context)

DEFAULT_PROMPT_TEMPLATE = """Ты — помощник, который отвечает на вопросы ТОЛЬКО на основе приведённого ниже контекста.
Если нужной информации в контексте НЕТ — ответь строго фразой: "нет информации".

Контекст:
{context}

Вопрос:
{question}

Ответ:
"""


