# raft_eval/metrics/__init__.py или raft_eval/metrics/registry.py (в зависимости как у тебя названо)

from raft_eval.metrics.bleu import BleuMetric
from raft_eval.metrics.token_count import TokenCountMetric
from raft_eval.metrics.cost_metric import CostMetric
from raft_eval.metrics.faithfulness import FaithfulnessMetric
from raft_eval.metrics.answer_relevancy import AnswerRelevancyMetric
from raft_eval.metrics.coverage import CoverageMetric
from raft_eval.metrics.style_score import StyleScoreMetric
from raft_eval.metrics.geval import GevalScoreMetric


METRICS_REGISTRY = {
    "bleu": BleuMetric,
    "token_count": TokenCountMetric,
    "cost_metric": CostMetric,
    "faithfulness": FaithfulnessMetric,
    "answer_relevancy": AnswerRelevancyMetric,
    "coverage": CoverageMetric,
    "style_score": StyleScoreMetric,
    "geval":GevalScoreMetric,
}
