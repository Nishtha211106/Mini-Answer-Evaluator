from google import genai
import json

client = genai.Client(api_key="YOUR_API_KEY_HERE")

MODEL = "gemini-2.0-flash-lite-001"

def evaluate_answer(question: str, student_answer: str, rubric: dict, leniency: int = 2) -> dict:
    
    leniency_map = {
        1: "Be very strict. Award marks only if the criterion is clearly and completely met. No benefit of doubt.",
        2: "Be balanced. Award marks if the criterion is mostly met. Give partial credit where deserved.",
        3: "Be lenient. Give benefit of doubt. Award marks if the student shows understanding even if incomplete."
    }
    
    leniency_instruction = leniency_map.get(leniency, leniency_map[2])
    
    prompt = f"""
You are an expert teacher evaluating a student's answer.

QUESTION:
{question}

STUDENT ANSWER:
{student_answer}

EVALUATION RUBRIC ({rubric['subject']}):
{rubric['criteria']}
Maximum marks: {rubric['max_marks']}

LENIENCY INSTRUCTION:
{leniency_instruction}

Evaluate based on the rubric and leniency instruction above.
Return ONLY a JSON object, nothing else:
{{
  "marks_awarded": <integer>,
  "max_marks": {rubric['max_marks']},
  "feedback": "<what student did well and what is missing>",
  "justification": "<point-by-point explanation>"
}}
"""
    response = client.models.generate_content(
        model=MODEL,
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
        model=MODEL,
        contents=prompt
    )
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)
