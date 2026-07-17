import hashlib


def generate_content_hash(text: str) -> str:
    """
    Generate SHA-256 hash for node content.
    Used for version comparison and staleness detection.
    """

    if text is None:
        text = ""

    # Normalize whitespace
    normalized_text = " ".join(text.split())

    return hashlib.sha256(
        normalized_text.encode("utf-8")
    ).hexdigest()