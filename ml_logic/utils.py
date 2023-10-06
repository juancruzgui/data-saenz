from params import *

def create_search_query(candidate_used, candidates):
    query = f"{candidate_used.lower()}"

    for cand in candidates:
        if cand != candidate_used.lower():
            query+= f" NOT {cand}"
    return query

def get_first_word(text):
    return text.split(' ')[0].lower()

def get_lastnames(candidates):
    candidates_lastnames = []
    for candidate in candidates:
        candidates_lastnames.append(candidate.split(' ')[-1].lower())

    return candidates_lastnames
