import os
import json
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

JD_DATABASE = {
    "devops": """
DevOps Engineer Responsibilities:
- Design and maintain CI/CD pipelines
- Manage Kubernetes clusters
- Use Docker for containerization
- Automate infrastructure using Terraform
- Implement monitoring using Prometheus & Grafana
- Work with AWS cloud services
- Handle system scalability and reliability
""",

    "backend": """
Backend Engineer Responsibilities:
- Build scalable REST APIs
- Design efficient database schema
- Optimize SQL queries
- Implement authentication systems
- Handle microservices architecture
- Improve backend performance
""",

    "ml": """
Machine Learning Engineer Responsibilities:
- Data preprocessing and feature engineering
- Build and train ML models
- Evaluate models using proper metrics
- Deploy ML pipelines
- Monitor model performance and drift
"""
}



def extract_structured_data(resume_text):

    prompt = f"""
Extract structured information from this resume.

Return STRICT JSON format:

{{
  "roles": [],
  "technical_skills": [],
  "tools": [],
  "achievements_with_numbers": [],
  "projects": [],
  "soft_skills": [],
  "education": []
}}

Return only valid JSON.
No explanations.

Resume:
{resume_text}
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    print("MODEL OUTPUT:", content)  # 👈 TEMP DEBUG

    if not content:
        return empty_structure()

    try:
        return json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start != -1 and end != -1 and start < end:
            try:
                cleaned = content[start:end]
                return json.loads(cleaned)
            except:
                return empty_structure()
        else:
            return empty_structure()


def empty_structure():
    return {
        "roles": [],
        "technical_skills": [],
        "tools": [],
        "achievements_with_numbers": [],
        "projects": [],
        "soft_skills": [],
        "education": []
    }







# -------- Stage 1: Resume Analysis --------
#def analyze_resume(resume_text):

    prompt = f"""
    You are a senior technical interviewer.

    Analyze the following resume and return:

    1. Candidate seniority level
    2. Top 5 strongest technical domains
    3. Short summary of major projects
    4. Areas where depth should be tested

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -------- Stage 2: Strength Prioritization --------
#def prioritize_strengths(analysis_output):

    prompt = f"""
   Based on this resume analysis:

    {analysis_output}

    Select:
    - 3 primary focus domains
    - 2 secondary domains
    Explain briefly why.
    """

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# -------- Stage 3: Question Generation --------

def generate_questions(structured_data, jd_text):

    prompt = f"""
You are a strict but realistic senior technical interviewer.

JOB DESCRIPTION:
{jd_text}

CANDIDATE RESUME:
{structured_data}

FOCUS STRATEGY:


Generate:

1. First question MUST be: "Tell me about yourself."
2. Exactly 2 JD-based questions.
3. Exactly 2 Resume-based questions.

STRICT JSON ONLY:

{{
  
  "jd_questions": ["q1","q2"],
  "resume_questions": ["q1","q2"]
}}

No explanations.
No extra keys.
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    content = content.replace("\n", " ").replace("\r", " ")

    # -------- SAFE JSON PARSING --------
    try:
        result = json.loads(content)
    except Exception:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start != -1 and end != -1 and start < end:
            cleaned = content[start:end]
            cleaned = cleaned.replace("\n", " ").replace("\r", " ")
            try:
                result = json.loads(cleaned)
            except Exception:
                result = {}
        else:
            result = {}

    # -------- BUILD QUESTION LIST --------
    questions = []

    # Intro
    questions.append({
        "type": "intro",
        "text": "Tell me about yourself."
    })

    # JD Questions
    for q in result.get("jd_questions", []):
        questions.append({
            "type": "jd",
            "text": q
        })

    # Resume Questions
    for q in result.get("resume_questions", []):
        questions.append({
            "type": "resume",
            "text": q
        })

    return questions
    



def evaluate_answer(question, answer, structured_data):

    prompt = f"""
You are a strict but realistic technical interviewer.

Question:
{question}

Candidate Answer:
{answer}

Structured Resume:
{structured_data}

Evaluate the answer.

Return STRICT JSON format:

{{
  "score": 0,
  "strengths": "",
  "weaknesses": "",
  "follow_up_question": ""
}}

Scoring Guide:
0-3  = Very weak
4-5  = Basic but incomplete
6-7  = Good understanding
8-9  = Strong answer
10   = Excellent

Rules:
- Score from 0 to 10.
- Be realistic and consistent.
- If score < 6:
    Generate ONLY ONE focused follow-up question.
    It must target the SINGLE biggest weakness.
    Do NOT create multiple sub-questions.
    Do NOT create numbered lists.
    Keep it short and conversational.
- If score >= 6:
    follow_up_question must be empty "".
- Only return valid JSON.
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    content = response.choices[0].message.content.strip()

    # 🔥 Remove problematic control characters
    content = content.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    try:
        return json.loads(content)

    except Exception:
        start = content.find("{")
        end = content.rfind("}") + 1

        if start != -1 and end != -1 and start < end:
            cleaned = content[start:end]
            cleaned = cleaned.replace("\n", " ").replace("\r", " ").replace("\t", " ")

            try:
                return json.loads(cleaned)
            except Exception:
                pass

    # 🔥 Safe fallback so server never crashes
    return {
        "score": 5,
        "strengths": "Could not fully evaluate.",
        "weaknesses": "Parsing error occurred.",
        "follow_up_question": ""
    }




# -------- MASTER PIPELINE --------
def run_pipeline(resume_text, domain):

    structured_data = extract_structured_data(resume_text)
    jd_text = JD_DATABASE.get(domain.lower(), "")


  #  analysis = analyze_resume(resume_text)
  #  priorities = prioritize_strengths(analysis)

    questions = generate_questions(structured_data,jd_text)

    return {
        "structured_data": structured_data,
        "questions": questions
    }

