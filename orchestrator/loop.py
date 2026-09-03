from agentic_function_writer.agents.coding_agent import call_coding_agent
from agentic_function_writer.agents.test_writing_agent import write_tests
from agentic_function_writer.orchestrator.function_test_executor import run_tests
from agentic_function_writer.agents.refactoring_agent import refactor_code
from agentic_function_writer.agents.debugging_agent import debug_code

def run_agentic_loop(user_goal):
    """Main multi-agent workflow: 
    write code → write tests → run tests → iterate if the tests fail."""

    # set number of iterations for the test loop
    n_iter = 3

    code = call_coding_agent(user_goal)
    tests = write_tests(code)

    # if the function fails the tests, 
    # it will call a debugger agent to repair the code up to 3x
    for _ in range(n_iter):
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