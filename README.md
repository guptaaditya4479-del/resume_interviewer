# Resume Interviewer - AI-Powered Technical Interview System

An intelligent interview system that conducts technical interviews based on resumes and job descriptions. Built with FastAPI backend and React frontend.

## Features

### Backend
- ✅ **Secure Configuration**: API keys stored in environment variables
- ✅ **Database Persistence**: SQLite database for session management
- ✅ **Comprehensive Logging**: Structured logging throughout the application
- ✅ **Error Handling**: Proper validation and error responses
- ✅ **CORS Enabled**: Ready for frontend integration
- ✅ **Health Monitoring**: `/health` endpoint for system checks
- ✅ **RESTful API**: Clean API design with OpenAPI documentation

### AI Capabilities
- Extract structured data from PDF resumes
- Generate domain-specific interview questions (DevOps, Backend, ML)
- Evaluate candidate answers with scoring (0-10)
- Generate intelligent follow-up questions for weak answers
- Provide detailed feedback (strengths, weaknesses)

## Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd resume_interviewer
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:
```env
OPENROUTER_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=mistralai/mistral-7b-instruct
DEBUG=True
```

⚠️ **NEVER commit the `.env` file to version control!**

5. **Initialize database**
```bash
python database.py
```

6. **Run the server**
```bash
uvicorn main:app --reload
```

Backend will be available at `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## API Endpoints

### POST /interview
Start a new interview session by uploading a resume.

**Request:**
- `resume`: PDF file (multipart/form-data)
- `domain`: string (devops | backend | ml)

**Response:**
```json
{
  "session_id": "uuid",
  "question": "Tell me about yourself.",
  "type": "intro"
}
```

### POST /answer
Submit an answer to the current question.

**Request:**
```json
{
  "session_id": "uuid",
  "answer": "Your answer text..."
}
```

**Response:**
```json
{
  "feedback": {
    "score": 7,
    "strengths": "Good understanding...",
    "weaknesses": "Could improve...",
    "follow_up_question": ""
  },
  "next_question": "Next question text",
  "type": "jd"
}
```

### GET /interview/{session_id}/summary
Get complete interview summary with all Q&A pairs.

### GET /health
Health check endpoint.

## Project Structure

```
resume_interviewer/
├── main.py              # FastAPI application entry point
├── pipeline.py          # AI pipeline for question generation and evaluation
├── utils.py             # PDF text extraction utilities
├── config.py            # Configuration management
├── database.py          # SQLAlchemy models and database setup
├── db_operations.py     # Database CRUD operations
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (DO NOT COMMIT)
├── .gitignore          # Git ignore rules
├── interview_sessions.db # SQLite database (auto-generated)
└── frontend/           # React frontend
    ├── src/
    │   ├── components/    # React components
    │   ├── services/      # API service layer
    │   ├── App.jsx        # Main application
    │   └── main.jsx       # Entry point
    ├── package.json
    └── vite.config.js
```

## Supported Domains

### DevOps
Focus areas: CI/CD pipelines, Kubernetes, Docker, Terraform, AWS, monitoring (Prometheus/Grafana)

### Backend
Focus areas: REST APIs, database design, SQL optimization, authentication, microservices, performance

### Machine Learning
Focus areas: Data preprocessing, feature engineering, model training, evaluation metrics, ML pipelines, model monitoring

## Interview Flow

1. **Upload Resume**: Candidate uploads PDF resume and selects job domain
2. **Question Generation**: System extracts structured data and generates:
   - 1 intro question ("Tell me about yourself")
   - 2 job description-based questions
   - 2 resume-based questions
3. **Answer Evaluation**: Each answer is scored 0-10 with feedback
4. **Follow-up Questions**: If score < 6, system asks targeted follow-up
5. **Completion**: All answers stored in database with full summary

## Security Notes

- ✅ API keys stored in environment variables
- ✅ PDF file validation (type, size limits)
- ✅ Input sanitization and validation
- ✅ Proper error handling without exposing internals
- ⚠️ CORS set to allow all origins (change for production!)
- ⚠️ Use HTTPS in production
- ⚠️ Add authentication before deploying

## Database Schema

### interviews
- session_id, resume_text, domain, structured_data (JSON)
- status (in_progress | completed)
- current_index, created_at, updated_at

### questions
- interview_id, question_text, question_type, order_index

### answers  
- interview_id, question_id, answer_text
- score, strengths, weaknesses, follow_up_question

## Development

### Running Tests
```bash
pytest  # Backend tests (TODO)
```

### Logging
Logs are printed to console with format:
```
2024-04-06 12:30:45 - module_name - INFO - Log message
```

Set `DEBUG=True` in `.env` for INFO level logs.

## Troubleshooting

**Issue: "OPENROUTER_API_KEY not found"**
- Solution: Create `.env` file with your API key

**Issue: Database errors**
- Solution: Run `python database.py` to initialize tables

**Issue: CORS errors in frontend**
- Solution: Ensure backend is running and CORS middleware is enabled

**Issue: PDF extraction fails**
- Solution: Ensure PDF is text-based (not scanned images)

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Rate limiting implementation
- [ ] Real-time interview (WebSocket support)
- [ ] Video recording capability
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Export interview reports as PDF

## License

[Your License Here]

## Contributing

[Your contributing guidelines here]
