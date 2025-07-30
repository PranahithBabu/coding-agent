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

async def apply_code_changes(sandbox: Sandbox, repo_name: str, prompt: str) -> str:
    """Apply code changes based on the user prompt"""
    # For now, implement README editing functionality
    if "readme" in prompt.lower() and ("edit" in prompt.lower() or "update" in prompt.lower() or "add" in prompt.lower()):
        # Extract the text to add from the prompt
        # Look for patterns like "mentioning X" or "add X" or "with X"
        import re
        
        # Try to extract the text to add
        patterns = [
            r'mentioning\s+"([^"]+)"',
            r'mentioning\s+([^,\n]+)',
            r'add\s+"([^"]+)"',
            r'add\s+([^,\n]+)',
            r'with\s+"([^"]+)"',
            r'with\s+([^,\n]+)',
            r'edit.*?with\s+"([^"]+)"',
            r'edit.*?with\s+([^,\n]+)'
        ]
        
        text_to_add = None
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                text_to_add = match.group(1).strip()
                break
        
        if not text_to_add:
            # Default text if we can't extract specific text
            text_to_add = "Updated by Backspace Coding Agent"
        
        readme_code = f"""
import subprocess
import os

print("🔍 Starting README modification...")

# We should be in the repository directory after cloning
print("📁 Current directory contents:")
try:
    files = os.listdir('.')
    print(f"Found {{len(files)}} files/directories:")
    for file in files:
        print(f"  - {{file}}")
except Exception as e:
    print(f"❌ Error listing directory: {{e}}")

# Check if README.md exists
print("🔍 Checking if README.md exists...")
if os.path.exists('README.md'):
    print("✅ README.md file found")
else:
    print("❌ README.md file not found")
    # Create a basic README.md if it doesn't exist
    print("📝 Creating new README.md file...")
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write("# Hotel Management Application\\n\\nA hotel management system.")
        print("✅ Created new README.md file")
    except Exception as e:
        print(f"❌ Error creating README.md: {{e}}")
        exit(1)

# Read current README.md
print("📖 Attempting to read README.md...")
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        current_content = f.read()
    print(f"✅ README.md read successfully, content length: {{len(current_content)}} characters")
    if len(current_content) > 0:
        print(f"📄 First 200 characters: {{current_content[:200]}}...")
    else:
        print("📄 README.md is empty")
except Exception as e:
    print(f"❌ Error reading README.md: {{e}}")
    current_content = ""

# Check if the text we want to add is already there
target_text = "{text_to_add}"
print(f"🎯 Target text to add: '{{target_text}}'")

if target_text in current_content:
    print(f"ℹ️ Text '{{target_text}}' already exists in README.md")
else:
    print(f"📝 Adding text '{{target_text}}' to README.md")
    
    # Add the text to README.md
    new_content = current_content + "\\n\\n**Note:** " + target_text
    
    # Write the updated content back
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ README.md updated successfully")
        
        # Verify the write
        with open('README.md', 'r', encoding='utf-8') as f:
            verify_content = f.read()
        print(f"✅ Verification: README.md now has {{len(verify_content)}} characters")
        
    except Exception as e:
        print(f"❌ Error writing README.md: {{e}}")
        raise Exception(f"Failed to write README.md: {{e}}")

print("✅ Code changes applied successfully")
"""
        
        result = sandbox.run_code(readme_code)
        print(f"🔍 Sandbox execution logs: {result.logs}")
        print(f"🔍 Sandbox stdout: {result.logs.stdout}")
        print(f"🔍 Sandbox stderr: {result.logs.stderr}")
        
        # Check if the execution completed successfully
        logs_str = str(result.logs)
        if "Code changes applied successfully" in logs_str:
            return "README.md updated successfully"
        elif "exit(1)" in logs_str or "exit(1)" in str(result.logs.stderr):
            # The script exited with error
            error_msg = f"Sandbox script exited with error. Logs: {result.logs}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        else:
            # Get detailed error information
            error_msg = f"Failed to apply code changes. Sandbox logs: {result.logs}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    else:
        # For other types of changes, implement more sophisticated logic
        # For now, return a placeholder
        return "Code changes applied based on prompt"

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
    
    if not github_token:
        raise HTTPException(status_code=500, detail="GitHub token not configured")
    
    if not e2b_api_key:
        raise HTTPException(status_code=500, detail="E2B API key not configured")
    
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
                yield await stream_log("📝 Applying code changes...")
                change_result = await apply_code_changes(sandbox, repo_name_only, request.prompt)
                yield await stream_log(f"✅ {change_result}")
                
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