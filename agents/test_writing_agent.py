from agentic_function_writer.utils.llm import call_llm
from agentic_function_writer.utils.extract import extract_tagged_code

def write_tests(raw_code: str) -> str:
    print("[2] Generating Unit Tests...")
    test_messages = [
        {
            "role": "system",
            "content": (
                "You are a QA Engineer. Write a Python script using 'assert' to test the function.\n"
                "Output ONLY the tests wrapped between <function> and </function>.\n"
                "Validate that exactly one <function> block is present."
            )
        },
        {"role": "user", "content": f"Here is the function:\n{raw_code}\nWrite 3 tests using 'assert'."}
    ]

    raw_tests = call_llm(test_messages)
    tests = extract_tagged_code(raw_tests)
    if tests is None:
        raise ValueError("No tests were generated")
    print("Raw test code:\n", raw_tests)
    print("Extracted test code:\n", tests)
    return tests