from ..utils.llm import call_llm
from ..utils.extract import extract_tagged_code
# coding agent
def call_coding_agent(user_goal: str) -> str:
    """
    Agent: Code Writer
    Takes a natural-language specification and returns a Python function
    extracted from <function>...</function> tags.
    """
    print(f"\n[1] Writing code for: {user_goal}")

    coding_messages = [
        {
            "role": "system",
            "content": (
                "You are a Python Expert. "
                "Output ONLY the Python function wrapped between <function> and </function>. "
                "No explanations. Validate that exactly one <function> block is present."
            )
        },
        {"role": "user", "content": f"Write a Python function for: {user_goal}"}
    ]

    raw_code = call_llm(coding_messages)
    code = extract_tagged_code(raw_code)
    if code is None:
        raise ValueError("No <function> block found")
    print("Code Generated.")
    print("Raw code:\n", raw_code)
    print("Extracted from tags:\n", code)
    return code