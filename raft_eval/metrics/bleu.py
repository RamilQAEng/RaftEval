# raft_eval/metrics/bleu.py

from raft_eval.metrics.base_metric import BaseMetric
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize.toktok import ToktokTokenizer

# создаём tokenizer один раз
tokenizer = ToktokTokenizer()

class BleuMetric(BaseMetric):
    name = "bleu"

    def evaluate_single(self, question, answer, context, gold_answer=""):
        # Берём gold_answer если есть, иначе fallback на context
        reference_text = gold_answer if gold_answer else context
        reference = [tokenizer.tokenize(reference_text)]
        hypothesis = tokenizer.tokenize(answer)

        smoothie = SmoothingFunction().method4
        score = sentence_bleu(reference, hypothesis, smoothing_function=smoothie)
        return round(score, 2)
