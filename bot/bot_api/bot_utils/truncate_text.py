def truncate_text(text: str, max_length: int = 20) -> str:
    return text[:max_length] + '...' if len(text) > max_length else text
