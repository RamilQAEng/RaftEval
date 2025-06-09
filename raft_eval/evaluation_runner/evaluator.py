from raft_eval.evaluation_runner.metrics_registry import METRICS_REGISTRY
from raft_eval.logging_utils.logger import log_batch_evaluation
from raft_eval.utils.save_utils import log_batch_evaluation


class Evaluator:
    def __init__(self, metrics="all"):
        if metrics == "all":
            self.metrics = [metric_class() for metric_class in METRICS_REGISTRY.values()]
        else:
            self.metrics = [METRICS_REGISTRY[m]() for m in metrics]

    def evaluate_batch(self, questions, answers, contexts, gold_answers):
        results = []
        for q, a, c, g in zip(questions, answers, contexts, gold_answers):
            row_result = {
                "question": q,
                "answer": a,
                "context": c,
                "gold_answer": g,
            }
            for metric in self.metrics:
                score = metric.evaluate_single(q, a, c, g)

                if isinstance(score, dict):
                    for sub_name, sub_score in score.items():
                        row_result[sub_name] = sub_score
                else:
                    row_result[metric.name] = score

            results.append(row_result)

        log_batch_evaluation(results)
        return results

    def evaluate_single(self, question, answer, context, gold_answer=""):
        result = {}
        for metric in self.metrics:
            score = metric.evaluate_single(question, answer, context, gold_answer)

            if isinstance(score, dict):
                for sub_name, sub_score in score.items():
                    result[sub_name] = sub_score
            else:
                result[metric.name] = score

        return result
