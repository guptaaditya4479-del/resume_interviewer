# Resume Interviewer - React Frontend

A modern React application for conducting AI-powered technical interviews based on resume analysis.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Tech Stack

- **React 18.2** - UI framework
- **Vite 5.0** - Build tool and dev server
- **Axios 1.6** - HTTP client
- **Pure CSS** - No UI framework dependencies

## Project Structure

```
src/
├── components/          # React components
│   ├── LandingPage.jsx         # Resume upload & domain selection
│   ├── InterviewSession.jsx    # Main interview flow
│   ├── QuestionDisplay.jsx     # Question display component
│   ├── AnswerInput.jsx         # Answer textarea component
│   ├── FeedbackDisplay.jsx     # Score & feedback display
│   └── CompletionSummary.jsx   # Final results page
├── services/
│   └── api.js                  # API client
├── App.jsx                     # Main app component
├── main.jsx                    # Entry point
└── index.css                   # Styles
```

## Features

### Landing Page
- PDF resume upload with validation
- Domain selection (Backend, DevOps, ML)
- Error handling and loading states

### Interview Session
- Dynamic question display
- Answer submission with feedback
- Real-time scoring (Relevance, Depth, Accuracy)
- Auto-advance between questions
- Progress tracking

### Feedback Display
- Color-coded scores (Green: 8+, Yellow: 6-7, Red: <6)
- Three scoring metrics:
  - **Relevance**: How well the answer addresses the question
  - **Depth**: Level of technical detail provided
  - **Accuracy**: Correctness of information
- Detailed textual feedback

### Completion Summary
- Overall grade (A-F) with score visualization
- Performance metrics breakdown
- Complete question & answer review
- Individual feedback for each response
- Restart interview option

## API Integration

The frontend connects to the backend at `http://localhost:8000`.

### Endpoints

**POST /interview**
- Uploads resume and starts interview
- Body: FormData with `resume` (File) and `domain` (string)
- Returns: `{ session_id, question }`

**POST /answer**
- Submits answer for current question
- Body: `{ session_id, answer }`
- Returns: `{ relevance_score, depth_score, accuracy_score, feedback, next_question?, is_complete }`

**GET /interview/:sessionId/summary**
- Retrieves interview results
- Returns: `{ average_score, questions[], summary }`

## Development

### Available Commands

```bash
npm run dev      # Start dev server on http://localhost:3000
npm run build    # Build for production
npm run preview  # Preview production build
```

### Dev Server Features

- ✅ Hot Module Replacement (HMR)
- ✅ Fast Refresh
- ✅ Proxy to backend API
- ✅ Port 3000 (configurable in vite.config.js)

### Environment Setup

Make sure the backend server is running:

```bash
cd C:\Users\Gupta\resume_interviewer
python main.py
```

Backend should run on `http://localhost:8000`

## Styling

The app uses custom CSS with:
- Purple gradient background
- Card-based white content areas
- Responsive design (mobile-friendly)
- Color-coded feedback scores
- Smooth transitions and animations

To customize, edit `src/index.css`.

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Optional Enhancements

### Add React Router

```bash
npm install react-router-dom
```

Then replace `src/App.jsx` with `App-with-router.jsx` for URL-based routing.

### Enhanced Interview Session

Replace `src/components/InterviewSession.jsx` with `InterviewSession-enhanced.jsx` to use modular sub-components.

## Troubleshooting

**Port already in use:**
Change port in `vite.config.js`:
```javascript
server: { port: 3001 }
```

**Backend connection errors:**
- Verify backend is running on port 8000
- Check CORS is enabled in backend
- Open browser console (F12) for details

**Module not found:**
```bash
npm install
```

## License

See LICENSE file in project root.

## Support

For detailed documentation, see:
- `../FRONTEND_README.md` - Complete guide
- `../FRONTEND_IMPLEMENTATION_GUIDE.txt` - Implementation details
- `../FRONTEND_SUMMARY.txt` - Quick reference
