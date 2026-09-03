from agentic_function_writer.utils.llm import call_llm
from agentic_function_writer.utils.extract import extract_tagged_code


def refactor_code(code: str) -> str:
    """Ask the LLM to refactor the code for readability and efficiency."""
    print("\n[5] Refactoring for Performance and Style...")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Senior Python Developer. \n"
                "Output ONLY the Python function wrapped between <function> and </function>. \n"
                "No explanations. Validate that exactly one <function> block is present."
            )
        },
        {
            "role": "user",
            "content": f"Refactor this code for efficiency and readability:\n{code}"
        }
    ]

    refined_code = call_llm(messages)
    code = extract_tagged_code(refined_code)
    if code is None:
        print('Refined code:\n', refined_code)
        raise ValueError('No code was returned by the extract_tagged_code fn after refactor ')
    print("Raw, refined code:\n", refined_code)
    print("Extracted from tags:\n", code)
    return refined_code