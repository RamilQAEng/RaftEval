# raft_eval/metrics/faithfulness.py

from raft_eval.metrics.base_metric import BaseMetric
from raft_eval.utils.prompts import build_prompt_for_metric
from raft_eval.utils.llm_client import call_llm
from raft_eval.utils.formatters import format_score

class FaithfulnessMetric(BaseMetric):
    name = "faithfulness"

    def evaluate_single(self, question, answer, context, gold_answer=""):
        prompt = build_prompt_for_metric("faithfulness", question,answer,context)
        llm_response = call_llm(prompt)
        score = llm_response.get("score", 0.0)
        return format_score(score)
