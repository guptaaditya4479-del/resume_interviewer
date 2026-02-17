from fastapi import FastAPI, UploadFile, File
from utils import extract_text_from_pdf
from pipeline import run_pipeline
import uuid
from pydantic import BaseModel
from pipeline import evaluate_answer
from fastapi import Form 
interview_sessions = {}


interview_sessions = {}

app = FastAPI()


@app.post("/interview")
async def interview(
    resume: UploadFile = File(...),
    domain: str = Form(...)
):

    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)

    result = run_pipeline(resume_text, domain)

    print("PIPELINE RESULT:", result)   # DEBUG

    session_id = str(uuid.uuid4())

    question_list = result.get("questions", [])


    if not isinstance(question_list, list) or len(question_list) == 0:
        return {"error": "Question generation failed"}

    interview_sessions[session_id] = {
        "structured_data": result["structured_data"],
        "questions": question_list,
        "current_index": 0
    }

    first_question = question_list[0]

    return {
        "session_id": session_id,
        "question": first_question["text"],
        "type": first_question["type"]
    }


    
class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@app.post("/answer")
async def answer_question(request: AnswerRequest):

    session = interview_sessions.get(request.session_id)

    if not session:
        return {"error": "Invalid session ID"}

    questions_list = session["questions"]

    current_index = session["current_index"]

    current_question = questions_list[current_index]

    evaluation = evaluate_answer(
    current_question["text"],
    request.answer,
    session["structured_data"]
    )


    # Cross-question logic
    score = evaluation.get("score", 0)
    follow_up = evaluation.get("follow_up_question", "")

    if score < 6 and follow_up:

        return {
            "feedback": evaluation,
            "next_question": evaluation["follow_up_question"],
            "type": "cross_question"
        }

    # Move to next main question
    session["current_index"] += 1

    if session["current_index"] >= len(questions_list):
        return {
            "feedback": evaluation,
            "message": "Interview completed"
        }

    next_question = questions_list[session["current_index"]]

    return {
    "feedback": evaluation,
    "next_question": next_question["text"],
    "type": next_question["type"]
    }


