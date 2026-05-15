import { useState } from 'react';

function InterviewSession({ sessionData, onSubmitAnswer, onComplete }) {
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [feedback, setFeedback] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
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
        setFeedback(result.feedback);
        setAnswer('');
        
        // Auto-clear feedback after showing next question
        setTimeout(() => setFeedback(null), 5000);
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>📝 Technical Interview</h2>
      
      <div className="question-card">
        <span className="question-type">{sessionData.type}</span>
        <h3>{sessionData.question}</h3>
      </div>

      {feedback && (
        <div className={`feedback-card ${feedback.score < 6 ? 'low-score' : ''}`}>
          <div className={`score ${feedback.score < 6 ? 'low' : ''}`}>
            Score: {feedback.score}/10
          </div>
          
          {feedback.strengths && (
            <div className="feedback-section">
              <strong>✓ Strengths:</strong>
              <p>{feedback.strengths}</p>
            </div>
          )}
          
          {feedback.weaknesses && (
            <div className="feedback-section">
              <strong>⚠ Areas to Improve:</strong>
              <p>{feedback.weaknesses}</p>
            </div>
          )}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="answer">Your Answer</label>
          <textarea
            id="answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type your answer here..."
            disabled={loading}
            autoFocus
          />
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading || !answer.trim()}>
          {loading ? 'Submitting...' : 'Submit Answer'}
        </button>
      </form>
    </div>
  );
}

export default InterviewSession;
