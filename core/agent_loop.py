"""
HaMoach — Generic Agent Loop
==============================
Observe → Think → Act → Return cycle.

The LLM can emit a JSON tool call: {"tool": "<name>", "query": "<arg>"}
If detected, we execute the tool, append the result, and call the LLM again.
Max 3 rounds to prevent infinite loops.
"""

from __future__ import annotations

import json
import re
from typing import Any, Callable

import ollama

from core.config import OLLAMA_MODEL

MAX_TOOL_ROUNDS = 3

ToolMap = dict[str, Callable[[str], str]]

# Matches a JSON object containing a "tool" key anywhere in the response.
_TOOL_CALL_RE = re.compile(
    r'\{\s*"tool"\s*:\s*"([^"]+)"\s*,\s*"query"\s*:\s*"([^"]*)"\s*\}',
)


def _extract_tool_call(text: str) -> tuple[str, str] | None:
    """Return (tool_name, query) if the text contains a tool-call JSON block."""
    match = _TOOL_CALL_RE.search(text)
    if match:
        return match.group(1), match.group(2)
    # Fallback: try to parse any JSON with "tool" key
    try:
        for candidate in re.finditer(r'\{[^{}]+\}', text):
            parsed = json.loads(candidate.group())
            if "tool" in parsed and "query" in parsed:
                return str(parsed["tool"]), str(parsed["query"])
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def run_agent(
    system_prompt: str,
    user_input: str,
    tools: ToolMap | None = None,
    model: str = OLLAMA_MODEL,
    num_ctx: int = 8192,
) -> str:
    """
    Run a single agent turn with optional tool calling.

    Args:
        system_prompt: The agent's system prompt.
        user_input: The user's message.
        tools: Optional dict mapping tool names to callables(query -> str).
        model: Ollama model name.
        num_ctx: Context window size.

    Returns:
        The agent's final text response (after any tool-calling rounds).
    """
    tools = tools or {}

    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    for _round in range(MAX_TOOL_ROUNDS + 1):
        response = ollama.chat(
            model=model,
            messages=messages,
            options={"num_ctx": num_ctx},
        )
        assistant_text: str = response["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_text})

        # Check for tool call
        if not tools:
            return assistant_text

        tool_call = _extract_tool_call(assistant_text)
        if tool_call is None:
            return assistant_text

        tool_name, tool_query = tool_call
        if tool_name not in tools:
            # Unknown tool — treat as final answer
            return assistant_text

        # Execute tool and feed result back
        tool_result = tools[tool_name](tool_query)
        messages.append({
            "role": "user",
            "content": f"[Tool result from '{tool_name}']:\n{tool_result}",
        })

    # Exhausted rounds — return last response
    return assistant_text
