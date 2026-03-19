import os
import json
import ollama
from test_cases import TEST_QUESTIONS
from router import route_query
from guard_agent import check_security
from practice_generator import generate_practice_questions
from context_injection import build_agent_prompt
from exam_coach import EXAM_COACH_SYSTEM_PROMPT

# Read all docs
DOCS = {}
for doc_name in ["intro_to_oop.md", "data_structures.md", "recursion.md", "sorting_algorithms.md", "java_basics.md"]:
    try:
        with open(os.path.join("docs", doc_name), "r", encoding="utf-8") as f:
            DOCS[doc_name] = f.read()
    except Exception as e:
        print(f"Could not read {doc_name}: {e}")

CONCEPT_SYSTEM_PROMPT = """You are a Concept Explainer. Explain concepts using ONLY the provided context.
If the provided context does not contain enough information to answer the question, say exactly "not enough info".
Always cite the source document.
Output valid JSON only with 'agent': 'concept', 'answer': 'your explanation', 'sources': ['doc_name']."""

def get_context(expected_doc):
    if expected_doc and expected_doc in DOCS:
        return [{"document": expected_doc, "chunk_id": "full_doc", "text": DOCS[expected_doc], "score": 1.0}]
    return []

def run_test(test):
    print(f"\n{'='*60}")
    print(f"Test {test['id']}: {test['input']}")
    print(f"{'='*60}")
    
    # 1. Guard Agent
    security = check_security(test['input'])
    if security.get("status") == "BLOCKED":
        print(f"BLOCKED by Guard: {security.get('reason')}")
        return
        
    # 2. Router
    route_res = route_query(test['input'])
    route = route_res.get("route")
    print(f"Routed to: {route} (Expected: {test['expected_agent']})")
    
    # 3. Context Retrieval (Mocked using expected_doc for simplicity as instructed by the test structure)
    context_chunks = get_context(test['expected_doc'])
    context_text = "\n".join([f"Document: {c['document']}\n{c['text']}" for c in context_chunks])
    if not context_chunks and test['should_refuse']:
         context_text = "No relevant context found."
    
    # 4. Agent Execution
    try:
        if route == "concept":
            messages = build_agent_prompt(CONCEPT_SYSTEM_PROMPT, test['input'], context_chunks)
            response = ollama.chat(model="qwen2.5:14b", messages=messages, format="json", options={"temperature": 0.0})
            print(f"Concept Explainer Output:\n{response['message']['content']}")
        elif route == "practice":
            res = generate_practice_questions(test['input'], context_text)
            print(f"Practice Generator Output:\n{json.dumps(res, indent=2)}")
        elif route == "exam":
            # First turn of exam coach
            user_message = f"<context>\n{context_text}\n</context>\n\n<question>\n{test['input']}\n</question>"
            response = ollama.chat(
                model="qwen2.5:14b", 
                messages=[
                    {"role": "system", "content": EXAM_COACH_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ], 
                format="json", 
                options={"temperature": 0.2}
            )
            print(f"Exam Coach Output:\n{response['message']['content']}")
        else:
            print(f"Unknown route: {route}")
    except Exception as e:
        print(f"Error during agent execution: {e}")

if __name__ == "__main__":
    for test in TEST_QUESTIONS:
        run_test(test)
