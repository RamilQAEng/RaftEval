# RaftEval
---
### Built with the tools and technologies:

![Markdown](https://img.shields.io/badge/-Markdown-000000?style=for-the-badge&logo=markdown)
![Typer](https://img.shields.io/badge/-Typer-16A085?style=for-the-badge)
![TOML](https://img.shields.io/badge/-TOML-8D6748?style=for-the-badge)
![scikit-learn](https://img.shields.io/badge/-scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![tqdm](https://img.shields.io/badge/-tqdm-F7B93E?style=for-the-badge)
![Rich](https://img.shields.io/badge/-Rich-FFD700?style=for-the-badge)
![SymPy](https://img.shields.io/badge/-SymPy-3B5526?style=for-the-badge)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=for-the-badge&logo=numpy)
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python)
![SciPy](https://img.shields.io/badge/-SciPy-8CAAE6?style=for-the-badge&logo=scipy)
![pandas](https://img.shields.io/badge/-pandas-150458?style=for-the-badge&logo=pandas)
![OpenAI](https://img.shields.io/badge/-OpenAI-412991?style=for-the-badge&logo=openai)
![Pydantic](https://img.shields.io/badge/-Pydantic-EF4A7B?style=for-the-badge)



# 🚀 RaftEval — Framework для автоматизированной оценки качества RAG / LLM систем

RaftEval — это фреймворк для **batch-оценки и интерактивной оценки** качества генеративных LLM / RAG систем по множеству метрик: от фактической корректности до стиля и стоимости ответа.

Позволяет автоматически оценивать таблицы (Excel/CSV/JSONL) с парами `question → context → answer`, получать метрики в удобном виде для анализа и отчетности.

## 📊 Поддерживаемые метрики

| Метрика               | Где считается / способ вычисления                   | За что отвечает |
|-----------------------|----------------------------------------------------|-----------------|
| **BERTScore**         | `bert_score`                                       | Семантическое сходство с эталоном |
| **GEval**             | LLM-based → prompt + LLM                           | Общая оценка качества ответа |
| **Faithfulness**      | LLM-based → prompt + LLM                           | Фактологическая корректность (нет ли галлюцинаций) |
| **Answer Relevancy**  | LLM-based → prompt + LLM                           | Насколько ответ релевантен вопросу |
| **Coverage**          | LLM-based → prompt + LLM                           | Полнота покрытия релевантного контекста |
| **Style (тональность)** | LLM-based → prompt + LLM                          | Качество и понятность стиля ответа |
| **Toxicity**          | LLM-based → prompt + LLM                           | Проверка токсичности и неприемлемого контента |
| **Length penalty**    | Простая метрика                                    | Штраф за слишком короткие/длинные ответы |
| **Token Count**       | Простая метрика                                    | Количество токенов в ответе |
| **Cost per answer**   | Простая метрика → `cost_calculator`                | Финансовая стоимость генерации ответа |

## ⚙️ Как работает

1. Загружаете таблицу с данными:
    - Вопрос (Question)
    - Контекст (Context, retrieved from KB)
    - Ответ модели (Answer)
    - Эталон ответа (gold_answer)

2. Вызываете:
```bash
raft-eval evaluate --input-path my_data.xlsx --output-path output.xlsx --metrics all
```
3. На выходе получаете таблицу с оценками по всем выбранным метрикам.
4. Отдельно доступен interactive режим → позволяет вручную задать вопрос и оценить ответ в реальном времени.
## 🔥 Типичные use-cases

| Use-case                              | Рекомендуемые метрики                                 |
| ------------------------------------- | ---------------------------------------------------- |
| RAG QA System (Retrieval Augmented QA) | Faithfulness, Coverage, Relevancy                     |
| LLM Chat Assistant (Customer Support)  | Relevancy, Style, Toxicity, Faithfulness              |
| Marketing AI Writer (Copywriting)     | Style, Relevancy, Length, Cost per answer             |
| Summarization / Generation            | BERTScore, Faithfulness, GEval                         |
| Internal LLM Quality Audit            | GEval, Faithfulness, Coverage, Cost                   |

## 📦 Архитектура

- **Метрики:** `raft_eval/metrics/`
- **Вызовы LLM:** `raft_eval/utils/llm_client.py`
- **Промпты:** `raft_eval/utils/prompts.py`
- **Логирование:** `raft_eval/utils/save_utils.py`
- **CLI-интерфейс:** `raft_eval/cli.py`

## 🌐 Интеграция с LLM

- Используется **OpenRouter API** (`OPENROUTER_API_KEY` в `.env`).
- LLM модели могут быть любыми (**GPT-4o**, **Claude**, **Gemini** и др.).
- Промпты для каждой метрики задаются в `prompts.py`.

# 🛣️ RaftEval Roadmap

## 🔜 Версия 1.1 — Production-ready

- **Кэширование LLM-вызовов**  
  Встроенный in-memory cache (`dict`, `@lru_cache`) и disk-кэш на базе `diskcache` для повторного использования между сессиями.

- **Асинхронная обработка и батчи**  
  Реализация `evaluate_batch()` с параллельной обработкой. Использование `asyncio` и `Semaphore` для ускорения оценки больших датасетов (10k+ запросов).

- **Retry и обработка ошибок**  
  Подключение `tenacity` или кастомного retry-обёртки с exponential backoff для защиты от ошибок сети и перегрузки API (429/500).

- **Юнит-тестирование ядра**  
  Тесты для всех `.compute()` методов, утилит токенизации, подсчёта стоимости и кэширования. Цель — покрытие ≥ 90%.

- **Настроить базовый CI/CD pipeline через GitHub Actions**  
  Запуск тестов, линтера, проверка CLI, генерация coverage-отчётов.

---

## 🟡 Версия 1.2 — Архитектура и API

- Вынести все метрики в единый `Metric`-класс с интерфейсом `.compute()`  
- Реализовать `Metric Registry` с поддержкой `@register_metric`  
- Поддержка нескольких LLM-клиентов через универсальный интерфейс (`OpenAI`, `OpenRouter`, `DeepSeek`)  
- **Реализовать API-интерфейс через класс `Evaluator`**  
- Подготовить документацию (CLI/SDK usage, добавление кастомных метрик) с возможной интеграцией в `mkdocs`

## 📦 Установка через GitHub

# (Рекомендуется) Создайте изолированное окружение
```bash
python3 -m venv venv
```
Linux/MacOS
```bash
source venv/bin/activate
```
Windows: 
```bash
venv\Scripts\activate
```
# Установка последней версии RaftEval с GitHub
```bash
pip install git+https://github.com/RamilQAEng/RaftEval.git
```
⚙️ Конфигурация API-ключа (OpenAI)
RaftEval использует OpenAI / OpenRouter для LLM-оценки. Необходим API-ключ:

# Создайте .env файл в корне проекта

Linux/macOS:
```bash
touch .env
```
Windows
```bash
New-Item -Path . -Name ".env" -ItemType "file"
```

Внутрь .env добавьте строку:
OPENROUTER_API_KEY=sk-...

## 💻 Пример использования

### Evaluate

```bash
raft-eval evaluate \
  --input-path DataBase.xlsx \
  --output-path output.xlsx \
  --metrics faithfulness,answer_relevancy,coverage,style_score,token_count,cost_metric
```

### 🚀 Interactive mode

```bash
raft-eval interactive --knowledge-base-path NameBase.xlsx
```

Можно ввести произвольный вопрос:

- RAG ищет контекст → ответ → оценка по метрикам

## 🤝 Авторство

- **Проект:** RaftEval
- **Автор:** Ramil Allakhverdiev
- **Помощь:** ChatGPT 4o + OpenRouter API + 🛠 собственные кастомные метрики
