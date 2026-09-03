def run_tests(code: str, tests: str) -> tuple[bool, str | None]:
    print("[3] Executing and Verifying...")

    full_script = f"{code}\n\n{tests}"
    namespace = {}
    try:
        exec(full_script, namespace)
        print("\nAll tests passed!")
        return True, None
    except Exception as e:
        print(f"\nTests failed with error: {e}")
        return False, str(e)