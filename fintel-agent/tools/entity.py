from thefuzz import fuzz

def resolve_entities(name1: str, name2: str) -> dict:
    ratio = fuzz.ratio(name1.lower(), name2.lower())
    partial = fuzz.partial_ratio(name1.lower(), name2.lower())
    token_sort = fuzz.token_sort_ratio(name1.lower(), name2.lower())
    token_set = fuzz.token_set_ratio(name1.lower(), name2.lower())

    score = max(ratio, partial, token_sort, token_set)
    match = score >= 80

    return {
        "name1": name1,
        "name2": name2,
        "match": match,
        "score": score,
        "breakdown": {
            "ratio": ratio,
            "partial_ratio": partial,
            "token_sort_ratio": token_sort,
            "token_set_ratio": token_set
        }
    }