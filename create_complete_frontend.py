#!/usr/bin/env python3
"""
Complete React Frontend Setup Script for Resume Interviewer
This script creates the entire frontend directory structure and all necessary files.
"""

import os
import json

# Base directory
BASE_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

print("=" * 60)
print("Resume Interviewer - Frontend Setup")
print("=" * 60)

# ===== STEP 1: Create Directory Structure =====
print("\n[1/5] Creating directory structure...")
directories = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'src'),
    os.path.join(BASE_DIR, 'src', 'components'),
    os.path.join(BASE_DIR, 'src', 'services'),
    os.path.join(BASE_DIR, 'public'),
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"  ✓ {directory}")

# ===== STEP 2: Create Configuration Files =====
print("\n[2/5] Creating configuration files...")

# package.json
package_json = {
    "name": "resume-interviewer-frontend",
    "private": True,
    "version": "0.0.0",
    "type": "module",
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "axios": "^1.6.0",
        "react-router-dom": "^6.20.0"
    },
    "devDependencies": {
        "@types/react": "^18.2.43",
        "@types/react-dom": "^18.2.17",
        "@vitejs/plugin-react": "^4.2.1",
        "vite": "^5.0.8"
    }
}

with open(os.path.join(BASE_DIR, 'package.json'), 'w') as f:
    json.dump(package_json, f, indent=2)
print("  ✓ package.json")

# vite.config.js
vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, '')
      }
    }
  }
})
"""
with open(os.path.join(BASE_DIR, 'vite.config.js'), 'w') as f:
    f.write(vite_config)
print("  ✓ vite.config.js")

# index.html
index_html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Resume Interviewer</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
with open(os.path.join(BASE_DIR, 'index.html'), 'w') as f:
    f.write(index_html)
print("  ✓ index.html")

# .gitignore
gitignore = """node_modules
dist
dist-ssr
*.local
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
"""
with open(os.path.join(BASE_DIR, '.gitignore'), 'w') as f:
    f.write(gitignore)
print("  ✓ .gitignore")

# ===== STEP 3: Create API Service =====
print("\n[3/5] Creating API service...")

api_js = """import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const startInterview = async (resumeFile, domain) => {
  try {
    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('domain', domain);

    const response = await axios.post(`${API_BASE_URL}/interview`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    console.error('Start interview error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to start interview');
  }
};

export const submitAnswer = async (sessionId, answer) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/answer`, {
      session_id: sessionId,
      answer: answer
    });

    return response.data;
  } catch (error) {
    console.error('Submit answer error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to submit answer');
  }
};

export const getInterviewSummary = async (sessionId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/interview/${sessionId}/summary`
    );

    return response.data;
  } catch (error) {
    console.error('Get summary error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to get interview summary');
  }
};

export default {
  startInterview,
  submitAnswer,
  getInterviewSummary
};
"""
with open(os.path.join(BASE_DIR, 'src', 'services', 'api.js'), 'w') as f:
    f.write(api_js)
print("  ✓ src/services/api.js")

# ===== STEP 4: Create React Components =====
print("\n[4/5] Creating React components...")

# LandingPage.jsx
landing_page = """import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startInterview } from '../services/api';

const LandingPage = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [domain, setDomain] = useState('backend');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
    } else {
      setError('Please select a valid PDF file');
      setResumeFile(null);
    }
  };

  const handleStartInterview = async (e) => {
    e.preventDefault();
    
    if (!resumeFile) {
      setError('Please upload your resume');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await startInterview(resumeFile, domain);
      navigate(`/interview/${response.session_id}`, { 
        state: { question: response.question }
      });
    } catch (err) {
      setError(err.message || 'Failed to start interview. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="landing-page">
      <div className="container">
        <div className="header">
          <h1>Resume Interviewer</h1>
          <p>Upload your resume and start your technical interview</p>
        </div>

        <form onSubmit={handleStartInterview} className="upload-form">
          <div className="form-group">
            <label htmlFor="resume">Upload Resume (PDF)</label>
            <input
              type="file"
              id="resume"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={loading}
            />
            {resumeFile && (
              <p className="file-name">Selected: {resumeFile.name}</p>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="domain">Interview Domain</label>
            <select
              id="domain"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              disabled={loading}
            >
              <option value="backend">Backend Engineering</option>
              <option value="devops">DevOps</option>
              <option value="ml">Machine Learning</option>
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button 
            type="submit" 
            disabled={loading || !resumeFile}
            className="btn-primary"
          >
            {loading ? 'Starting Interview...' : 'Start Interview'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LandingPage;
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'LandingPage.jsx'), 'w') as f:
    f.write(landing_page)
print("  ✓ src/components/LandingPage.jsx")

# InterviewSession.jsx
interview_session = """import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import QuestionDisplay from './QuestionDisplay';
import AnswerInput from './AnswerInput';
import FeedbackDisplay from './FeedbackDisplay';
import { submitAnswer } from '../services/api';

const InterviewSession = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  const [currentQuestion, setCurrentQuestion] = useState(location.state?.question || '');
  const [questionNumber, setQuestionNumber] = useState(1);
  const [answer, setAnswer] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isComplete, setIsComplete] = useState(false);

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await submitAnswer(sessionId, answer);
      
      setFeedback({
        relevance_score: response.relevance_score,
        depth_score: response.depth_score,
        accuracy_score: response.accuracy_score,
        feedback: response.feedback
      });

      if (response.is_complete) {
        setIsComplete(true);
        setTimeout(() => {
          navigate(`/summary/${sessionId}`);
        }, 3000);
      } else if (response.next_question) {
        setTimeout(() => {
          setCurrentQuestion(response.next_question);
          setQuestionNumber(prev => prev + 1);
          setAnswer('');
          setFeedback(null);
        }, 5000);
      }
    } catch (err) {
      setError(err.message || 'Failed to submit answer. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleNextQuestion = () => {
    setFeedback(null);
    setAnswer('');
  };

  if (isComplete) {
    return (
      <div className="interview-session">
        <div className="container">
          <div className="completion-message">
            <h2>Interview Complete!</h2>
            <p>Redirecting to your summary...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="interview-session">
      <div className="container">
        <div className="interview-header">
          <h2>Interview Session</h2>
          <p>Session ID: {sessionId}</p>
          <p>Question {questionNumber}</p>
        </div>

        {!feedback ? (
          <>
            <QuestionDisplay 
              question={currentQuestion} 
              questionNumber={questionNumber}
            />
            <AnswerInput
              answer={answer}
              onChange={setAnswer}
              onSubmit={handleSubmitAnswer}
              loading={loading}
              disabled={loading}
            />
          </>
        ) : (
          <>
            <QuestionDisplay 
              question={currentQuestion} 
              questionNumber={questionNumber}
            />
            <div className="user-answer">
              <h3>Your Answer:</h3>
              <p>{answer}</p>
            </div>
            <FeedbackDisplay feedback={feedback} />
            {!isComplete && (
              <button 
                onClick={handleNextQuestion}
                className="btn-primary"
              >
                Continue to Next Question
              </button>
            )}
          </>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
};

export default InterviewSession;
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'InterviewSession.jsx'), 'w') as f:
    f.write(interview_session)
print("  ✓ src/components/InterviewSession.jsx")

# QuestionDisplay.jsx
question_display = """const QuestionDisplay = ({ question, questionNumber }) => {
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
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'QuestionDisplay.jsx'), 'w') as f:
    f.write(question_display)
print("  ✓ src/components/QuestionDisplay.jsx")

# AnswerInput.jsx
answer_input = """const AnswerInput = ({ answer, onChange, onSubmit, loading, disabled }) => {
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
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'AnswerInput.jsx'), 'w') as f:
    f.write(answer_input)
print("  ✓ src/components/AnswerInput.jsx")

# FeedbackDisplay.jsx
feedback_display = """const FeedbackDisplay = ({ feedback }) => {
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
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'FeedbackDisplay.jsx'), 'w') as f:
    f.write(feedback_display)
print("  ✓ src/components/FeedbackDisplay.jsx")

# CompletionSummary.jsx
completion_summary = """import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getInterviewSummary } from '../services/api';

const CompletionSummary = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const data = await getInterviewSummary(sessionId);
        setSummary(data);
      } catch (err) {
        setError(err.message || 'Failed to load interview summary');
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, [sessionId]);

  const getOverallGrade = (score) => {
    if (score >= 8) return { grade: 'A', label: 'Excellent', color: '#22c55e' };
    if (score >= 7) return { grade: 'B', label: 'Good', color: '#3b82f6' };
    if (score >= 6) return { grade: 'C', label: 'Fair', color: '#f59e0b' };
    if (score >= 5) return { grade: 'D', label: 'Pass', color: '#ef4444' };
    return { grade: 'F', label: 'Fail', color: '#991b1b' };
  };

  if (loading) {
    return (
      <div className="completion-summary">
        <div className="container">
          <div className="loading">Loading your results...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="completion-summary">
        <div className="container">
          <div className="error-message">{error}</div>
          <button onClick={() => navigate('/')} className="btn-primary">
            Start New Interview
          </button>
        </div>
      </div>
    );
  }

  const averageScore = summary?.average_score || 0;
  const gradeInfo = getOverallGrade(averageScore);

  return (
    <div className="completion-summary">
      <div className="container">
        <div className="summary-header">
          <h1>Interview Complete!</h1>
          <p>Here's your performance summary</p>
        </div>

        <div className="overall-score">
          <div className="score-circle" style={{ borderColor: gradeInfo.color }}>
            <span className="grade">{gradeInfo.grade}</span>
            <span className="score">{averageScore.toFixed(1)}/10</span>
          </div>
          <div className="score-details">
            <h2>{gradeInfo.label}</h2>
            <p>Overall Performance</p>
          </div>
        </div>

        <div className="performance-breakdown">
          <h3>Performance Breakdown</h3>
          <div className="metrics">
            <div className="metric">
              <span className="metric-label">Average Relevance</span>
              <span className="metric-value">
                {summary?.avg_relevance?.toFixed(1) || 0}/10
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Average Depth</span>
              <span className="metric-value">
                {summary?.avg_depth?.toFixed(1) || 0}/10
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Average Accuracy</span>
              <span className="metric-value">
                {summary?.avg_accuracy?.toFixed(1) || 0}/10
              </span>
            </div>
            <div className="metric">
              <span className="metric-label">Questions Answered</span>
              <span className="metric-value">
                {summary?.total_questions || 0}
              </span>
            </div>
          </div>
        </div>

        <div className="questions-review">
          <h3>Questions & Feedback</h3>
          {summary?.questions?.map((item, index) => (
            <div key={index} className="question-item">
              <div className="question-header-summary">
                <span className="q-number">Q{index + 1}</span>
                <span className="q-scores">
                  R: {item.relevance_score} | D: {item.depth_score} | A: {item.accuracy_score}
                </span>
              </div>
              <p className="q-text"><strong>Question:</strong> {item.question}</p>
              <p className="q-answer"><strong>Your Answer:</strong> {item.answer}</p>
              <div className="q-feedback">
                <strong>Feedback:</strong>
                <p>{item.feedback}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="summary-footer">
          <p className="summary-message">{summary?.summary || ''}</p>
          <button onClick={() => navigate('/')} className="btn-primary">
            Start New Interview
          </button>
        </div>
      </div>
    </div>
  );
};

export default CompletionSummary;
"""
with open(os.path.join(BASE_DIR, 'src', 'components', 'CompletionSummary.jsx'), 'w') as f:
    f.write(completion_summary)
print("  ✓ src/components/CompletionSummary.jsx")

# ===== STEP 5: Create Main App Files =====
print("\n[5/5] Creating main app files...")

# App.jsx
app_jsx = """import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import InterviewSession from './components/InterviewSession';
import CompletionSummary from './components/CompletionSummary';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/interview/:sessionId" element={<InterviewSession />} />
          <Route path="/summary/:sessionId" element={<CompletionSummary />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
"""
with open(os.path.join(BASE_DIR, 'src', 'App.jsx'), 'w') as f:
    f.write(app_jsx)
print("  ✓ src/App.jsx")

# main.jsx
main_jsx = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""
with open(os.path.join(BASE_DIR, 'src', 'main.jsx'), 'w') as f:
    f.write(main_jsx)
print("  ✓ src/main.jsx")

# index.css
index_css = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app {
  min-height: 100vh;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

/* Landing Page */
.landing-page {
  display: flex;
  align-items: center;
  min-height: 100vh;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 3rem;
}

.header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.upload-form {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-group input[type="file"],
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
}

.file-name {
  margin-top: 0.5rem;
  color: #10b981;
  font-size: 0.9rem;
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c00;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  border-left: 4px solid #c00;
}

/* Interview Session */
.interview-session {
  padding: 2rem 0;
}

.interview-header {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.interview-header h2 {
  color: #667eea;
  margin-bottom: 0.5rem;
}

.interview-header p {
  color: #666;
  font-size: 0.9rem;
}

.question-display {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-header {
  margin-bottom: 1rem;
}

.question-number {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.question-content {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #333;
}

.answer-input {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.answer-input label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #333;
}

.answer-input textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 200px;
}

.answer-input textarea:focus {
  outline: none;
  border-color: #667eea;
}

.answer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.char-count {
  color: #666;
  font-size: 0.9rem;
}

.user-answer {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #667eea;
}

.user-answer h3 {
  color: #667eea;
  margin-bottom: 0.75rem;
}

.user-answer p {
  color: #333;
  line-height: 1.6;
}

/* Feedback Display */
.feedback-display {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.feedback-display h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
}

.scores-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.score-item {
  text-align: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.score-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.score-value {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
}

.score-high { color: #10b981; }
.score-medium { color: #f59e0b; }
.score-low { color: #ef4444; }

.score-description {
  display: block;
  font-size: 0.85rem;
  color: #666;
}

.feedback-text {
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.feedback-text h4 {
  color: #333;
  margin-bottom: 0.75rem;
}

.feedback-text p {
  color: #555;
  line-height: 1.6;
}

/* Completion Summary */
.completion-summary {
  padding: 2rem 0;
}

.summary-header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
}

.summary-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.overall-score {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.score-circle {
  width: 150px;
  height: 150px;
  border: 8px solid;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-circle .grade {
  font-size: 3rem;
  font-weight: bold;
}

.score-circle .score {
  font-size: 1.2rem;
  color: #666;
}

.score-details h2 {
  color: #333;
  margin-bottom: 0.25rem;
}

.score-details p {
  color: #666;
}

.performance-breakdown {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.performance-breakdown h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.metric {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
}

.metric-label {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #667eea;
}

.questions-review {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.questions-review h3 {
  color: #667eea;
  margin-bottom: 1.5rem;
}

.question-item {
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.question-item:last-child {
  margin-bottom: 0;
}

.question-header-summary {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.q-number {
  font-weight: bold;
  color: #667eea;
}

.q-scores {
  font-size: 0.9rem;
  color: #666;
}

.q-text, .q-answer, .q-feedback {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.q-feedback {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  margin-top: 0.5rem;
}

.summary-footer {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-message {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.loading {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
  font-size: 1.2rem;
  color: #667eea;
}

.completion-message {
  background: white;
  padding: 3rem;
  border-radius: 12px;
  text-align: center;
}

.completion-message h2 {
  color: #10b981;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .overall-score {
    flex-direction: column;
  }
  
  .metrics {
    grid-template-columns: 1fr;
  }
}
"""
with open(os.path.join(BASE_DIR, 'src', 'index.css'), 'w') as f:
    f.write(index_css)
print("  ✓ src/index.css")

# ===== COMPLETION =====
print("\n" + "=" * 60)
print("✅ Frontend setup complete!")
print("=" * 60)
print("\nDirectory structure created:")
print("frontend/")
print("├── package.json")
print("├── vite.config.js")
print("├── index.html")
print("├── .gitignore")
print("├── public/")
print("└── src/")
print("    ├── App.jsx")
print("    ├── main.jsx")
print("    ├── index.css")
print("    ├── components/")
print("    │   ├── LandingPage.jsx")
print("    │   ├── InterviewSession.jsx")
print("    │   ├── QuestionDisplay.jsx")
print("    │   ├── AnswerInput.jsx")
print("    │   ├── FeedbackDisplay.jsx")
print("    │   └── CompletionSummary.jsx")
print("    └── services/")
print("        └── api.js")
print("\nNext steps:")
print("1. cd frontend")
print("2. npm install")
print("3. npm run dev")
print("\nThe app will run on http://localhost:3000")
print("Make sure the backend is running on http://localhost:8000")
