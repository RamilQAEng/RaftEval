# metrics/answer_relevancy.py

from raft_eval.metrics.base_metric import BaseMetric
from raft_eval.utils.prompts import build_prompt_for_metric
from raft_eval.utils.llm_client import call_llm
from raft_eval.utils.formatters import format_score

class StyleScoreMetric(BaseMetric):
    name = "style_score"

    def evaluate_single(self, question, answer, context, gold_answer=""):
        prompt = build_prompt_for_metric("style_score", question,answer,context)
        llm_response = call_llm(prompt)
        score = llm_response.get("score", 0.0)
        return format_score(score)
