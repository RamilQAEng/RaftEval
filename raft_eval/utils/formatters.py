# raft_eval/utils/formatters.py

def format_score(score):
    """
    Formats metric scores for readability:
    - rounds floats to 4 decimal places
    - rounds floats inside dicts
    - returns other types as is
    """
    if isinstance(score, float):
        return round(score, 4)
    elif isinstance(score, dict):
        return {k: round(v, 4) if isinstance(v, float) else v for k, v in score.items()}
    elif isinstance(score, list):
        return [round(v, 4) if isinstance(v, float) else v for v in score]
    else:
        return score
