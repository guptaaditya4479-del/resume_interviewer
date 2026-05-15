#!/usr/bin/env python3
import os
import json

base_dir = os.path.join(os.path.dirname(__file__), 'frontend')

# Create directories
dirs = [
    base_dir,
    os.path.join(base_dir, 'src'),
    os.path.join(base_dir, 'src', 'components'),
    os.path.join(base_dir, 'src', 'services'),
    os.path.join(base_dir, 'public')
]

print('Creating directories...')
for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)
    print(f'✓ Created: {dir_path}')

# Create package.json
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

print('\nCreating files...')

# Write package.json
with open(os.path.join(base_dir, 'package.json'), 'w') as f:
    json.dump(package_json, f, indent=2)
print(f'✓ Created: {os.path.join(base_dir, "package.json")}')

# Write vite.config.js
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

with open(os.path.join(base_dir, 'vite.config.js'), 'w') as f:
    f.write(vite_config)
print(f'✓ Created: {os.path.join(base_dir, "vite.config.js")}')

# Write index.html
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

with open(os.path.join(base_dir, 'index.html'), 'w') as f:
    f.write(index_html)
print(f'✓ Created: {os.path.join(base_dir, "index.html")}')

# Write .gitignore
gitignore = """node_modules
dist
dist-ssr
*.local
.vscode/*
"""

with open(os.path.join(base_dir, '.gitignore'), 'w') as f:
    f.write(gitignore)
print(f'✓ Created: {os.path.join(base_dir, ".gitignore")}')

# Write api.js
api_js = """import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

/**
 * Start a new interview session
 * @param {File} resumeFile - The resume file to upload
 * @param {string} domain - The interview domain (e.g., 'software-engineering', 'data-science')
 * @returns {Promise} Response with session ID and first question
 */
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
    throw new Error(`Failed to start interview: ${error.message}`);
  }
};

/**
 * Submit an answer to the current interview question
 * @param {string} sessionId - The interview session ID
 * @param {string} answer - The user's answer to the question
 * @returns {Promise} Response with feedback and next question or completion status
 */
export const submitAnswer = async (sessionId, answer) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/answer`, {
      session_id: sessionId,
      answer: answer
    });

    return response.data;
  } catch (error) {
    throw new Error(`Failed to submit answer: ${error.message}`);
  }
};

/**
 * Get the interview summary and feedback
 * @param {string} sessionId - The interview session ID
 * @returns {Promise} Response with interview summary, score, and feedback
 */
export const getInterviewSummary = async (sessionId) => {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/interview/${sessionId}/summary`
    );

    return response.data;
  } catch (error) {
    throw new Error(`Failed to get interview summary: ${error.message}`);
  }
};

export default {
  startInterview,
  submitAnswer,
  getInterviewSummary
};
"""

with open(os.path.join(base_dir, 'src', 'services', 'api.js'), 'w') as f:
    f.write(api_js)
print(f'✓ Created: {os.path.join(base_dir, "src", "services", "api.js")}')

print('\n✅ All directories and files created successfully!')
print('\nCreated structure:')
print('frontend/')
print('├── package.json')
print('├── vite.config.js')
print('├── index.html')
print('├── .gitignore')
print('├── public/')
print('└── src/')
print('    ├── components/')
print('    └── services/')
print('        └── api.js')
