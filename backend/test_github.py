import os
import re
import aiohttp
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_github_token():
    """Test GitHub token and repository access"""
    print("🔍 Testing GitHub token...")
    
    # Check if GitHub token is set
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ GITHUB_TOKEN not found in environment variables")
        return False
    
    print("✅ GITHUB_TOKEN found")
    
    # Test repository access
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    print(f"🔍 Testing access to repository: {repo_url}")
    
    # Extract repo name from URL
    repo_match = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git)?$', repo_url)
    if not repo_match:
        print("❌ Invalid GitHub repository URL")
        return False
    
    repo_name = repo_match.group(1)
    repo_owner, repo_name_only = repo_name.split('/')
    print(f"📁 Repository: {repo_owner}/{repo_name_only}")
    
    # Test GitHub API access
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            print("🌐 Testing GitHub API connection...")
            
            # Test repository access
            async with session.get(
                f"https://api.github.com/repos/{repo_owner}/{repo_name_only}",
                headers=headers
            ) as response:
                if response.status == 200:
                    repo_data = await response.json()
                    print("✅ Repository access successful!")
                    print(f"📋 Repository details:")
                    print(f"   - Name: {repo_data['name']}")
                    print(f"   - Full name: {repo_data['full_name']}")
                    print(f"   - Private: {repo_data['private']}")
                    print(f"   - Default branch: {repo_data['default_branch']}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ GitHub API access failed: {response.status}")
                    print(f"📤 Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ GitHub test failed: {str(e)}")
        return False

async def test_github_user():
    """Test GitHub user authentication"""
    print("\n🔍 Testing GitHub user authentication...")
    
    github_token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.github.com/user",
                headers=headers
            ) as response:
                if response.status == 200:
                    user_data = await response.json()
                    print("✅ GitHub authentication successful!")
                    print(f"👤 User: {user_data['login']}")
                    print(f"📧 Email: {user_data.get('email', 'Not public')}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ GitHub authentication failed: {response.status}")
                    print(f"📤 Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ GitHub user test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting GitHub Token Test")
    print("=" * 50)
    
    async def run_tests():
        # Test repository access
        repo_test = await test_github_token()
        
        # Test user authentication
        user_test = await test_github_user()
        
        print("=" * 50)
        if repo_test and user_test:
            print("🎉 GitHub tests PASSED!")
        else:
            print("💥 GitHub tests FAILED!")
    
    asyncio.run(run_tests()) 