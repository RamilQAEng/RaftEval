import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

class KnowledgeBaseRetriever:
    def __init__(self, kb_path: str, model_name: str = "all-MiniLM-L6-v2"):
        self.kb_path = kb_path
        self.df = pd.read_excel(kb_path)
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self._embed_knowledge()

    def _embed_knowledge(self):
        # Векторизация всех вопросов в БЗ
        questions = self.df['question'].fillna("").tolist()
        self.embeddings = self.model.encode(questions, convert_to_tensor=True)

    def get_relevant_context(self, question: str, top_k: int = 1) -> str:
        question_emb = self.model.encode(question, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(question_emb, self.embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        idx = top_results.indices[0].item()
        score = top_results.values[0].item()

        # Можно задать порог для релевантности, например 0.5
        if score < 0.5:
            return None

        # Возвращаем context из таблицы для наиболее релевантного вопроса
        return self.df.iloc[idx]['context'] if pd.notna(self.df.iloc[idx]['context']) else ""
