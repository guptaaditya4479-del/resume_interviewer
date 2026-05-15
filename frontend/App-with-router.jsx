// OPTIONAL: React Router version of App.jsx
// 
// To use this version:
// 1. Install React Router: npm install react-router-dom
// 2. Replace src/App.jsx with this file
// 3. Update LandingPage.jsx and other components to use useNavigate() instead of callbacks
//
// This provides URL-based routing instead of state-based navigation

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
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

/*
 * BENEFITS OF ROUTER VERSION:
 * - URL reflects current page (shareable links)
 * - Browser back/forward buttons work
 * - Better for larger apps
 * 
 * CURRENT VERSION:
 * - Simpler, no extra dependency
 * - All state managed in App.jsx
 * - Works perfectly for this use case
 * 
 * Both versions are valid! Use whichever you prefer.
 */
