from retrieval import retrieve_rubric
from evaluator import evaluate_answer, evaluate_without_rubric
import time

def print_result(result: dict):
    print(f"  Marks Awarded : {result['marks_awarded']} / {result['max_marks']}")
    print(f"  Feedback      : {result['feedback']}")
    print(f"  Justification : {result['justification']}")

def get_leniency() -> int:
    print("Select leniency level:")
    print("  1 → Strict")
    print("  2 → Normal (default)")
    print("  3 → Lenient")
    choice = input("> ").strip()
    if choice in ["1", "2", "3"]:
        return int(choice)
    print("Invalid choice, using Normal (2)\n")
    return 2

def main():
    print("=== Mini Answer Evaluator ===\n")

    question = input("Enter the question:\n> ").strip()
    print()
    student_answer = input("Enter the student's answer:\n> ").strip()
    print()

    leniency = get_leniency()
    print()

    leniency_labels = {1: "Strict", 2: "Normal", 3: "Lenient"}
    print(f"📏 Leniency: {leniency_labels[leniency]}\n")

    # Step 1: Retrieve rubric
    rubric = retrieve_rubric(question, student_answer)
    print(f"📋 Retrieved Rubric: {rubric['subject']}")
    print(f"Criteria:{rubric['criteria']}\n")

    # Step 2: Evaluate WITH rubric
    print("⏳ Evaluating WITH rubric...\n")
    result_with = evaluate_answer(question, student_answer, rubric, leniency)

    # Step 3: Evaluate WITHOUT rubric
    time.sleep(10)
    print("⏳ Evaluating WITHOUT rubric...\n")
    result_without = evaluate_without_rubric(question, student_answer)

    # Step 4: Display comparison
    print("=" * 50)
    print(f"✅ EVALUATION WITH RUBRIC ({leniency_labels[leniency]}):")
    print("=" * 50)
    print_result(result_with)

    print()
    print("=" * 50)
    print("❌ EVALUATION WITHOUT RUBRIC:")
    print("=" * 50)
    print_result(result_without)

    print()
    print("=" * 50)
    print("📊 COMPARISON SUMMARY:")
    print("=" * 50)
    diff = result_with['marks_awarded'] - result_without['marks_awarded']
    if diff > 0:
        print(f"  Rubric gave {diff} more mark(s) — more structured evaluation")
    elif diff < 0:
        print(f"  Without rubric gave {abs(diff)} more mark(s) — more lenient evaluation")
    else:
        print(f"  Both gave same marks — but rubric gives better justification")

if __name__ == "__main__":
    main()
