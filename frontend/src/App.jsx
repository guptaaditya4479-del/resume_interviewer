import { useState } from 'react';
import LandingPage from './components/LandingPage';
import InterviewSession from './components/InterviewSession';
import CompletionSummary from './components/CompletionSummary';
import { startInterview, submitAnswer } from './services/api';
import './index.css';

function App() {
  const [stage, setStage] = useState('landing'); // landing, interview, completed
  const [sessionData, setSessionData] = useState(null);

  const handleStartInterview = async (resumeFile, domain) => {
    const result = await startInterview(resumeFile, domain);
    setSessionData(result);
    setStage('interview');
  };

  const handleSubmitAnswer = async (answer) => {
    const result = await submitAnswer(sessionData.session_id, answer);
    
    if (result.message === 'Interview completed') {
      setStage('completed');
      return result;
    }
    
    // Update with next question
    setSessionData({
      ...sessionData,
      question: result.next_question,
      type: result.type
    });
    
    return result;
  };

  const handleRestart = () => {
    setStage('landing');
    setSessionData(null);
  };

  return (
    <>
      {stage === 'landing' && (
        <LandingPage onStartInterview={handleStartInterview} />
      )}
      
      {stage === 'interview' && sessionData && (
        <InterviewSession
          sessionData={sessionData}
          onSubmitAnswer={handleSubmitAnswer}
          onComplete={() => setStage('completed')}
        />
      )}
      
      {stage === 'completed' && sessionData && (
        <CompletionSummary
          sessionId={sessionData.session_id}
          onRestart={handleRestart}
        />
      )}
    </>
  );
}

export default App;
