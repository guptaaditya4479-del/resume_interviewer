const fs = require('fs');
const path = require('path');

const baseDir = path.join(__dirname, 'frontend');

// Create directories
const dirs = [
  baseDir,
  path.join(baseDir, 'src'),
  path.join(baseDir, 'src', 'components'),
  path.join(baseDir, 'src', 'services'),
  path.join(baseDir, 'public')
];

console.log('Creating directories...');
dirs.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log('✓ Created:', dir);
  } else {
    console.log('- Already exists:', dir);
  }
});

// Define files and their content
const files = [
  {
    path: path.join(baseDir, 'package.json'),
    content: JSON.stringify({
      "name": "resume-interviewer-frontend",
      "private": true,
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
    }, null, 2)
  },
  {
    path: path.join(baseDir, 'vite.config.js'),
    content: `import { defineConfig } from 'vite'
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
`
  },
  {
    path: path.join(baseDir, 'index.html'),
    content: `<!doctype html>
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
`
  },
  {
    path: path.join(baseDir, '.gitignore'),
    content: `node_modules
dist
dist-ssr
*.local
.vscode/*
`
  },
  {
    path: path.join(baseDir, 'src', 'services', 'api.js'),
    content: `import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const startInterview = async (resumeFile, domain) => {
  try {
    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('domain', domain);

    const response = await axios.post(\`\${API_BASE_URL}/interview\`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    return response.data;
  } catch (error) {
    throw new Error(\`Failed to start interview: \${error.message}\`);
  }
};

export const submitAnswer = async (sessionId, answer) => {
  try {
    const response = await axios.post(\`\${API_BASE_URL}/answer\`, {
      session_id: sessionId,
      answer: answer
    });

    return response.data;
  } catch (error) {
    throw new Error(\`Failed to submit answer: \${error.message}\`);
  }
};

export const getInterviewSummary = async (sessionId) => {
  try {
    const response = await axios.get(
      \`\${API_BASE_URL}/interview/\${sessionId}/summary\`
    );

    return response.data;
  } catch (error) {
    throw new Error(\`Failed to get interview summary: \${error.message}\`);
  }
};

export default {
  startInterview,
  submitAnswer,
  getInterviewSummary
};
`
  }
];

console.log('\nCreating files...');
files.forEach(file => {
  fs.writeFileSync(file.path, file.content, 'utf8');
  console.log('✓ Created:', file.path);
});

console.log('\n✅ All directories and files created successfully!');
console.log('\nCreated structure:');
console.log('frontend/');
console.log('├── package.json');
console.log('├── vite.config.js');
console.log('├── index.html');
console.log('├── .gitignore');
console.log('├── public/');
console.log('└── src/');
console.log('    ├── components/');
console.log('    └── services/');
console.log('        └── api.js');
