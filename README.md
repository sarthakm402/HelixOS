# Helix OS

A local AI execution system that converts natural language into structured plans and runs them through deterministic tools. Built as a personal control plane for a single machine.

Not a chatbot. The LLM plans — a separate executor acts.

---

## How it works

```
user input → router → planner (LLM) → validator → executor → tools → result
``` 

Three layers:

**Interface** (`frontend/`) — terminal input, streamed output, /commands

**Control plane** (`core/`) — routes input, builds JSON execution plan, validates it, runs it step by step

**Services** (`services/`) — deterministic tools that do the actual work. The LLM never touches this layer directly.

The planner outputs a JSON plan:
```json
[{"tool": "filesystem", "action": "find_file", "args": {"name": "chat.py"}}]
```

Steps can reference earlier results for multi-step chains:
```json
[
  {"id": "s1", "tool": "filesystem", "action": "find_file", "args": {"name": "chat.py"}},
  {"id": "s2", "tool": "filesystem", "action": "read_file", "args": {"path": "$s1"}}
]
```

---

## Capabilities

**Filesystem**
- find, read, list, navigate (cd/pwd)
- create file/dir, delete file/dir, move file/dir
- index-based resolution — just use names, no full paths needed

**OS**
- CPU, RAM, swap, disk usage
- list running processes, filter by name
- kill process by name or PID
- run shell commands

**Memory**
- persist facts to disk across sessions
- injected into LLM context on every call
- last 10 messages of conversation history in context

**Repository Analysis**
- walks project files
- extracts AST metadata (classes, functions, imports)
- LLM summarization into structured JSON

**Reliability**
- plan validator catches bad plans before execution
- runtime errors caught per-step, never crash the loop
- human readable error messages
- startup sequence — index built, memories loaded, ollama started before first prompt

**Cross-platform**
- platform adapter layer for shell execution and disk paths
- works on Linux, Windows, Mac

---

## Stack

- Python 3.10+
- Ollama (local, gemma3:4b) — zero cloud APIs
- psutil — OS introspection
- requests — Ollama HTTP calls
- Everything else is Python stdlib

---

## Prerequisites

1. Install ollama from [ollama.ai](https://ollama.ai)
2. Pull the model:
```bash
ollama pull gemma3:4b
```

---

## Install

```bash
git clone https://github.com/yourname/HelixOS
cd HelixOS
pip install -e .
```

---

## Run

```bash
helix
```

From anywhere. Ollama starts automatically if not running.

---

## Project structure

```
HelixOS/
  frontend/
    terminal.py       — entry point, main loop
  core/
    config.py         — all constants and paths
    router.py         — routes input to commands or agent
    planner.py        — builds plan, validates, executes
    chat.py           — LLM conversation with memory context
    memory.py         — in-memory history + disk persistence
    tool_registry.py  — all tools registered here
    analyser.py       — repo analysis pipeline
    handle_system_commands.py — /commands
  services/
    llm.py            — ollama HTTP client
    ast_helper.py     — Python AST metadata extractor
    file_system.py    — find, read, ls, cd, pwd
    file_ops.py       — create, delete, move
    fs_index.py       — filesystem index with thread-safe refresh
    os_ops.py         — system stats, processes, kill
    platform/
      __init__.py     — OS detector
      linux.py        — shell + disk for Linux
      windows.py      — shell + disk for Windows
      mac.py          — shell + disk for Mac
```

---

## Why this is different from a chatbot with tools

Most LLM tool setups let the model decide and execute in one step. Helix separates planning from execution deliberately:

- The LLM outputs a JSON plan. A separate executor runs it. They never mix.
- Plans are validated before anything executes — bad plans fall back to chat, never crash.
- Multi-step dependencies are explicit in the plan via `$stepId`, not hidden in LLM reasoning.
- The LLM is one component in a deterministic system, not the system itself.

---

## What it is not
 No background tasks, no multi-agent workflows, no GUI, no plugin system.
