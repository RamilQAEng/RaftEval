# raft_eval/metrics/base_metric.py

from abc import ABC, abstractmethod

class BaseMetric(ABC):
    name = "base_metric"

    @abstractmethod
    def evaluate_single(self, question, answer, context, gold_answer=""):
        """
        Evaluate a single example.
        Should return a scalar score or dictionary of scores.
        """
        pass

    def evaluate_batch(self, question, answer, context, gold_answer=None):
        results = []
        if gold_answer is None:
            gold_answer = [""] * len(question)  # fallback

        for q, a, c, g in zip(question, answer, context, gold_answer):
            result = self.evaluate_single(q, a, c, g)
            results.append(result)
        return results
