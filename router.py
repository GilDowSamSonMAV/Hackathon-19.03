import json
from core.agent_loop import run_agent
from core.config import GEMINI_MODEL

# =============================================================================
# ROUTER AGENT
# =============================================================================

ROUTER_SYSTEM_PROMPT = """You are a query router for a university study assistant. Your ONLY job is to classify the user's message into exactly one category.

<categories>
concept — The user wants something EXPLAINED. Keywords: "what is", "explain", "how does", "compare", "describe", "define", "difference between"
practice — The user wants PRACTICE QUESTIONS generated. Keywords: "practice", "questions", "quiz me", "create questions", "practice exam", "test me on", "give me problems"
exam — The user wants an INTERACTIVE EXAM simulation. Keywords: "quiz me", "test my understanding", "oral exam", "examine me", "assess my knowledge", "exam simulation"
</categories>

<rules>
1. Output ONLY valid JSON. No explanation. No preamble.
2. "quiz me" or "test my understanding" → exam (interactive, not static questions)
3. "give me practice questions" → practice (static questions with answers)
4. If genuinely ambiguous → concept (safest default)
</rules>

<output_format>
{"route": "concept" | "practice" | "exam", "reason": "5 words max explaining why"}
</output_format>

<examples>
User: "What is polymorphism?"
{"route": "concept", "reason": "asks for explanation"}

User: "Give me 3 practice questions about linked lists"
{"route": "practice", "reason": "requests practice questions"}

User: "Quiz me on recursion"
{"route": "exam", "reason": "wants interactive testing"}

User: "Compare merge sort vs quick sort"
{"route": "concept", "reason": "asks for comparison"}

User: "Create a practice exam on OOP"
{"route": "practice", "reason": "requests exam questions"}

User: "Test my understanding of hash tables"
{"route": "exam", "reason": "wants knowledge assessment"}

User: "How do I declare an array in Java?"
{"route": "concept", "reason": "asks how-to explanation"}
</examples>"""

def route_query(user_query: str) -> dict:
    """
    Routes a user's study query to the appropriate agent/category using Gemini.
    """
    try:
        raw_response = run_agent(
            system_prompt=ROUTER_SYSTEM_PROMPT,
            user_input=f"User Query: \"{user_query}\"",
            model_name=GEMINI_MODEL
        )
        
        # Parse the returned string into a Python dictionary
        # Find JSON block
        import re
        match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(raw_response)
        
    except Exception as e:
        print(f"Error routing query: {e}")
        return {"route": "concept", "reason": "fallback due to error"}

# =============================================================================
# EXAMPLES & TESTING
# =============================================================================
if __name__ == "__main__":
    # A list of diverse test queries to verify the routing logic
    test_queries = [
        "What is the difference between mitosis and meiosis?",
        "Give me 5 hard practice questions on linear algebra.",
        "Can we do a mock oral exam on World War II history?",
        "I am struggling to understand pointers in C.",
        "Test my understanding of the water cycle."
    ]
    
    print("Testing the Router Agent with Ollama:\n" + "-"*50)
    for query in test_queries:
        print(f"User Query : {query}")
        result = route_query(query)
        print(f"Route      : {result.get('route')}")
        print(f"Reason     : {result.get('reason')}\n")

