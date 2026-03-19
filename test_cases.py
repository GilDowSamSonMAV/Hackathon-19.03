# =============================================================================
# TEST QUESTIONS (10 scenarios from the brief)
# =============================================================================

TEST_QUESTIONS = [
    {"id": 1,  "input": "What is polymorphism?",                                    "expected_agent": "concept",  "expected_doc": "intro_to_oop.md",      "should_refuse": False},
    {"id": 2,  "input": "Give me 3 practice questions about linked lists",           "expected_agent": "practice", "expected_doc": "data_structures.md",   "should_refuse": False},
    {"id": 3,  "input": "Quiz me on recursion",                                     "expected_agent": "exam",     "expected_doc": "recursion.md",         "should_refuse": False},
    {"id": 4,  "input": "Compare merge sort vs quick sort",                          "expected_agent": "concept",  "expected_doc": "sorting_algorithms.md","should_refuse": False},
    {"id": 5,  "input": "Create a practice exam on OOP",                             "expected_agent": "practice", "expected_doc": "intro_to_oop.md",      "should_refuse": False},
    {"id": 6,  "input": "What is the time complexity of binary search?",             "expected_agent": "concept",  "expected_doc": None,                   "should_refuse": True},  # NOT in docs
    {"id": 7,  "input": "Explain the call stack in recursion with an example",       "expected_agent": "concept",  "expected_doc": "recursion.md",         "should_refuse": False},
    {"id": 8,  "input": "Test my understanding of hash tables",                      "expected_agent": "exam",     "expected_doc": "data_structures.md",   "should_refuse": False},
    {"id": 9,  "input": "How do I declare an array in Java?",                        "expected_agent": "concept",  "expected_doc": "java_basics.md",       "should_refuse": False},
    {"id": 10, "input": "What did the professor say about the midterm?",             "expected_agent": "concept",  "expected_doc": None,                   "should_refuse": True},  # NOT in docs
]
