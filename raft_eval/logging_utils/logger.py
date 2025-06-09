import jsonlines
import pandas as pd
import os
from datetime import datetime

def save_results(results, output_path):
    if output_path.endswith(".csv"):
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False)
    elif output_path.endswith(".xlsx"):
        df = pd.DataFrame(results)
        df.to_excel(output_path, index=False)
    elif output_path.endswith(".jsonl"):
        with jsonlines.open(output_path, mode='w') as writer:
            for row in results:
                writer.write(row)
    else:
        raise ValueError(f"Unsupported output format: {output_path}")

def log_interactive_result(question, context, answer, result):
    log_path = "interactive_log.jsonl"
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "context": context,
        "answer": answer,
        "metrics": result
    }
    if not os.path.exists(log_path):
        with jsonlines.open(log_path, mode='w') as writer:
            writer.write(log_entry)
    else:
        with jsonlines.open(log_path, mode='a') as writer:
            writer.write(log_entry)
def log_batch_evaluation(results):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    log_path = os.path.join(log_dir, f"batch_evaluation_{timestamp}.jsonl")

    with jsonlines.open(log_path, mode='w') as writer:
        for row in results:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                **row
            }
            writer.write(log_entry)

    print(f"📝 Batch evaluation log saved to {log_path}")
