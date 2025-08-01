# 🤖 Backspace Coding Agent - Backend

A complete AI-powered code modification system that understands natural language prompts and automatically applies code changes to GitHub repositories.

## 🚀 Features

- **🤖 Intelligent AI Analysis**: Uses Groq API to understand natural language prompts
- **📁 File Content Analysis**: Intelligently analyzes existing files before making changes
- **🔍 Code Validation**: Validates generated code for safety and correctness
- **🔒 Secure Execution**: Uses E2B sandbox for safe code execution
- **🌿 Git Integration**: Automatic repository cloning, branching, and committing
- **📝 Pull Request Creation**: Creates professional pull requests via GitHub API
- **📡 Real-time Streaming**: Server-Sent Events (SSE) for live progress updates

## 🏗️ Architecture

```
Frontend (React + Next.js)
    ↓
FastAPI Backend (/code endpoint)
    ↓
Enhanced AI Service (Steps 1-8)
    ↓
E2B Sandbox Execution
    ↓
Git Operations + GitHub API
    ↓
Pull Request Creation
```

## 📋 Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- Groq API Key
- E2B API Key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   E2B_API_KEY=your_e2b_api_key
   GITHUB_TOKEN=your_github_token
   ```

## 🚀 Usage

### Start the Backend Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### API Endpoints

#### POST `/code`
Process code modification requests

**Request Body:**
```json
{
  "repoUrl": "https://github.com/owner/repo",
  "prompt": "Add a dark mode toggle to the page"
}
```

**Response:** Server-Sent Events (SSE) stream with real-time progress updates

#### GET `/health`
Health check endpoint

#### GET `/`
Service information

### Example Usage

```bash
curl -X POST "http://localhost:8000/code" \
  -H "Content-Type: application/json" \
  -d '{
    "repoUrl": "https://github.com/your-username/your-repo",
    "prompt": "Add a blue button to the homepage"
  }'
```

## 🧪 Testing

### Quick Integration Test
```bash
python quick_test.py
```

### Complete System Test
```bash
python test_integration.py
```

### Individual Component Tests
```bash
# Test E2B sandbox
python test_e2b.py

# Test GitHub API
python test_github.py

# Test Git operations
python test_git_clone.py

# Test code modification
python test_code_modification.py
```

## 🔧 System Components

### 1. Enhanced AI Service (`ai_service.py`)
- **Step 1**: Basic AI Integration with Groq API
- **Step 2**: Code Generation from AI analysis
- **Step 3**: Enhanced JSON parsing with fallback mechanisms
- **Step 4**: Intelligent file content analysis
- **Step 5**: Code validation and safety checks
- **Step 6**: E2B sandbox integration for secure execution
- **Step 7**: GitHub API integration for pull requests
- **Step 8**: Complete workflow orchestration

### 2. FastAPI Backend (`main.py`)
- RESTful API endpoints
- Server-Sent Events (SSE) streaming
- Error handling and validation
- Repository URL parsing
- Branch name generation

### 3. Test Suite
- Integration tests
- Component tests
- Mock data tests
- Error handling tests

## 🔄 Workflow

1. **User submits request** with repository URL and prompt
2. **AI analyzes prompt** and existing file content
3. **Code is generated** based on AI analysis
4. **Code is validated** for safety and correctness
5. **E2B sandbox is initialized** for secure execution
6. **Repository is cloned** and new branch is created
7. **Code changes are applied** in the sandbox
8. **Changes are committed** and pushed to GitHub
9. **Pull request is created** via GitHub API
10. **Real-time progress** is streamed back to frontend

## 🛡️ Security Features

- **Sandbox Execution**: All code runs in isolated E2B environment
- **Code Validation**: Generated code is validated before execution
- **Error Handling**: Comprehensive error handling and logging
- **API Key Protection**: Environment variables for sensitive data
- **Git Safety**: Automatic branch creation prevents conflicts

## 📊 Monitoring

The system provides real-time progress updates through SSE:

```
🚀 Starting Backspace Coding Agent...
📋 Processing prompt: Add a dark mode toggle
🔗 Repository: https://github.com/owner/repo
🤖 Analyzing user request with AI...
🔍 Validating generated code...
🔒 Initializing secure sandbox...
📥 Cloning repository...
🌿 Creating branch: backspace-ai-1234567890-1234
📝 Applying AI-generated code changes...
📦 Staging changes...
💾 Committing changes...
🚀 Pushing changes...
📝 Creating pull request...
✅ Pull request created: https://github.com/owner/repo/pull/123
```

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

### Debug Mode

Enable debug logging by setting:
```bash
export DEBUG=true
```

## 📈 Performance

- **AI Analysis**: ~2-5 seconds
- **Sandbox Execution**: ~10-30 seconds
- **Git Operations**: ~5-15 seconds
- **Total Processing**: ~20-60 seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test files for examples
3. Check the logs for detailed error messages
4. Create an issue in the repository

---

**🎉 The Backspace Coding Agent is now ready for production use!** 