import { useState } from 'react';

function LandingPage({ onStartInterview }) {
  const [resumeFile, setResumeFile] = useState(null);
  const [domain, setDomain] = useState('devops');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setError('Please upload a PDF file');
        setResumeFile(null);
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB');
        setResumeFile(null);
        return;
      }
      setError('');
      setResumeFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      await onStartInterview(resumeFile, domain);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start interview. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🎯 AI Resume Interviewer</h1>
      <p className="subtitle">Upload your resume and start your technical interview</p>

      <form onSubmit={handleSubmit}>
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
            <p style={{ marginTop: '10px', color: '#48bb78' }}>
              ✓ {resumeFile.name} selected
            </p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="domain">Select Job Domain</label>
          <select
            id="domain"
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            disabled={loading}
          >
            <option value="devops">DevOps Engineer</option>
            <option value="backend">Backend Engineer</option>
            <option value="ml">Machine Learning Engineer</option>
          </select>
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading || !resumeFile}>
          {loading ? 'Starting Interview...' : 'Start Interview'}
        </button>
      </form>
    </div>
  );
}

export default LandingPage;
