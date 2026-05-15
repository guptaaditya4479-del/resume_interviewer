const AnswerInput = ({ answer, onChange, onSubmit, loading, disabled }) => {
  const handleKeyDown = (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      onSubmit();
    }
  };

  return (
    <div className="answer-input">
      <label htmlFor="answer">Your Answer:</label>
      <textarea
        id="answer"
        value={answer}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type your answer here... (Ctrl+Enter to submit)"
        rows="10"
        disabled={disabled}
      />
      <div className="answer-footer">
        <span className="char-count">{answer.length} characters</span>
        <button
          onClick={onSubmit}
          disabled={disabled || !answer.trim()}
          className="btn-primary"
        >
          {loading ? 'Submitting...' : 'Submit Answer'}
        </button>
      </div>
    </div>
  );
};

export default AnswerInput;
