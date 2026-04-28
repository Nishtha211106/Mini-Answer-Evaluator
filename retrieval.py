from rubrics import RUBRICS

def retrieve_rubric(question: str, answer: str) -> dict:
    combined_text = (question + " " + answer).lower()
    
    best_match = None
    best_score = 0
    fallback = None

    for rubric in RUBRICS:
        if rubric["id"] == "fallback":
            fallback = rubric
            continue
        
        score = sum(1 for kw in rubric["keywords"] if kw in combined_text)
        
        if score > best_score:
            best_score = score
            best_match = rubric

    return best_match if best_match else fallback