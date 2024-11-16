import re


def is_numeric(text: str) -> bool:
    pattern = r'^\d+$'
    return bool(re.match(pattern, text))
