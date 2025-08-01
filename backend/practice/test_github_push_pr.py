import os
import re
import asyncio
import aiohttp
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Load environment variables
load_dotenv()

async def get_next_branch_number():
    """Get the next available branch number for backspace-push-test"""
    print("🔍 Checking existing branches...")
    
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = "PranahithBabu"
    repo_name = "hotel-management-application"
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return 1
    
    try:
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
                    
                    # Find existing backspace-push-test branches
                    backspace_branches = []
                    for branch_name in branch_names:
                        if branch_name.startswith("backspace-push-test"):
                            backspace_branches.append(branch_name)
                    
                    print(f"📋 Found existing backspace branches: {backspace_branches}")
                    
                    if not backspace_branches:
                        print("✅ No existing backspace branches found, starting with 1")
                        return 1
                    
                    # Extract numbers from branch names
                    numbers = []
                    for branch in backspace_branches:
                        if branch == "backspace-push-test":
                            numbers.append(0)  # Base branch without number
                        else:
                            # Extract number from branch name like "backspace-push-test-1"
                            match = re.search(r'backspace-push-test-(\d+)$', branch)
                            if match:
                                numbers.append(int(match.group(1)))
                    
                    if numbers:
                        next_number = max(numbers) + 1
                        print(f"✅ Next available branch number: {next_number}")
                        return next_number
                    else:
                        print("✅ No numbered branches found, starting with 1")
                        return 1
                else:
                    print(f"❌ Failed to get branches: {response.status}")
                    return 1
                    
    except Exception as e:
        print(f"❌ Error checking branches: {str(e)}")
        return 1

async def test_github_push():
    """Test pushing changes to GitHub"""
    print("🔍 Testing GitHub push functionality...")
    
    e2b_api_key = os.getenv("E2B_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    repo_name_only = "hotel-management-application"
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False, None, None
    
    try:
        sandbox = Sandbox(api_key=e2b_api_key)
        
        # Get next branch number
        branch_number = await get_next_branch_number()
        branch_name = f'backspace-push-test-{branch_number}'
        
        print(f"🌿 Using branch name: {branch_name}")
        
        # Return the branch name and number so it can be used by other functions
        return await _test_github_push_internal(sandbox, repo_url, repo_name_only, github_token, branch_name, branch_number)
    except Exception as e:
        print(f"❌ GitHub push test failed: {str(e)}")
        return False, None, None

async def _test_github_push_internal(sandbox, repo_url, repo_name_only, github_token, branch_name, branch_number):
    """Internal function to test GitHub push"""
    push_test_code = f"""
import subprocess
import os

# Clone repository
print("📥 Cloning repository...")
clone_result = subprocess.run(['git', 'clone', '{repo_url}'], capture_output=True, text=True)
if clone_result.returncode != 0:
    print(f"❌ Clone failed: {{clone_result.stderr}}")
    exit(1)

# Change to repository directory
os.chdir('{repo_name_only}')

# Configure Git user
print("⚙️ Configuring Git...")
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Create new branch
branch_name = '{branch_name}'
print(f"🌿 Creating branch: {{branch_name}}")
branch_result = subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True, text=True)
if branch_result.returncode != 0:
    print(f"❌ Branch creation failed: {{branch_result.stderr}}")
    exit(1)

# Make a small change to README.md
print("📝 Modifying README.md...")
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Add a test note
test_note = f"\\n\\n**Test Note:** This is a test push from Backspace Agent - Branch {branch_number}"
if test_note not in content:
    new_content = content + test_note
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ Added test note to README.md")
else:
    print("ℹ️ Test note already exists")

# Stage and commit changes
print("📦 Staging changes...")
subprocess.run(['git', 'add', 'README.md'], capture_output=True, text=True)

print("📝 Committing changes...")
commit_result = subprocess.run(['git', 'commit', '-m', 'Test push from Backspace Agent'], capture_output=True, text=True)
if commit_result.returncode != 0:
    print(f"❌ Commit failed: {{commit_result.stderr}}")
    exit(1)

# Configure remote with token
print("🔗 Configuring remote...")
remote_url = 'https://{github_token}@github.com/PranahithBabu/{repo_name_only}.git'
subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], capture_output=True, text=True)

# Push to GitHub
print("🚀 Pushing to GitHub...")
push_result = subprocess.run(['git', 'push', '-u', 'origin', branch_name], capture_output=True, text=True)
print(f"📤 Push stdout: {{push_result.stdout}}")
print(f"📤 Push stderr: {{push_result.stderr}}")

if push_result.returncode == 0:
    print("✅ Push to GitHub successful!")
    print(f"🌿 Branch '{{branch_name}}' pushed successfully")
else:
    print("❌ Push to GitHub failed!")
    print(f"📤 Error: {{push_result.stderr}}")
    exit(1)

print("✅ GitHub push test completed")
"""
    
    result = sandbox.run_code(push_test_code)
    print(f"📤 Push test logs: {result.logs}")
    
    if "Push to GitHub successful!" in str(result.logs):
        print("✅ GitHub push test PASSED!")
        return True, branch_name, branch_number
    else:
        print("❌ GitHub push test FAILED!")
        return False, None, None

async def test_pull_request_creation_with_branch(branch_name, branch_number):
    """Test creating a pull request via GitHub API with specific branch"""
    print(f"\n🔍 Testing Pull Request creation for branch: {branch_name}")
    
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = "PranahithBabu"
    repo_name = "hotel-management-application"
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False
    
    try:
        # First, verify the branch exists
        print("🔍 Verifying branch exists...")
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with aiohttp.ClientSession() as session:
            # Check if branch exists
            async with session.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch_name}",
                headers=headers
            ) as response:
                if response.status != 200:
                    print(f"❌ Branch '{branch_name}' does not exist: {response.status}")
                    return False
                else:
                    branch_data = await response.json()
                    print(f"✅ Branch '{branch_name}' exists")
            
            # Test GitHub API for PR creation
            pr_data = {
                "title": f"Test PR from Backspace Agent - Branch {branch_number}",
                "body": f"This is a test pull request created by the Backspace Coding Agent to verify PR creation functionality. Branch: {branch_name}",
                "head": branch_name,
                "base": "main"
            }
            
            print("🔗 Creating pull request via GitHub API...")
            
            async with session.post(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls",
                headers=headers,
                json=pr_data
            ) as response:
                if response.status == 201:
                    pr_response = await response.json()
                    pr_url = pr_response["html_url"]
                    pr_number = pr_response["number"]
                    print("✅ Pull Request created successfully!")
                    print(f"🔗 PR URL: {pr_url}")
                    print(f"📊 PR Number: #{pr_number}")
                    print(f"📋 Title: {pr_response['title']}")
                    print(f"🌿 Branch: {pr_response['head']['ref']} -> {pr_response['base']['ref']}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to create PR: {response.status}")
                    print(f"📤 Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Pull Request creation test failed: {str(e)}")
        return False

async def test_cleanup():
    """Test cleanup - close the test PR"""
    print("\n🧹 Testing cleanup...")
    
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = "PranahithBabu"
    repo_name = "hotel-management-application"
    
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False
    
    try:
        # First, find the test PR
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        async with aiohttp.ClientSession() as session:
            # Get all PRs
            async with session.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls",
                headers=headers
            ) as response:
                if response.status == 200:
                    prs = await response.json()
                    test_pr = None
                    
                    for pr in prs:
                        if "Test PR from Backspace Agent" in pr["title"]:
                            test_pr = pr
                            break
                    
                    if test_pr:
                        pr_number = test_pr["number"]
                        print(f"🔍 Found test PR #{pr_number}")
                        
                        # Close the PR
                        close_data = {"state": "closed"}
                        async with session.patch(
                            f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}",
                            headers=headers,
                            json=close_data
                        ) as close_response:
                            if close_response.status == 200:
                                print(f"✅ Test PR #{pr_number} closed successfully")
                                return True
                            else:
                                print(f"❌ Failed to close PR #{pr_number}")
                                return False
                    else:
                        print("ℹ️ No test PR found to clean up")
                        return True
                else:
                    print(f"❌ Failed to get PRs: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Cleanup test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting GitHub Push & PR Test")
    print("=" * 50)
    
    async def run_tests():
        # Test GitHub push
        push_test, branch_name, branch_number = await test_github_push()
        
        if push_test and branch_name and branch_number:
            # Test PR creation with the same branch name
            pr_test = await test_pull_request_creation_with_branch(branch_name, branch_number)
            
            # Test cleanup
            cleanup_test = await test_cleanup()
            
            print("=" * 50)
            if pr_test and cleanup_test:
                print("🎉 GitHub Push & PR tests PASSED!")
            else:
                print("💥 GitHub Push & PR tests FAILED!")
        else:
            print("=" * 50)
            print("💥 GitHub Push & PR tests FAILED! (Push failed)")
    
    asyncio.run(run_tests()) 