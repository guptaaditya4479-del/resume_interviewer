import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const startInterview = async (resumeFile, domain) => {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('domain', domain);

  const response = await api.post('/interview', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const submitAnswer = async (sessionId, answer) => {
  const response = await api.post('/answer', {
    session_id: sessionId,
    answer: answer,
  });
  return response.data;
};

export const getInterviewSummary = async (sessionId) => {
  const response = await api.get(`/interview/${sessionId}/summary`);
  return response.data;
};

export default api;
