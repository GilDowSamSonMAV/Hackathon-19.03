"""
HaMoach — Router Agent
=======================
Classifies user input into one of three specialist agents.
Returns the agent name and confidence score.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from agents.prompts import ROUTER_SYSTEM_PROMPT
from core.agent_loop import run_agent
from core.config import ROUTER_CONFIDENCE_THRESHOLD


@dataclass
class RouteResult:
    agent: str
    confidence: float
    reasoning: str


VALID_AGENTS = {"concept_explainer", "practice_generator", "exam_coach"}
DEFAULT_AGENT = "concept_explainer"


def _parse_router_response(text: str) -> RouteResult:
    """Parse the JSON response from the router LLM."""
    # Try to find JSON in the response
    for match in re.finditer(r'\{[^{}]+\}', text):
        try:
            data = json.loads(match.group())
            agent = data.get("agent", DEFAULT_AGENT)
            if agent not in VALID_AGENTS:
                agent = DEFAULT_AGENT
            return RouteResult(
                agent=agent,
                confidence=float(data.get("confidence", 0.5)),
                reasoning=data.get("reasoning", ""),
            )
        except (json.JSONDecodeError, ValueError, TypeError):
            continue

    # Fallback: couldn't parse — default to concept explainer
    return RouteResult(
        agent=DEFAULT_AGENT,
        confidence=0.3,
        reasoning="Failed to parse router response, defaulting to concept explainer",
    )


def route_query(user_input: str) -> RouteResult:
    """
    Send user input to the router agent, return the classification.

    Returns:
        RouteResult with agent name, confidence, and reasoning.
    """
    raw_response = run_agent(
        system_prompt=ROUTER_SYSTEM_PROMPT,
        user_input=user_input,
    )
    result = _parse_router_response(raw_response)

    if result.confidence < ROUTER_CONFIDENCE_THRESHOLD:
        result.reasoning = (
            f"Low confidence ({result.confidence:.2f}). "
            f"Original: {result.reasoning}"
        )

    return result
