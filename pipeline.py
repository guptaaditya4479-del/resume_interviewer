import os
import json
from openai import OpenAI
from config import Config
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO if Config.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=Config.OPENROUTER_API_KEY,
    base_url=Config.OPENAI_BASE_URL
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
    logger.info("Starting structured data extraction from resume")
    
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

    try:
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        content = response.choices[0].message.content.strip()
        logger.debug(f"Model response for structured data: {content[:100]}...")
        
        if not content:
            logger.warning("Empty response from model")
            return empty_structure()
        
        try:
            result = json.loads(content)
            logger.info("Successfully parsed structured data")
            return result
        except Exception as e:
            logger.warning(f"JSON parse failed, attempting cleanup: {e}")
            start = content.find("{")
            end = content.rfind("}") + 1
            
            if start != -1 and end != -1 and start < end:
                try:
                    cleaned = content[start:end]
                    result = json.loads(cleaned)
                    logger.info("Successfully parsed cleaned JSON")
                    return result
                except Exception as e2:
                    logger.error(f"Failed to parse cleaned JSON: {e2}")
                    return empty_structure()
            else:
                logger.error("Could not find valid JSON structure")
                return empty_structure()
    except Exception as e:
        logger.error(f"Error in extract_structured_data: {e}", exc_info=True)
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
    logger.info("Generating interview questions")
    
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

    try:
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("\n", " ").replace("\r", " ")
        logger.debug(f"Question generation response: {content[:100]}...")

        # -------- SAFE JSON PARSING --------
        try:
            result = json.loads(content)
        except Exception as e:
            logger.warning(f"JSON parse failed for questions, attempting cleanup: {e}")
            start = content.find("{")
            end = content.rfind("}") + 1

            if start != -1 and end != -1 and start < end:
                cleaned = content[start:end]
                cleaned = cleaned.replace("\n", " ").replace("\r", " ")
                try:
                    result = json.loads(cleaned)
                except Exception as e2:
                    logger.error(f"Failed to parse cleaned question JSON: {e2}")
                    result = {}
            else:
                logger.error("Could not find valid JSON structure in questions")
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

        logger.info(f"Generated {len(questions)} questions total")
        return questions
        
    except Exception as e:
        logger.error(f"Error in generate_questions: {e}", exc_info=True)
        # Return at least the intro question
        return [{"type": "intro", "text": "Tell me about yourself."}]
    



def evaluate_answer(question, answer, structured_data):
    logger.info(f"Evaluating answer for question: {question[:50]}...")
    
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

    try:
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        content = response.choices[0].message.content.strip()
        content = content.replace("\n", " ").replace("\r", " ").replace("\t", " ")

        try:
            result = json.loads(content)
            logger.info(f"Answer evaluated with score: {result.get('score', 'N/A')}")
            return result

        except Exception as e:
            logger.warning(f"JSON parse failed for evaluation, attempting cleanup: {e}")
            start = content.find("{")
            end = content.rfind("}") + 1

            if start != -1 and end != -1 and start < end:
                cleaned = content[start:end]
                cleaned = cleaned.replace("\n", " ").replace("\r", " ").replace("\t", " ")

                try:
                    result = json.loads(cleaned)
                    logger.info(f"Answer evaluated (after cleanup) with score: {result.get('score', 'N/A')}")
                    return result
                except Exception as e2:
                    logger.error(f"Failed to parse cleaned evaluation JSON: {e2}")
                    pass

        # Safe fallback
        logger.warning("Returning fallback evaluation due to parsing errors")
        return {
            "score": 5,
            "strengths": "Could not fully evaluate.",
            "weaknesses": "Parsing error occurred.",
            "follow_up_question": ""
        }
        
    except Exception as e:
        logger.error(f"Error in evaluate_answer: {e}", exc_info=True)
        return {
            "score": 5,
            "strengths": "Evaluation error occurred.",
            "weaknesses": "System error during evaluation.",
            "follow_up_question": ""
        }




def run_pipeline(resume_text, domain):
    logger.info(f"Running interview pipeline for domain: {domain}")
    
    structured_data = extract_structured_data(resume_text)
    jd_text = JD_DATABASE.get(domain.lower(), "")
    
    if not jd_text:
        logger.warning(f"Unknown domain: {domain}")

    questions = generate_questions(structured_data, jd_text)

    logger.info(f"Pipeline completed successfully")
    return {
        "structured_data": structured_data,
        "questions": questions
    }

