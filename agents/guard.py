"""
HaMoach — Guard Agent
======================
Classifies user input as SAFE or BLOCKED before routing.
Layer 2 of the security defense.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from agents.prompts import GUARD_SYSTEM_PROMPT
from core.agent_loop import run_agent
from core.config import GUARD_ENABLED


@dataclass
class GuardResult:
    status: str  # "SAFE" or "BLOCKED"
    reason: str


def _parse_guard_response(text: str) -> GuardResult:
    """Parse the JSON response from the guard LLM."""
    for match in re.finditer(r'\{[^{}]+\}', text):
        try:
            data = json.loads(match.group())
            status = data.get("status", "").upper()
            if status in ("SAFE", "BLOCKED"):
                return GuardResult(
                    status=status,
                    reason=data.get("reason", ""),
                )
        except (json.JSONDecodeError, ValueError, TypeError):
            continue

    # Fallback: if we can't parse, allow through (fail open for usability)
    return GuardResult(status="SAFE", reason="Guard response unparseable — defaulting to SAFE")


def check_input(user_input: str) -> GuardResult:
    """
    Classify user input as SAFE or BLOCKED.

    Returns:
        GuardResult with status and reason.
    """
    if not GUARD_ENABLED:
        return GuardResult(status="SAFE", reason="Guard disabled")

    raw_response = run_agent(
        system_prompt=GUARD_SYSTEM_PROMPT,
        user_input=user_input,
    )
    return _parse_guard_response(raw_response)
