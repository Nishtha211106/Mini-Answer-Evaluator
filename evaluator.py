from google import genai
import json

client = genai.Client(api_key="YOUR_GEMINI_API_KEY_HERE")

def evaluate_answer(question: str, student_answer: str, rubric: dict) -> dict:
    prompt = f"""
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
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)

def evaluate_without_rubric(question: str, student_answer: str) -> dict:
    prompt = f"""
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
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)