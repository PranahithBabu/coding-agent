import os
import re
import asyncio
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Load environment variables
load_dotenv()

async def test_git_clone():
    """Test Git clone functionality in E2B sandbox"""
    print("🔍 Testing Git clone in E2B sandbox...")
    
    # Check if E2B API key is set
    e2b_api_key = os.getenv("E2B_API_KEY")
    if not e2b_api_key:
        print("❌ E2B_API_KEY not found in environment variables")
        return False
    
    print("✅ E2B_API_KEY found")
    
    # Repository to test
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    print(f"🔍 Testing clone of repository: {repo_url}")
    
    # Extract repo name from URL
    repo_match = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$', repo_url)
    if not repo_match:
        print("❌ Invalid GitHub repository URL")
        return False
    
    repo_name = repo_match.group(1)
    repo_owner, repo_name_only = repo_name.split('/')
    print(f"📁 Repository: {repo_owner}/{repo_name_only}")
    
    try:
        print("🔒 Creating E2B sandbox...")
        sandbox = Sandbox(api_key=e2b_api_key)
        
        print("✅ Sandbox created successfully")
        
        try:
            # Test Git installation
            print("🧪 Testing Git installation...")
            git_result = sandbox.run_code("import subprocess; result = subprocess.run(['git', '--version'], capture_output=True, text=True); print(f'Git version: {result.stdout}'); print(f'Exit code: {result.returncode}')")
            
            if "git version" in str(git_result.logs):
                print("✅ Git is available in sandbox")
            else:
                print("❌ Git is not available in sandbox")
                print(f"📤 Logs: {git_result.logs}")
                return False
            
            # Test repository cloning
            print("🌿 Testing repository cloning...")
            clone_code = f"""
import subprocess
import os

# Clone the repository
result = subprocess.run(['git', 'clone', '{repo_url}'], capture_output=True, text=True)
print(f"Clone exit code: {{result.returncode}}")
print(f"Clone stdout: {{result.stdout}}")
print(f"Clone stderr: {{result.stderr}}")

# List directory contents
if result.returncode == 0:
    files = os.listdir('.')
    print(f"Directory contents: {{files}}")
    
    # Check if repository directory exists
    if '{repo_name_only}' in files:
        print(f"✅ Repository '{repo_name_only}' cloned successfully")
        
        # List contents of the repository
        repo_files = os.listdir('{repo_name_only}')
        print(f"Repository files: {{repo_files}}")
    else:
        print(f"❌ Repository directory '{repo_name_only}' not found")
"""
            
            clone_result = sandbox.run_code(clone_code)
            print(f"📤 Clone result logs: {clone_result.logs}")
            
            if "Repository 'hotel-management-application' cloned successfully" in str(clone_result.logs):
                print("✅ Git clone test PASSED!")
                return True
            else:
                print("❌ Git clone test FAILED!")
                return False
                
        finally:
            print("🔒 Closing sandbox...")
            # Note: E2B sandbox closes automatically after 5 minutes
            print("✅ Sandbox will close automatically")
            
    except Exception as e:
        print(f"❌ Git clone test failed: {str(e)}")
        return False

async def test_git_operations():
    """Test basic Git operations in E2B sandbox"""
    print("\n🔍 Testing Git operations in E2B sandbox...")
    
    e2b_api_key = os.getenv("E2B_API_KEY")
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    repo_name_only = "hotel-management-application"
    
    try:
        sandbox = Sandbox(api_key=e2b_api_key)
        
        git_ops_code = f"""
import subprocess
import os

# Clone repository
subprocess.run(['git', 'clone', '{repo_url}'], capture_output=True, text=True)

# Change to repository directory
os.chdir('{repo_name_only}')

# Configure Git user
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Check current branch
result = subprocess.run(['git', 'branch'], capture_output=True, text=True)
print(f"Current branches: {{result.stdout}}")

# Create new branch
branch_name = 'backspace-test-branch'
result = subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True, text=True)
print(f"Create branch result: {{result.stdout}}")
print(f"Create branch stderr: {{result.stderr}}")

# Check status
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(f"Git status: {{result.stdout}}")

print("✅ Git operations completed")
"""
        
        result = sandbox.run_code(git_ops_code)
        print(f"📤 Git operations logs: {result.logs}")
        
        if "Git operations completed" in str(result.logs):
            print("✅ Git operations test PASSED!")
            return True
        else:
            print("❌ Git operations test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Git operations test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Git Clone Test")
    print("=" * 50)
    
    async def run_tests():
        # Test basic Git clone
        clone_test = await test_git_clone()
        
        # Test Git operations
        ops_test = await test_git_operations()
        
        print("=" * 50)
        if clone_test and ops_test:
            print("🎉 Git tests PASSED!")
        else:
            print("💥 Git tests FAILED!")
    
    asyncio.run(run_tests()) 