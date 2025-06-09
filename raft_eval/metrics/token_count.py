# raft_eval/metrics/token_count.py

from raft_eval.metrics.base_metric import BaseMetric

class TokenCountMetric(BaseMetric):
    name = "token_count"

    def evaluate_single(self, question, answer, context, gold_answer=""):
        input_tokens = len(question.split()) + len(context.split())
        output_tokens = len(answer.split())
        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens
        }
