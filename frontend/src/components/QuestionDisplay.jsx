const QuestionDisplay = ({ question, questionNumber }) => {
  return (
    <div className="question-display">
      <div className="question-header">
        <span className="question-number">Question {questionNumber}</span>
      </div>
      <div className="question-content">
        <p>{question}</p>
      </div>
    </div>
  );
};

export default QuestionDisplay;
