import os
import json
from openai import OpenAI

# =============================================================================
# PRACTICE GENERATOR AGENT
# =============================================================================

PRACTICE_GENERATOR_SYSTEM_PROMPT = """You are a Practice Question Generator for university CS students. You create practice questions based ONLY on the provided course materials.

<rules>
1. Generate questions using ONLY information from the <context> chunks. Do NOT use outside knowledge.
2. Each question MUST have a correct answer derived from the context.
3. Mix question types: multiple choice, short answer, code tracing, true/false.
4. Mix difficulty: 40% easy, 40% medium, 20% hard.
5. ALWAYS cite which document each question is based on.
6. If the context doesn't have enough material → say so and generate fewer questions.
</rules>

<question_format>
Each question must include:
- question: The question text
- type: "multiple_choice" | "short_answer" | "code_trace" | "true_false"
- difficulty: "easy" | "medium" | "hard"
- answer: The correct answer
- explanation: Why this is correct (1-2 sentences)
- source_doc: Which document this came from
</question_format>

<output_format>
Respond in valid JSON only:
{
  "agent": "practice_generator",
  "answer": "Here are your practice questions:",
  "questions": [
    {
      "question": "What is the time complexity of insertion in a linked list at the head?",
      "type": "short_answer",
      "difficulty": "easy",
      "answer": "O(1)",
      "explanation": "Inserting at the head only requires updating the head pointer.",
      "source_doc": "data_structures.md"
    }
  ],
  "sources": [{"document": "data_structures.md", "chunk_id": "chunk_XXX", "excerpt": "...", "relevance_score": 0.XX}],
  "confidence": 0.XX,
  "follow_up": "Want me to generate harder questions on this topic?"
}
</output_format>"""

def generate_practice_questions(user_query: str, context: str) -> dict:
    """
    Generates practice questions based on the provided context and user query.
    Needs the OPENAI_API_KEY environment variable set.
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Format the user message to include the context
    user_message = f"User Request: {user_query}\n\n<context>\n{context}\n</context>"
    
    # Call the LLM with JSON mode enabled
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Could be changed to a more capable model if needed
        messages=[
            {"role": "system", "content": PRACTICE_GENERATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        response_format={"type": "json_object"},
        temperature=0.2, # Low temperature to stay grounded in the provided context
    )
    
    # Parse the returned string into a Python dictionary
    result_str = response.choices[0].message.content
    try:
        return json.loads(result_str)
    except json.JSONDecodeError:
        # Fallback if the model somehow failed to output valid JSON
        return {
            "agent": "practice_generator",
            "answer": "Failed to parse generated questions.",
            "questions": [],
            "sources": [],
            "confidence": 0.0,
            "follow_up": "Would you like me to try generating the questions again?"
        }

# =============================================================================
# EXAMPLES & TESTING
# =============================================================================
if __name__ == "__main__":
    # Ensure the API key is set before running
    if not os.environ.get("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY environment variable is not set.")
        print("Please set it before running, e.g., 'set OPENAI_API_KEY=your_key_here'\n")
    else:
        # Sample context and query for testing
        test_context = """
        Document: data_structures.md
        Chunk: chunk_001
        Excerpt: A linked list is a linear data structure where elements are not stored at contiguous memory locations. The elements in a linked list are linked using pointers. Insertion at the head of a linked list takes O(1) time complexity because it only requires updating the new node's next pointer to the current head and then updating the head pointer.
        """
        test_query = "Give me practice questions about linked lists."
        
        print("Testing the Practice Generator Agent:\n" + "-"*50)
        try:
            result = generate_practice_questions(test_query, test_context)
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"API Error: {e}\n")
