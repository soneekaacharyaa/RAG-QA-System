import time
from generate_answers import load_system, generate_answer

test_cases = [
    ("Who directed The Shawshank Redemption?", "Frank Darabont"),
    ("When was The Godfather released?", "1972"),
    ("Who starred in The Dark Knight?", ["Christian Bale", "Heath Ledger"]),
    ("What is the runtime of The Shawshank Redemption?", None),
    ("Who won Best Picture in 2023?", None),
    ("What's the budget of Avatar?", None)
]

def simple_evaluation(test_cases):
    print("Starting Evaluation")    
    index, processed_data, embedding_model, openai_client = load_system()
    
    correct = 0
    correct_dont_know = 0
    total = len(test_cases)
    should_know = len([q for q in test_cases if q[1] is not None])
    
    for question, expected in test_cases:
        
        answer, context_type, _ = generate_answer(
            question,
            index,
            processed_data,
            embedding_model,
            openai_client
        )
        print(f"Q: {question}")
        print(f"A: {answer}")
        if expected is not None:
            if context_type == "local_search":
                if answer and any(exp.lower() in answer.lower() for exp in ([expected] if isinstance(expected, str) else expected)):
                    correct_should_know += 1
        else:
            if answer is None or context_type == "web_search":
                correct_dont_know += 1
    
    accuracy = correct_should_know / should_know * 100
    dont_know_accuracy = correct_dont_know / (total - should_know) * 100
    
    print("\n Evaluation Results:")
    print(f"Correct answers (should know): {correct}/{should_know} ({accuracy:.1f}%)")
    print(f"Correct 'I don't know' (shouldn't know): {correct_dont_know}/{total-should_know} ({dont_know_accuracy:.1f}%)")

if __name__ == "__main__":
    simple_evaluation(test_cases)