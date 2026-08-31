from ..agents.coder import call_coding_agent
from ..agents.tester import write_tests
from ..orchestrator import run_tests
from ..agents.refactor import refactor_code
from ..agents.debugger import debug_code

def run_agentic_loop(user_goal):
    """Main multi-agent workflow: code → tests → execution → refinement."""
    n_iter = 0

    code = call_coding_agent(user_goal)
    tests = write_tests(code)

    # if the function fails the tests, 
    # it will call a debugger agent to repair the code up to 3x
    while n_iter<3:
        n_iter +=1
        passed, error_msg = run_tests(code, tests)
        if not passed:
            code = debug_code(code, tests, error_msg)
            continue
        break
    else:
        print('After 3 revisions, the code has not passed all tests')
        return {
            "code": code,
            "iterations": n_iter,
            "tests": tests,
            "passed": passed
        }

    # optional final pass to clean up the code. Not recommended for small local llm
    final_version = refactor_code(code)
    return {
                "code": final_version,
                "iterations": n_iter,
                "tests": tests,
                "passed": passed
            }