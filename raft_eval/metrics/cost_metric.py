# raft_eval/metrics/cost_metric.py

from raft_eval.metrics.base_metric import BaseMetric
from raft_eval.metrics.token_count import TokenCountMetric

class CostMetric(BaseMetric):
    name = "cost_metric"

    def __init__(self):
        self.token_counter = TokenCountMetric()
        self.input_cost_per_1k = 0.3  # $ per 1K tokens
        self.output_cost_per_1k = 0.88

    def evaluate_single(self, question, answer, context, gold_answer=""):
        tokens = self.token_counter.evaluate_single(question,answer,context)
        input_cost = (tokens["input_tokens"] / 1000) * self.input_cost_per_1k
        output_cost = (tokens["output_tokens"] / 1000) * self.output_cost_per_1k
        total_cost = input_cost + output_cost
        return {
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(total_cost, 4)
        }
