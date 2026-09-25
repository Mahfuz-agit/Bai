from app.knowledge.extract import extract_concepts, extract_claims

def test_extract_concepts():
    concepts = extract_concepts("Learning systems improve learning systems. Memory improves learning.")
    assert concepts

def test_extract_claims():
    claims = extract_claims([(1, "Memory is strengthened because retrieval improves recall over time.")])
    assert claims
