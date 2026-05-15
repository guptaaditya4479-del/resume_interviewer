"""Database CRUD operations for interview management"""
import json
import logging
from sqlalchemy.orm import Session
from database import Interview, Question, Answer

logger = logging.getLogger(__name__)


def create_interview(db: Session, session_id: str, resume_text: str, domain: str, structured_data: dict, questions: list):
    """Create a new interview session in the database"""
    try:
        # Create interview record
        db_interview = Interview(
            session_id=session_id,
            resume_text=resume_text,
            domain=domain,
            structured_data=json.dumps(structured_data),
            status="in_progress",
            current_index=0
        )
        db.add(db_interview)
        db.flush()  # Get the interview ID
        
        # Create question records
        for idx, q in enumerate(questions):
            db_question = Question(
                interview_id=db_interview.id,
                question_text=q["text"],
                question_type=q["type"],
                order_index=idx
            )
            db.add(db_question)
        
        db.commit()
        db.refresh(db_interview)
        logger.info(f"Created interview session in DB: {session_id}")
        return db_interview
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating interview in DB: {e}", exc_info=True)
        raise


def get_interview_by_session_id(db: Session, session_id: str):
    """Get interview by session ID"""
    return db.query(Interview).filter(Interview.session_id == session_id).first()


def get_interview_with_questions(db: Session, session_id: str):
    """Get interview with all questions"""
    interview = get_interview_by_session_id(db, session_id)
    if interview:
        questions = db.query(Question).filter(
            Question.interview_id == interview.id
        ).order_by(Question.order_index).all()
        return interview, questions
    return None, None


def update_interview_index(db: Session, session_id: str, new_index: int):
    """Update the current question index"""
    try:
        interview = get_interview_by_session_id(db, session_id)
        if interview:
            interview.current_index = new_index
            db.commit()
            logger.info(f"Updated interview {session_id} to index {new_index}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating interview index: {e}", exc_info=True)
        return False


def complete_interview(db: Session, session_id: str):
    """Mark interview as completed"""
    try:
        interview = get_interview_by_session_id(db, session_id)
        if interview:
            interview.status = "completed"
            db.commit()
            logger.info(f"Completed interview: {session_id}")
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Error completing interview: {e}", exc_info=True)
        return False


def save_answer(db: Session, session_id: str, question_id: int, answer_text: str, evaluation: dict):
    """Save candidate answer and evaluation"""
    try:
        interview = get_interview_by_session_id(db, session_id)
        if not interview:
            return None
            
        db_answer = Answer(
            interview_id=interview.id,
            question_id=question_id,
            answer_text=answer_text,
            score=evaluation.get("score"),
            strengths=evaluation.get("strengths"),
            weaknesses=evaluation.get("weaknesses"),
            follow_up_question=evaluation.get("follow_up_question", "")
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        logger.info(f"Saved answer for question {question_id}")
        return db_answer
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving answer: {e}", exc_info=True)
        raise


def get_interview_summary(db: Session, session_id: str):
    """Get complete interview summary with all Q&A"""
    interview = get_interview_by_session_id(db, session_id)
    if not interview:
        return None
    
    questions = db.query(Question).filter(
        Question.interview_id == interview.id
    ).order_by(Question.order_index).all()
    
    answers = db.query(Answer).filter(
        Answer.interview_id == interview.id
    ).all()
    
    # Build answer mapping
    answer_map = {a.question_id: a for a in answers}
    
    # Combine questions with answers
    qa_list = []
    for q in questions:
        answer = answer_map.get(q.id)
        qa_list.append({
            "question": q.question_text,
            "type": q.question_type,
            "answer": answer.answer_text if answer else None,
            "score": answer.score if answer else None,
            "strengths": answer.strengths if answer else None,
            "weaknesses": answer.weaknesses if answer else None
        })
    
    return {
        "session_id": interview.session_id,
        "domain": interview.domain,
        "status": interview.status,
        "created_at": interview.created_at,
        "qa_pairs": qa_list
    }
