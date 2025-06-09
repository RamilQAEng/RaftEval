import pandas as pd
import jsonlines

def load_dataset(input_path):
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
    elif input_path.endswith(".xlsx"):
        df = pd.read_excel(input_path)
    elif input_path.endswith(".jsonl"):
        with jsonlines.open(input_path) as reader:
            df = pd.DataFrame(reader)
    else:
        raise ValueError(f"Unsupported input format: {input_path}")

    required_columns = ["question", "context", "answer"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Поддержка gold_answer (опционально)
    gold_answers = df.get("gold_answer", pd.Series([""] * len(df))).tolist()

    return df["question"].tolist(), df["context"].tolist(), df["answer"].tolist(), gold_answers
