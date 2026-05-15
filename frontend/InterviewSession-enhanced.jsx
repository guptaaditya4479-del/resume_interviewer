// ENHANCED VERSION: InterviewSession with sub-components
// This version uses QuestionDisplay, AnswerInput, and FeedbackDisplay components
// 
// To use: Replace src/components/InterviewSession.jsx with this file

import { useState } from 'react';
import QuestionDisplay from './QuestionDisplay';
import AnswerInput from './AnswerInput';
import FeedbackDisplay from './FeedbackDisplay';

function InterviewSession({ sessionData, onSubmitAnswer, onComplete }) {
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [questionNumber, setQuestionNumber] = useState(1);

  const handleSubmit = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await onSubmitAnswer(answer);
      
      if (result.message === 'Interview completed') {
        onComplete();
      } else {
        // Show feedback with scores
        setFeedback({
          relevance_score: result.relevance_score || 0,
          depth_score: result.depth_score || 0,
          accuracy_score: result.accuracy_score || 0,
          feedback: result.feedback || ''
        });
        
        // Auto-clear feedback and reset for next question
        setTimeout(() => {
          setFeedback(null);
          setAnswer('');
          setQuestionNumber(prev => prev + 1);
        }, 5000);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="interview-session">
      <div className="container">
        <div className="interview-header">
          <h2>Technical Interview</h2>
          <p>Session ID: {sessionData.session_id}</p>
        </div>

        {!feedback ? (
          <>
            <QuestionDisplay 
              question={sessionData.question} 
              questionNumber={questionNumber}
            />
            <AnswerInput
              answer={answer}
              onChange={setAnswer}
              onSubmit={handleSubmit}
              loading={loading}
              disabled={loading}
            />
            {error && <div className="error-message">{error}</div>}
          </>
        ) : (
          <>
            <QuestionDisplay 
              question={sessionData.question} 
              questionNumber={questionNumber}
            />
            <div className="user-answer">
              <h3>Your Answer:</h3>
              <p>{answer}</p>
            </div>
            <FeedbackDisplay feedback={feedback} />
            <p className="next-question-info">
              Next question loading in 5 seconds...
            </p>
          </>
        )}
      </div>
    </div>
  );
}

export default InterviewSession;

/*
 * DIFFERENCES FROM ORIGINAL:
 * - Uses QuestionDisplay component for consistent question formatting
 * - Uses AnswerInput component with character counter and Ctrl+Enter support
 * - Uses FeedbackDisplay component with color-coded scores (3 metrics)
 * - Cleaner separation of concerns
 * - Better visual hierarchy
 * 
 * The original version works fine too! This is just a more modular approach.
 */
