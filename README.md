# Agentic Function Writer

A lightweight multi‑agent system that generates Python functions, writes simple tests, executes them, debugs failures, and optionally refactors the final code — all powered by a local LLM.

This project demonstrates clean agent boundaries, a simple orchestrator, schema‑enforced LLM output, and deterministic test execution. It is designed as an example of agentic system architecture.

This project was intentionally designed to run on a small, relatively weak local LLM so I could evaluate how smaller models behave in an agentic workflow. My initial testing used a quantized version of Mistral‑7B‑Instruct on a 6 GB GPU. The system itself works, but the model is often inconsistent in following the schema, producing valid <function> blocks, or generating correct code. Because the program prompts the user for a new goal each time it runs, you can directly explore the limitations of smaller models and observe how the agents compensate for those weaknesses. Working with constrained models forces you to think carefully about the boundaries and failure modes of LLMs, and highlights why agentic design and strict schema enforcement matter.

## 🚀 Overview
The system takes a natural‑language goal such as:

> Write a function that checks whether a number is prime.

Then it runs a full agentic workflow:

### Coding Agent  
Generates a Python function wrapped in <function>...</function> tags.

### Test Writing Agent  
Writes three assert‑based unit tests, also wrapped in <function> tags.

### Function Test Executor  
Executes the function + tests using exec() and reports pass/fail.

### Debugging Agent  
If tests fail, the debugger fixes the code and returns a corrected version.

### Refactoring Agent (optional)  
Cleans up the final code for readability and efficiency.

### Orchestration Loop
Coordinates the entire workflow and handles retry logic.

This produces a fully working, tested, and optionally refactored Python function.

## 🧠 Architecture
```
agentic-function-writer/
│
├── main.py
│
├── orchestrator/
│   ├── loop.py
|   └── function_test_executor.py
│
├── agents/
│   ├── coding_agent.py
│   ├── test_writing_agent.py
│   ├── debugging_agent.py
│   └── refactoring_agent.py
│
├── utils/
│   ├── llm.py
│   └── extract.py
│
└── README.md
```

## Agents
Each agent performs one capability:
| Agent | Responsibility |
| --- | --- |
| **Coding** | Generates the initial Python function |
| **Testing** | Writes assert‑based unit tests |
| **Debugging** | Fixes failing code using error messages |
| **Refactoring** | Improves readability and efficiency |


All agents enforce a strict schema:
**LLM output must contain exactly one** \<function\>...\</function\> block.**

## Utils
Small, deterministic utilities:
- llm.py — local LLM adapter
- extract.py — extracts code from <function> tags

## Orchestrator
The orchestrator coordinates the entire workflow:
- loop.py 
  - calls coding and test writing agents 
  - runs tests
  - debug and iterate if needed

- runner.py 
  — executes code + tests and returns pass/fail

## 🔁 Agentic Loop
The orchestrator implements:

```Python
code = call_coding_agent(goal)
tests = write_tests(code)

for _ in range(n_iter):
    passed, error = run_tests(code, tests)
    if passed:
        break
    code = debug_code(code, tests, error)

# optional. Not recommended with weak models.
final_version = refactor_code(code)
```
This loop is intentionally simple and readable — perfect for demonstrating agentic system design.

## 🧪 Test Execution
Tests are executed using:

```Python
exec(code + "\n\n" + tests, {})
```
The runner returns:
- `True, None` if all tests pass
- `False, error_message` if any test fails

This error message is fed directly into the debugger agent.

## 🏗️ LLM Requirements
This project uses a local inference server compatible with the OpenAI chat completions API. I used llama.cpp with a quantized version of Mistral 7b instruct downloaded from HuggingFace. I chose llama.cpp because it provides fast, lightweight local inference and exposes an OpenAI‑compatible API, making it ideal for testing weak‑LLM agent behavior.

- llama.cpp -- https://github.com/ggml-org/llama.cpp
- Mistral 7B Instruct (quantized gguf) -- https://huggingface.co/itlwas/Mistral-7B-Instruct-v0.1-Q4_K_M-GGUF

Example configuration in utils\llm.py:

```Python
API_URL = "http://localhost:8080/v1/chat/completions"
MODEL = "mistral-7b-instruct-v0.1.Q4_K_M"
```
Any model that supports chat messages and returns:

```json
{
  "choices": [
    { "message": { "content": "..." } }
  ]
}
```
will work.

## ▶️ Running the Program
From the the folder above the project root:

```bash
python -m agentic_function_writer.main
```
You will be prompted:
```Code
What function should the agent build?
```
Enter a natural‑language description, such as:
```Code
Write a function that returns the nth Fibonacci number.
```
The system will:
- generate code
- generate tests
- run tests
- debug failures
- refactor the final version
- print the results

## 🎯 Design Goals
This project is intentionally built to demonstrate:
- clean agent boundaries
- schema‑enforced LLM output
- deterministic test execution
- minimal orchestrator logic
- modular architecture
- weak‑model robustness
- readability and clarity

It is not meant to be production‑ready — it is meant to be educational.

📄 License
MIT License 