# raft_eval/utils/save_utils.py

import pandas as pd
import jsonlines
from datetime import datetime
import os

def log_batch_evaluation(results, output_path=None):
    df_rows = []

    for row in results:
        flat_row = {}
        for k, v in row.items():
            if isinstance(v, dict):
                # Flatten dict (e.g. ROUGE returns dict)
                for sub_k, sub_v in v.items():
                    # Example: rouge1, rouge2, rougeL
                    flat_row[f"{k}_{sub_k}" if not k.startswith("rouge") else sub_k] = sub_v
            else:
                flat_row[k] = v
        df_rows.append(flat_row)

    df = pd.DataFrame(df_rows)

    if not output_path:
        # Default filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        output_path = f"batch_evaluation_{timestamp}.jsonl"

    # Save .xlsx if needed
    if output_path.endswith(".xlsx"):
        # 👉 Здесь укажем порядок колонок
        cols_order = ["question", "answer", "context", "gold_answer"]
        metric_cols = [col for col in df.columns if col not in cols_order]
        df = df[cols_order + metric_cols]

        df.to_excel(output_path, index=False)
        print(f"✅ Saved batch results to {output_path}")

    # Save .jsonl if needed
    elif output_path.endswith(".jsonl"):
        with jsonlines.open(output_path, mode="w") as writer:
            for row in df.to_dict(orient="records"):
                writer.write(row)
        print(f"✅ Saved batch results to {output_path}")

    else:
        raise ValueError(f"Unsupported output format: {output_path}")
