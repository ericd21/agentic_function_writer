from ..utils.llm import call_llm
from ..utils.extract import extract_tagged_code

def debug_code(code: str, tests:str, error_msg: str) -> str:
    """
    Agent: Debugger
    Takes failing code + tests + error message and returns a corrected function
    extracted from <function>...</function> tags.
    """
    print("[4] Debug Code...")
    full_script = f"{code}\n\n{tests}"
    fix_messages = [
        {   
            "role": "system", 
            "content": (
                "You are a Senior Debugger."
                "Output ONLY the Python function wrapped between <function> and </function>. "
                "No explanations. Validate that exactly one <function> block is present."                                       
            )
         },
        {
            "role": "user",
            "content": (
                f"The following code failed with error '{error_msg}':\n{full_script}\n\n"
                "Fix the code and provide the full corrected version."
            )
        }
    ]

    fixed_code = call_llm(fix_messages)
    code = extract_tagged_code(fixed_code)
    if code is None:
        raise ValueError("Debugger agent did not produce a valid <function> block.")
    print("\nRevised Code Version:\n", fixed_code)
    print("\nExtracted from Tags:\n", code)
    return code