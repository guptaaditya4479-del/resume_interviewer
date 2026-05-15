import { useState, useEffect } from 'react';
import { getInterviewSummary } from '../services/api';

function CompletionSummary({ sessionId, onRestart }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getInterviewSummary(sessionId);
        setSummary(data);
      } catch (err) {
        setError('Failed to load interview summary');
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, [sessionId]);

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading interview summary</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">{error}</div>
        <button onClick={onRestart}>Start New Interview</button>
      </div>
    );
  }

  const averageScore = summary?.qa_pairs
    ?.filter(qa => qa.score !== null)
    ?.reduce((sum, qa) => sum + qa.score, 0) / 
    summary?.qa_pairs?.filter(qa => qa.score !== null)?.length || 0;

  return (
    <div className="container">
      <div className="completion-message">
        <h2>🎉 Interview Completed!</h2>
        <p>Thank you for completing the technical interview</p>
        {averageScore > 0 && (
          <div className="score" style={{ marginTop: '20px' }}>
            Average Score: {averageScore.toFixed(1)}/10
          </div>
        )}
      </div>

      <h3>Interview Summary</h3>
      <p><strong>Domain:</strong> {summary?.domain}</p>
      <p><strong>Status:</strong> {summary?.status}</p>

      <h3 style={{ marginTop: '30px' }}>Questions & Answers</h3>
      
      {summary?.qa_pairs?.map((qa, index) => (
        <div key={index} className="question-card" style={{ marginBottom: '20px' }}>
          <span className="question-type">{qa.type}</span>
          <h4 style={{ margin: '10px 0', color: '#555' }}>
            {index + 1}. {qa.question}
          </h4>
          
          {qa.answer && (
            <>
              <p style={{ fontStyle: 'italic', color: '#666', marginTop: '10px' }}>
                <strong>Your Answer:</strong> {qa.answer}
              </p>
              
              {qa.score !== null && (
                <div style={{ marginTop: '15px' }}>
                  <div className={`score ${qa.score < 6 ? 'low' : ''}`} style={{ fontSize: '1.3em' }}>
                    Score: {qa.score}/10
                  </div>
                  
                  {qa.strengths && (
                    <div style={{ marginTop: '10px' }}>
                      <strong style={{ color: '#48bb78' }}>✓ Strengths:</strong>
                      <p>{qa.strengths}</p>
                    </div>
                  )}
                  
                  {qa.weaknesses && (
                    <div style={{ marginTop: '10px' }}>
                      <strong style={{ color: '#fc8181' }}>⚠ Areas to Improve:</strong>
                      <p>{qa.weaknesses}</p>
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      ))}

      <div className="button-group">
        <button onClick={onRestart}>Start New Interview</button>
      </div>
    </div>
  );
}

export default CompletionSummary;
