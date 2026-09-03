from agentic_function_writer.orchestrator.loop import run_agentic_loop


if __name__ == "__main__":
    goal = input("What function should the agent build? ")
    result = run_agentic_loop(goal)
    print("Final code:\n", result['code'])