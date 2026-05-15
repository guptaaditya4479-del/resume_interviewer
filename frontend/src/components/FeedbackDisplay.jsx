const FeedbackDisplay = ({ feedback }) => {
  const getScoreColor = (score) => {
    if (score >= 8) return 'score-high';
    if (score >= 6) return 'score-medium';
    return 'score-low';
  };

  const getScoreLabel = (score) => {
    if (score >= 8) return 'Excellent';
    if (score >= 6) return 'Good';
    if (score >= 4) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="feedback-display">
      <h3>Feedback</h3>
      
      <div className="scores-container">
        <div className="score-item">
          <span className="score-label">Relevance</span>
          <span className={`score-value ${getScoreColor(feedback.relevance_score)}`}>
            {feedback.relevance_score}/10
          </span>
          <span className="score-description">
            {getScoreLabel(feedback.relevance_score)}
          </span>
        </div>

        <div className="score-item">
          <span className="score-label">Depth</span>
          <span className={`score-value ${getScoreColor(feedback.depth_score)}`}>
            {feedback.depth_score}/10
          </span>
          <span className="score-description">
            {getScoreLabel(feedback.depth_score)}
          </span>
        </div>

        <div className="score-item">
          <span className="score-label">Accuracy</span>
          <span className={`score-value ${getScoreColor(feedback.accuracy_score)}`}>
            {feedback.accuracy_score}/10
          </span>
          <span className="score-description">
            {getScoreLabel(feedback.accuracy_score)}
          </span>
        </div>
      </div>

      <div className="feedback-text">
        <h4>Detailed Feedback:</h4>
        <p>{feedback.feedback}</p>
      </div>
    </div>
  );
};

export default FeedbackDisplay;
