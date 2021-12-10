from src.utils import sanitize_phrases

def test_sanitize():
    sample = ["represent- ation model"]
    actual = ["representation model"]
    output = sanitize_phrases(sample)
    
    assert sample == output, "Output not as expected"