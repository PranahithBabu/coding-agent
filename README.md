# 🤖 Autonomus PR submission capable Coding Agent

A complete AI-powered code modification system that understands natural language prompts and automatically applies code changes to GitHub repositories.

---

## ✨ Features

- **🌐 Friendly UI**: Clean, minimal Swiss-style frontend (Next.js)
- **🤖 Intelligent AI Analysis**: Uses Groq API (gemma2-9b-it model) to understand natural language prompts
- **📁 Sophisticated File Analysis**: Advanced repository scanning and intelligent file modification decisions
- **🔍 Smart Code Generation**: AI-generated modification scripts for precise file changes
- **🔒 Secure Execution**: Uses E2B sandbox for safe code execution
- **🌿 Git Integration**: Automatic repository cloning, branching, and committing
- **📝 Pull Request Creation**: Creates professional pull requests via GitHub API
- **📡 Real-time Streaming**: Server-Sent Events (SSE) for live progress updates
- **💾 Storage**: History of code fixes stored in `localStorage` promoting privacy-first application

---

## 🏗️ Architecture

```
Frontend → FastAPI → EnhancedCodingAgent → E2B Sandbox → GitHub API
    ↑                                                      ↓
    ←─────────────── SSE Stream ←──────────────────────────┘
```
---
## 🔄 Workflow

1. **User submits request** with repository URL and prompt
2. **Repository scanning** - AI scans all files in the repository
3. **Intelligent routing** - AI decides which files to create vs modify
4. **File content analysis** - AI reads existing file content for context
5. **Modification script generation** - AI generates specific Python scripts for each file
6. **Secure execution** - Scripts run in isolated E2B sandbox
7. **Git operations** - Changes are committed and pushed to GitHub
8. **Pull request creation** - Professional PR created via GitHub API
9. **Real-time progress** - Live updates streamed back to frontend
---
## 🧰 Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Frontend    | React, Next.js     |
| Backend     | FastAPI            |
| Sandbox     | E2B                |
| Agent Logic | Gemma2-9b-it       |
---
## 📋 Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- Groq API Key
- E2B API Key
---
## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PranahithBabu/coding-agent
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   E2B_API_KEY=your_e2b_api_key
   GITHUB_TOKEN=your_github_token
   ```
4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```
---
## 🚀 Usage

### Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```
The server will start on `http://localhost:8000`

### Start the Frontend Client

```bash
cd frontend
npm run dev
```

### API Endpoints

#### POST `/code`
Process code modification requests

**Request Body:**
```json
{
  "repoUrl": "https://github.com/owner/repo",
  "prompt": "Create a SignUp form"
}
```

**Response:** Server-Sent Events (SSE) stream with real-time progress updates

### Example Usage

```bash
curl -X POST "http://localhost:8000/code" \
  -H "Content-Type: application/json" \
  -d '{
    "repoUrl": "https://github.com/your-username/your-repo",
    "prompt": "Enhance styling of homepage"
  }'
```
---
## 🔧 Enhanced System Components

### 1. Sophisticated AI Service (`ai_implementation.py`)
- **🤖 Advanced LLM Integration**: Uses gemma2-9b-it model for better understanding
- **📁 Intelligent File Routing**: AI decides which files to create vs modify
- **🔍 File Content Analysis**: Reads existing files for context-aware modifications
- **📝 Smart Code Generation**: Generates specific modification scripts for each file
- **✅ Code Validation**: Validates generated code for safety and correctness
- **🔒 E2B Sandbox Integration**: Secure execution environment
- **📋 GitHub API Integration**: Professional pull request creation
- **🔄 Complete Workflow Orchestration**: End-to-end process management

### 2. Enhanced FastAPI Backend (`main.py`)
- **🚀 RESTful API endpoints** with sophisticated error handling
- **📡 Server-Sent Events (SSE) streaming** for real-time updates
- **🔍 Repository URL parsing** and validation
- **🌿 Dynamic branch name generation** with conflict prevention
- **📂 Repository file scanning** and analysis
- **🤖 AI-powered modification** with file content reading

### 3. Comprehensive Test Suite
- **🧪 Enhanced integration tests** with sophisticated LLM logic
- **🔧 Component tests** for individual features
- **📊 Mock data tests** for development
- **⚠️ Error handling tests** for robustness
---
## 🛡️ Security Features

- **🔒 Sandbox Execution**: All code runs in isolated E2B environment
- **🔍 Code Validation**: Generated code is validated before execution
- **⚠️ Error Handling**: Comprehensive error handling and logging
- **🔑 API Key Protection**: Environment variables for sensitive data
- **🌿 Git Safety**: Automatic branch creation prevents conflicts
- **📁 File Safety**: File content analysis prevents destructive changes
---
## 📊 Enhanced Monitoring

The system provides detailed real-time progress updates through SSE:

```
🚀 Starting Backspace Coding Agent...
📋 Processing prompt: Add a dark mode toggle
🔗 Repository: https://github.com/owner/repo
📂 Scanning repository files...
📋 Found 15 files in repository
🤖 Analyzing your request with AI...
📋 AI Summary: Processing 3 files based on user request
📝 Processing: Create new file: dark-mode.js
✅ Created dark-mode.js
📝 Processing: Modify existing file: index.html
🔧 Generating modification script for index.html
✅ Successfully modified index.html
📝 Processing: Modify existing file: style.css
🔧 Generating modification script for style.css
✅ Successfully modified style.css
✅ All AI-powered changes completed
📦 Committing and pushing changes...
✅ Changes committed and pushed successfully
🔗 Creating pull request...
✅ Pull request created: https://github.com/owner/repo/pull/123
```
---
## 🐛 Troubleshooting

### Common Issues

1. **Missing Environment Variables**
   - Ensure all required API keys are set in `.env` file
   - Check variable names match exactly

2. **E2B Sandbox Issues**
   - Verify E2B API key is valid
   - Check network connectivity

3. **GitHub API Issues**
   - Verify GitHub token has appropriate permissions
   - Check repository accessibility

4. **AI Analysis Failures**
   - Verify Groq API key is valid
   - Check prompt clarity and specificity
   - Ensure gemma2-9b-it model is available
---
## 📈 Performance

- **Repository Scanning**: ~2-5 seconds
- **AI Analysis**: ~3-8 seconds
- **File Modification**: ~5-15 seconds per file
- **Sandbox Execution**: ~10-30 seconds
- **Git Operations**: ~5-15 seconds
- **Total Processing**: ~25-75 seconds
---
## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request
---
## 📄 License

This project is licensed under the MIT License.
