import os
import json
import requests
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Configuration
load_dotenv()
LOCAL_BACKEND_URL = "http://127.0.0.1:5000/ask"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

teacher_model = genai.GenerativeModel(
    model_name="gemini-2.5-pro",
    generation_config={"response_mime_type": "application/json"}
)

def get_local_answer(question):
    try:
        response = requests.post(LOCAL_BACKEND_URL, json={"question": question})
        return response.json()
    except Exception as e:
        return {"answer": f"Error: {e}", "sources_used": []}

def grade_answer(question, context, student_answer):
    prompt = f"""
    You are an expert Marimba Pedagogy Professor and Player. Grade the student's answer based strictly on the provided context.
    
    QUESTION: {question}
    CONTEXT: {context}
    STUDENT ANSWER: {student_answer}
    
    Provide a JSON response containing exactly these keys:
    {{
      "score": <float between 0.0 and 1.0, measuring factual accuracy against context>,
      "reasoning": "<string explaining exactly why they received this score>",
      "groundedness": <float between 0.0 and 1.0, where 1.0 means zero hallucinations>
    }}
    """
    
    try:
        response = teacher_model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error grading with Gemini: {e}")
        return {"score": 0.0, "reasoning": "Failed to generate grade.", "groundedness": 0.0}

# Execution
with open("eval_set.json", "r") as f:
    questions = json.load(f)

results = []
print(f"Starting Evaluation for {len(questions)} questions using Gemini 2.5 Pro...\n")

for item in questions:
    print(f"Testing Q{item['id']}: {item['question'][:50]}...")
    
    # get answer from local fine-tuned model
    local_data = get_local_answer(item['question'])
    
    # convert retrieved sources into a readable text block for Gemini
    sources = local_data.get('sources_used', [])
    context_str = "\n\n".join([str(s) for s in sources]) if isinstance(sources, list) else str(sources)
    
    # grade the answer using Gemini
    grade = grade_answer(item['question'], context_str, local_data.get('answer', ''))
    
    results.append({
        "question": item['question'],
        "student_answer": local_data.get('answer', ''),
        "score": grade.get('score', 0.0),
        "groundedness": grade.get('groundedness', 0.0),
        "reasoning": grade.get('reasoning', '')
    })
    
    time.sleep(1) 

# Final Report
avg_score = sum(r['score'] for r in results) / len(results) if results else 0
avg_groundedness = sum(r['groundedness'] for r in results) / len(results) if results else 0

print("\n" + "="*30)
print("       FINAL REPORT        ")
print("="*30)
print(f"Average Accuracy Score:   {avg_score:.2%}")
print(f"Average Groundedness:     {avg_groundedness:.2%}")
print("="*30)

with open("eval_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Evaluation complete! Detailed report saved to eval_results.json.")