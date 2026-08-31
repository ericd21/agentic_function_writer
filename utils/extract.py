import re


def extract_tagged_code(text: str) -> str | None:
    """Extract code wrapped in <function> tags."""
    match = re.search(r"<function>(.*?)</function>", text, re.S)
    return match.group(1).strip() if match else None