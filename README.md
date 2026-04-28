# Mini-Answer-Evaluator
A mini answer evaluation system that uses a rubric + LLM (Gemini) to evaluate a student's answer, built as a simplified version of what is done at Evalvia.
## What It Does

Takes three inputs:
- A question
- A student's answer
- A subject-specific rubric (auto-detected)

Returns:
- Marks awarded
- Maximum marks
- Feedback
- Justification

## Project Structure
mini-answer-evaluator
─ rubrics.py       # All rubric definitions
─ retrieval.py     # Keyword-based rubric retrieval
─ evaluator.py     # Gemini API evaluation (with + without rubric)
─ main.py          # CLI entry point

## How to Run
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install google-genai

# Add your Gemini API key in evaluator.py
# Get free key from: https://aistudio.google.com

# Run
python main.py
```

## Approach
### 1. Rubric Design
Created rubrics manually based on real Class 12 marking patterns for:
- Physics (Class 12)
- Mathematics (Class 12)
- English (Class 10)
- English (Class 12)
- Chemistry (Class 12)
- Fallback (generic — handles unknown subjects)

Each rubric contains keywords for detection and criteria for marking.

### 2. Rubric Retrieval (Keyword Matching)
- Combines question + answer into one lowercase string
- Counts how many keywords from each rubric appear in that string
- Returns the rubric with the highest keyword count
- If nothing matches → uses fallback rubric
- No embeddings or AI needed — simple, fast, zero cost

### 3. Prompt Engineering
The prompt is designed carefully:
- Gives AI a role → "You are an expert teacher"
- Provides question, answer, and rubric
- Instructs AI to evaluate strictly based on rubric
- Forces structured JSON output so it can be parsed in Python

### 4. Bonus — Rubric vs No Rubric Comparison
Same answer evaluated twice:
- With rubric → strict, criterion-based, consistent
- Without rubric → lenient, judgment-based, inconsistent

This proves rubric-based evaluation is fairer and more structured.

## Prompts
# Prompt 1
For evaluation with using rubric.

You are an expert teacher evaluating a student's answer.

QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

EVALUATION RUBRIC ({rubric['subject']}):
{rubric['criteria']}
Maximum marks: {rubric['max_marks']}

Evaluate strictly based on the rubric.
Return ONLY a JSON object, nothing else:
{{
  "marks_awarded": <integer>,
  "max_marks": {rubric['max_marks']},
  "feedback": "<what student did well and what is missing>",
  "justification": "<point-by-point explanation>"
}}

# Prompt 2
For evaluation without using rubric.
You are an expert teacher evaluating a student's answer.

QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

Evaluate this answer on your own judgment without any specific rubric.
Return ONLY a JSON object in this exact format, nothing else:
{{
  "marks_awarded": <integer between 0 and 5>,
  "max_marks": 5,
  "feedback": "<what the student did well and what is missing>",
  "justification": "<point-by-point explanation of marks given or deducted>"
}}

## Improvements I Would Make

- **Better retrieval** — use sentence embeddings instead of keywords for more accurate subject detection
- **Web UI** — build a simple frontend so non-technical users can use it
- **Confidence score** — show how confident the AI is about its evaluation
- **Multi-rubric blending** — handle cross-subject questions
- **Database** — store past evaluations for review and analysis
- **Automated rubric generation** — let teachers input their own rubric

## Tech Stack

- Python 3.14
- Google Gemini API (gemini-2.5-flash)
- google-genai library
