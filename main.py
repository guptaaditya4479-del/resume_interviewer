from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from utils import extract_text_from_pdf
from pipeline import run_pipeline
import uuid
from pydantic import BaseModel
from pipeline import evaluate_answer
from fastapi import Form
import logging
from config import Config
from database import init_db, get_db, Interview, Question
from db_operations import (
    create_interview, 
    get_interview_by_session_id, 
    get_interview_with_questions,
    update_interview_index, 
    complete_interview, 
    save_answer,
    get_interview_summary
)
import json

# Set up logging
logging.basicConfig(
    level=logging.INFO if Config.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database on startup
init_db()

app = FastAPI(
    title="Resume Interviewer API",
    description="AI-powered technical interview system",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "resume-interviewer",
        "version": "1.0.0"
    }


# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal server error",
        "status_code": 500
    }


@app.post("/interview")
async def interview(
    resume: UploadFile = File(...),
    domain: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"New interview request - domain: {domain}, file: {resume.filename}")
    
    # Validate file type
    if not resume.filename.endswith('.pdf'):
        logger.warning(f"Invalid file type: {resume.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        resume_bytes = await resume.read()
        
        # Validate file size (e.g., max 10MB)
        if len(resume_bytes) > 10 * 1024 * 1024:
            logger.warning(f"File too large: {len(resume_bytes)} bytes")
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        resume_text = extract_text_from_pdf(resume_bytes)
        
        if not resume_text.strip():
            logger.error("Extracted empty text from PDF")
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        result = run_pipeline(resume_text, domain)

        session_id = str(uuid.uuid4())
        question_list = result.get("questions", [])

        if not isinstance(question_list, list) or len(question_list) == 0:
            logger.error("Question generation failed")
            raise HTTPException(status_code=500, detail="Question generation failed")

        # Save to database instead of in-memory
        create_interview(
            db=db,
            session_id=session_id,
            resume_text=resume_text,
            domain=domain,
            structured_data=result["structured_data"],
            questions=question_list
        )

        first_question = question_list[0]
        
        logger.info(f"Interview session created: {session_id}")
        return {
            "session_id": session_id,
            "question": first_question["text"],
            "type": first_question["type"]
        }
        
    except ValueError as e:
        logger.error(f"ValueError in interview endpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in interview endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


    
class AnswerRequest(BaseModel):
    session_id: str
    answer: str

@app.post("/answer")
async def answer_question(request: AnswerRequest, db: Session = Depends(get_db)):
    logger.info(f"Answer received for session: {request.session_id}")
    
    # Get interview and questions from database
    interview, questions_list = get_interview_with_questions(db, request.session_id)

    if not interview:
        logger.warning(f"Invalid session ID: {request.session_id}")
        raise HTTPException(status_code=404, detail="Invalid session ID")

    current_index = interview.current_index
    
    if current_index >= len(questions_list):
        logger.warning(f"Interview already completed: {request.session_id}")
        raise HTTPException(status_code=400, detail="Interview already completed")
    
    current_question = questions_list[current_index]
    
    # Parse structured data from JSON
    structured_data = json.loads(interview.structured_data)

    try:
        evaluation = evaluate_answer(
            current_question.question_text,
            request.answer,
            structured_data
        )
        
        # Save the answer to database
        save_answer(
            db=db,
            session_id=request.session_id,
            question_id=current_question.id,
            answer_text=request.answer,
            evaluation=evaluation
        )

        # Cross-question logic
        score = evaluation.get("score", 0)
        follow_up = evaluation.get("follow_up_question", "")

        if score < 6 and follow_up:
            logger.info(f"Score {score} - generating follow-up question")
            return {
                "feedback": evaluation,
                "next_question": evaluation["follow_up_question"],
                "type": "cross_question"
            }

        # Move to next main question
        new_index = current_index + 1
        update_interview_index(db, request.session_id, new_index)

        if new_index >= len(questions_list):
            complete_interview(db, request.session_id)
            logger.info(f"Interview completed for session: {request.session_id}")
            return {
                "feedback": evaluation,
                "message": "Interview completed"
            }

        next_question = questions_list[new_index]

        return {
            "feedback": evaluation,
            "next_question": next_question.question_text,
            "type": next_question.question_type
        }
        
    except Exception as e:
        logger.error(f"Error in answer evaluation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error evaluating answer")


@app.get("/interview/{session_id}/summary")
async def get_summary(session_id: str, db: Session = Depends(get_db)):
    """Get complete interview summary with all Q&A pairs"""
    logger.info(f"Getting summary for session: {session_id}")
    
    summary = get_interview_summary(db, session_id)
    
    if not summary:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(status_code=404, detail="Session not found")
    
    return summary



