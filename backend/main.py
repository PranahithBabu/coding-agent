from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import os
import re
import aiohttp
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from ai_service import AIService

# Load environment variables
load_dotenv()

app = FastAPI(title="Backspace Coding Agent API")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    repoUrl: str
    prompt: str

async def stream_log(message: str) -> str:
    """Format message for SSE streaming"""
    return f"data: {json.dumps({'message': message})}\n\n"

async def get_next_branch_number(repo_owner: str, repo_name: str) -> int:
    """Get the next available branch number for backspace-agent"""
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise Exception("GITHUB_TOKEN not found in environment variables")
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with aiohttp.ClientSession() as session:
        # Get all branches
        async with session.get(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches",
            headers=headers
        ) as response:
            if response.status == 200:
                branches = await response.json()
                branch_names = [branch["name"] for branch in branches]
                
                # Find existing backspace-agent branches
                backspace_branches = []
                for branch_name in branch_names:
                    if branch_name.startswith("backspace-agent"):
                        backspace_branches.append(branch_name)
                
                if not backspace_branches:
                    return 1
                
                # Extract numbers from branch names
                numbers = []
                for branch in backspace_branches:
                    if branch == "backspace-agent":
                        numbers.append(0)  # Base branch without number
                    else:
                        # Extract number from branch name like "backspace-agent-1"
                        match = re.search(r'backspace-agent-(\d+)$', branch)
                        if match:
                            numbers.append(int(match.group(1)))
                
                if numbers:
                    return max(numbers) + 1
                else:
                    return 1
            else:
                return 1

async def extract_repo_info(repo_url: str) -> tuple[str, str, str]:
    """Extract repository owner, name, and full name from URL"""
    repo_match = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$', repo_url)
    if not repo_match:
        raise ValueError("Invalid GitHub repository URL")
    
    repo_name = repo_match.group(1)
    repo_owner, repo_name_only = repo_name.split('/')
    return repo_owner, repo_name_only, repo_name

async def apply_code_changes(sandbox: Sandbox, repo_name: str, prompt: str, stream_log_func):
    """Apply AI-powered code changes based on the user prompt"""
    
    # Initialize AI service
    ai_service = AIService()
    
    # First, get the repository structure
    structure_code = """
import os
print("📁 Scanning repository structure...")
files = []
for root, dirs, filenames in os.walk('.'):
    for filename in filenames:
        if not filename.startswith('.') and not root.startswith('./.git'):
            rel_path = os.path.join(root, filename)
            files.append(rel_path)
print("Repository files:")
for file in sorted(files):
    print(f"  - {file}")
"""
    
    structure_result = sandbox.run_code(structure_code)
    repo_files = []
    
    # Parse the file list from output
    for line in str(structure_result.logs).split('\n'):
        if line.strip().startswith('  - '):
            file_path = line.strip()[4:]  # Remove "  - " prefix
            repo_files.append(file_path)
    
    if not repo_files:
        repo_files = ["README.md"]  # Fallback
    
    print(f"📋 Repository files detected: {repo_files}")
    
    # Use AI to analyze the prompt and generate changes
    yield await stream_log("🤖 Analyzing your request with AI...")
    analysis = ai_service.analyze_prompt(prompt, repo_files)
    
    print(f"🤖 AI Analysis: {json.dumps(analysis, indent=2)}")
    yield await stream_log(f"📋 AI Summary: {analysis.get('summary', 'Processing changes...')}")
    
    # Generate the code to execute
    ai_code = await ai_service.generate_code_changes(analysis, repo_files)
    
    print(f"🤖 Generated AI code:\n{ai_code}")
    
    # Execute the AI-generated code
    result = sandbox.run_code(ai_code)
    print(f"🔍 AI execution logs: {result.logs}")
    
    # Check if the execution completed successfully
    logs_str = str(result.logs)
    if "AI-powered code changes completed" in logs_str:
        yield await stream_log(f"✅ AI-powered changes applied: {analysis.get('summary', 'Changes completed')}")
    else:
        error_msg = f"AI code execution failed. Logs: {result.logs}"
        print(f"❌ {error_msg}")
        yield await stream_log(f"❌ {error_msg}")
        raise Exception(error_msg)

async def commit_and_push_changes(sandbox: Sandbox, repo_name: str, branch_name: str, github_token: str, repo_owner: str, repo_name_only: str):
    """Commit and push changes to GitHub"""
    commit_code = f"""
import subprocess
import os

print("🔍 Starting commit and push process...")

# We should be in the repository directory after cloning
print("📁 Current directory contents:")
try:
    files = os.listdir('.')
    print(f"Found {{len(files)}} files/directories:")
    for file in files:
        print(f"  - {{file}}")
except Exception as e:
    print(f"❌ Error listing directory: {{e}}")

# Configure Git user
print("⚙️ Configuring Git user...")
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Check git status
print("📊 Checking git status...")
status_result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(f"Git status: {{status_result.stdout}}")

# Stage all changes
print("📦 Staging changes...")
add_result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
if add_result.returncode != 0:
    print(f"❌ Git add failed: {{add_result.stderr}}")
    exit(1)
print("✅ Changes staged successfully")

# Commit changes
print("📝 Committing changes...")
commit_result = subprocess.run(['git', 'commit', '-m', 'Update by Backspace Coding Agent'], capture_output=True, text=True)
print(f"Commit stdout: {{commit_result.stdout}}")
print(f"Commit stderr: {{commit_result.stderr}}")
if commit_result.returncode != 0:
    print(f"❌ Commit failed: {{commit_result.stderr}}")
    exit(1)
print("✅ Changes committed successfully")

# Configure remote with token
print("🔗 Configuring remote...")
remote_url = 'https://{github_token}@github.com/{repo_owner}/{repo_name_only}.git'
subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], capture_output=True, text=True)

# Push to GitHub
print("🚀 Pushing to GitHub...")
push_result = subprocess.run(['git', 'push', '-u', 'origin', '{branch_name}'], capture_output=True, text=True)
print(f"Push stdout: {{push_result.stdout}}")
print(f"Push stderr: {{push_result.stderr}}")
if push_result.returncode == 0:
    print("✅ Changes pushed successfully")
else:
    print(f"❌ Push failed: {{push_result.stderr}}")
    exit(1)

print("✅ Commit and push completed")
"""
    
    result = sandbox.run_code(commit_code)
    if "Commit and push completed" not in str(result.logs):
        raise Exception("Failed to commit and push changes")

async def create_pull_request(repo_owner: str, repo_name: str, branch_name: str, branch_number: int, prompt: str) -> str:
    """Create a pull request via GitHub API"""
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        raise Exception("GITHUB_TOKEN not found in environment variables")
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    pr_data = {
        "title": f"Update by Backspace Agent - Branch {branch_number}",
        "body": f"This pull request was automatically created by the Backspace Coding Agent based on your prompt:\n\n**Prompt:** {prompt}\n\n**Branch:** {branch_name}",
        "head": branch_name,
        "base": "main"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls",
            headers=headers,
            json=pr_data
        ) as response:
            if response.status == 201:
                pr_response = await response.json()
                return pr_response["html_url"]
            else:
                error_text = await response.text()
                raise Exception(f"Failed to create PR: {response.status} - {error_text}")

@app.post("/code")
async def process_code_request(request: CodeRequest):
    """Main endpoint to process code changes"""
    
    github_token = os.getenv("GITHUB_TOKEN")
    e2b_api_key = os.getenv("E2B_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not github_token:
        raise HTTPException(status_code=500, detail="GitHub token not configured")
    
    if not e2b_api_key:
        raise HTTPException(status_code=500, detail="E2B API key not configured")
    
    if not groq_api_key:
        raise HTTPException(status_code=500, detail="Groq API key not configured")
    
    async def generate_stream():
        try:
            yield await stream_log("🚀 Starting Backspace Coding Agent...")
            yield await stream_log(f"📋 Processing prompt: {request.prompt}")
            yield await stream_log(f"🔗 Repository: {request.repoUrl}")
            
            # Extract repository information
            yield await stream_log("🔍 Extracting repository information...")
            repo_owner, repo_name_only, repo_name = await extract_repo_info(request.repoUrl)
            yield await stream_log(f"📁 Repository: {repo_owner}/{repo_name_only}")
            
            # Get next branch number
            yield await stream_log("🔢 Determining next branch number...")
            branch_number = await get_next_branch_number(repo_owner, repo_name_only)
            branch_name = f"backspace-agent-{branch_number}"
            yield await stream_log(f"🌿 Using branch: {branch_name}")
            
            # Start E2B sandbox session
            yield await stream_log("🔒 Initializing secure sandbox...")
            sandbox = Sandbox(api_key=e2b_api_key)
            
            try:
                # Clone repository
                yield await stream_log("📥 Cloning repository...")
                clone_code = f"""
import subprocess
import os

# Clone repository
clone_result = subprocess.run(['git', 'clone', '{request.repoUrl}'], capture_output=True, text=True)
if clone_result.returncode != 0:
    print(f"❌ Clone failed: {{clone_result.stderr}}")
    exit(1)

print("✅ Repository cloned successfully")

# Change to the cloned repository directory
os.chdir('{repo_name_only}')
print(f"✅ Changed to repository directory: {repo_name_only}")

# List contents to verify
files = os.listdir('.')
print(f"📁 Repository contents: {{files}}")
"""
                
                result = sandbox.run_code(clone_code)
                if "Repository cloned successfully" not in str(result.logs):
                    raise Exception("Failed to clone repository")
                
                # Create new branch
                yield await stream_log(f"🌿 Creating branch: {branch_name}")
                branch_code = f"""
import subprocess
import os

print("🔍 Starting branch creation...")

# We should be in the repository directory after cloning
print("📁 Current directory contents:")
try:
    files = os.listdir('.')
    print(f"Found {{len(files)}} files/directories:")
    for file in files:
        print(f"  - {{file}}")
except Exception as e:
    print(f"❌ Error listing directory: {{e}}")

# Configure Git user
print("⚙️ Configuring Git user...")
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Create new branch
print(f"🌿 Creating branch: {branch_name}")
branch_result = subprocess.run(['git', 'checkout', '-b', '{branch_name}'], capture_output=True, text=True)
print(f"Branch creation stdout: {{branch_result.stdout}}")
print(f"Branch creation stderr: {{branch_result.stderr}}")
if branch_result.returncode != 0:
    print(f"❌ Branch creation failed: {{branch_result.stderr}}")
    exit(1)

print("✅ Branch created successfully")
"""
                
                result = sandbox.run_code(branch_code)
                if "Branch created successfully" not in str(result.logs):
                    raise Exception("Failed to create branch")
                
                # Apply code changes
                yield await stream_log("📝 Applying AI-powered code changes...")
                async for log_message in apply_code_changes(sandbox, repo_name_only, request.prompt, stream_log):
                    yield log_message
                
                # Commit and push changes
                yield await stream_log("📦 Committing and pushing changes...")
                await commit_and_push_changes(sandbox, repo_name_only, branch_name, github_token, repo_owner, repo_name_only)
                yield await stream_log("✅ Changes committed and pushed successfully")
                
                # Create pull request
                yield await stream_log("🔗 Creating pull request...")
                pr_url = await create_pull_request(repo_owner, repo_name_only, branch_name, branch_number, request.prompt)
                yield await stream_log(f"✅ Pull Request created successfully!")
                yield await stream_log(f"🔗 PR URL: {pr_url}")
                
                # Send PR URL to frontend
                yield f"data: {json.dumps({'pr_url': pr_url})}\n\n"
                
            finally:
                # Sandbox closes automatically after 5 minutes
                yield await stream_log("🔒 Sandbox will close automatically")
                
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            yield await stream_log(error_msg)
            # Don't raise HTTPException here as it causes "response already started" error
            # Just log the error and continue
            print(f"Backend error: {str(e)}")
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "text/event-stream",
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Backspace Coding Agent API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 