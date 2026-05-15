# Resume Interviewer - React Frontend

## Quick Setup (EASIEST METHOD)

### Option 1: Double-click `SETUP_FRONTEND.bat`
Just double-click the `SETUP_FRONTEND.bat` file in the resume_interviewer directory!

### Option 2: Run from Command Prompt
```cmd
cd C:\Users\Gupta\resume_interviewer
python create_complete_frontend.py
```

This comprehensive script creates the ENTIRE frontend:
- ✅ Complete directory structure
- ✅ All configuration files (package.json, vite.config.js, etc.)
- ✅ All 6 React components
- ✅ API service module  
- ✅ Main App.jsx and routing
- ✅ Complete CSS styling

### After Setup: Install Dependencies

```cmd
cd frontend
npm install
```

### Start the Development Server

```cmd
npm run dev
```

The app will run on **http://localhost:3000**

---

## What's Included

### Components (src/components/)

1. **LandingPage.jsx**
   - PDF resume upload
   - Domain selection (backend, devops, ml)
   - Start interview button
   - Error handling

2. **InterviewSession.jsx**
   - Main interview flow manager
   - Question/answer state management
   - Feedback display coordination
   - Auto-navigation between questions

3. **QuestionDisplay.jsx**
   - Displays current question
   - Shows question number
   - Clean, readable formatting

4. **AnswerInput.jsx**
   - Large textarea for answers
   - Character count
   - Ctrl+Enter to submit
   - Loading states

5. **FeedbackDisplay.jsx**
   - Displays 3 scores (Relevance, Depth, Accuracy)
   - Color-coded scoring (green/yellow/red)
   - Detailed feedback text
   - Score labels (Excellent/Good/Fair/Needs Improvement)

6. **CompletionSummary.jsx**
   - Overall grade (A-F) with score circle
   - Performance metrics breakdown
   - All questions & answers review
   - Individual feedback for each question
   - Start new interview button

### API Service (src/services/api.js)

Three main functions connecting to backend at `http://localhost:8000`:

```javascript
startInterview(resumeFile, domain)
// POST /interview - Upload resume & select domain

submitAnswer(sessionId, answer)
// POST /answer - Submit answer for current question

getInterviewSummary(sessionId)
// GET /interview/{sessionId}/summary - Get final results
```

### Styling (src/index.css)

- Modern gradient background
- Clean white cards for content
- Responsive design (mobile-friendly)
- Color-coded feedback scores
- Professional typography
- Smooth animations and transitions

---

## Application Flow

1. **Landing Page** (`/`)
   - User uploads resume PDF
   - Selects domain (backend/devops/ml)
   - Clicks "Start Interview"
   - → Navigates to `/interview/:sessionId`

2. **Interview Session** (`/interview/:sessionId`)
   - Shows question one at a time
   - User types answer
   - Submits answer
   - Displays feedback with scores
   - Auto-advances to next question after 5 seconds
   - → Navigates to `/summary/:sessionId` when complete

3. **Completion Summary** (`/summary/:sessionId`)
   - Shows overall grade and score
   - Performance breakdown
   - All questions with feedback
   - Option to start new interview

---

## Technical Details

### Tech Stack
- **React 18.2** - UI framework
- **Vite 5.0** - Build tool and dev server
- **React Router 6.20** - Client-side routing
- **Axios 1.6** - HTTP client for API calls
- **Modern CSS** - No UI library, custom styling

### Project Structure
```
frontend/
├── package.json              # Dependencies and scripts
├── vite.config.js            # Vite configuration with proxy
├── index.html                # HTML entry point
├── .gitignore                # Git ignore rules
├── public/                   # Static assets
└── src/
    ├── main.jsx              # React app entry point
    ├── App.jsx               # Main app with routes
    ├── index.css             # Global styles
    ├── components/           # React components
    │   ├── LandingPage.jsx
    │   ├── InterviewSession.jsx
    │   ├── QuestionDisplay.jsx
    │   ├── AnswerInput.jsx
    │   ├── FeedbackDisplay.jsx
    │   └── CompletionSummary.jsx
    └── services/
        └── api.js            # API client module
```

### Routes
- `/` - Landing page (upload resume)
- `/interview/:sessionId` - Active interview session
- `/summary/:sessionId` - Interview results

### API Integration
The frontend expects these backend endpoints:

**POST /interview**
- Content-Type: multipart/form-data
- Body: { resume: File, domain: string }
- Returns: { session_id: string, question: string }

**POST /answer**
- Content-Type: application/json
- Body: { session_id: string, answer: string }
- Returns: { 
    relevance_score: number,
    depth_score: number,
    accuracy_score: number,
    feedback: string,
    is_complete: boolean,
    next_question?: string
  }

**GET /interview/:sessionId/summary**
- Returns: {
    average_score: number,
    avg_relevance: number,
    avg_depth: number,
    avg_accuracy: number,
    total_questions: number,
    summary: string,
    questions: Array<{
      question: string,
      answer: string,
      feedback: string,
      relevance_score: number,
      depth_score: number,
      accuracy_score: number
    }>
  }

---

## Development

### Available Scripts

```bash
npm run dev      # Start development server (http://localhost:3000)
npm run build    # Build for production (outputs to dist/)
npm run preview  # Preview production build
```

### Development Features
- ✅ Hot Module Replacement (HMR)
- ✅ Fast refresh on file changes
- ✅ Proxy to backend API at localhost:8000
- ✅ Error handling with user feedback
- ✅ Loading states for async operations
- ✅ Responsive design
- ✅ Modern React patterns (hooks, functional components)

### Environment Variables (optional)
You can create a `.env` file in the frontend directory:
```
VITE_API_URL=http://localhost:8000
```

Then update `src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

---

## Troubleshooting

### Backend not running
**Error:** Failed to start interview / Failed to submit answer

**Solution:** Make sure your backend is running on http://localhost:8000
```bash
cd C:\Users\Gupta\resume_interviewer
python main.py
```

### Port 3000 already in use
**Error:** Port 3000 is already in use

**Solution:** Either:
1. Stop the other process using port 3000
2. Or change the port in `vite.config.js`:
   ```javascript
   server: {
     port: 3001,  // Use different port
     ...
   }
   ```

### CORS errors
**Error:** CORS policy blocking requests

**Solution:** Make sure your backend has CORS enabled:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Module not found
**Error:** Cannot find module 'react' or other dependencies

**Solution:** Run `npm install` in the frontend directory

---

## Ready to Go! 🚀

1. ✅ Run `SETUP_FRONTEND.bat` or `python create_complete_frontend.py`
2. ✅ `cd frontend && npm install`
3. ✅ `npm run dev`
4. ✅ Open http://localhost:3000
5. ✅ Make sure backend is running on http://localhost:8000

**Your resume interviewer frontend is ready!**

## API Endpoints

The frontend expects these backend endpoints:

- `POST /interview` - Start interview (FormData with resume file and domain)
- `POST /answer` - Submit answer (JSON with session_id and answer)
- `GET /interview/{session_id}/summary` - Get interview summary

## Components Overview

### LandingPage.jsx
- Resume file upload (PDF)
- Domain selection dropdown (devops, backend, ml)
- Start interview button

### InterviewSession.jsx
- Main interview flow manager
- State management for current question, answers, feedback
- Handles question display and answer submission
- Shows feedback after each answer

### QuestionDisplay.jsx
- Displays current question
- Shows question number and type

### AnswerInput.jsx
- Textarea for user's answer
- Submit button
- Character count (optional)

### FeedbackDisplay.jsx
- Shows evaluation scores (relevance, depth, accuracy)
- Displays feedback text
- Indicates if there's a follow-up question

### CompletionSummary.jsx
- Final interview results
- Overall score
- All questions and feedback
- Performance breakdown

## Development

```cmd
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```
