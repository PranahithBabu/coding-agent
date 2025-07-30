import os
import re
import asyncio
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Load environment variables
load_dotenv()

async def test_readme_modification():
    """Test README.md modification functionality"""
    print("🔍 Testing README.md modification...")
    
    e2b_api_key = os.getenv("E2B_API_KEY")
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    repo_name_only = "hotel-management-application"
    
    try:
        sandbox = Sandbox(api_key=e2b_api_key)
        
        # Test reading and modifying README.md
        readme_test_code = f"""
import subprocess
import os

# Clone repository
subprocess.run(['git', 'clone', '{repo_url}'], capture_output=True, text=True)

# Change to repository directory
os.chdir('{repo_name_only}')

# Configure Git user
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Create new branch
branch_name = 'backspace-readme-update'
subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True, text=True)

# Read current README.md
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        current_content = f.read()
    print(f"📖 Current README.md content length: {{len(current_content)}} characters")
    print(f"📖 First 200 characters: {{current_content[:200]}}")
except Exception as e:
    print(f"❌ Error reading README.md: {{e}}")
    current_content = ""

# Check if the text we want to add is already there
target_text = "**Note:** Rolling out more details soon"
if target_text in current_content:
    print(f"ℹ️ Text '{{target_text}}' already exists in README.md")
else:
    print(f"📝 Adding text '{{target_text}}' to README.md")
    
    # Add the text to README.md
    new_content = current_content + "\\n\\n" + target_text
    
    # Write the updated content back
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ README.md updated successfully")

# Check Git status
result = subprocess.run(['git', 'status'], capture_output=True, text=True)
print(f"📊 Git status after modification:\\n{{result.stdout}}")

# Stage the changes
subprocess.run(['git', 'add', 'README.md'], capture_output=True, text=True)

# Commit the changes
commit_result = subprocess.run(['git', 'commit', '-m', 'Update README.md with Backspace Agent'], capture_output=True, text=True)
print(f"📝 Commit result: {{commit_result.stdout}}")
print(f"📝 Commit stderr: {{commit_result.stderr}}")

print("✅ README modification test completed")
"""
        
        result = sandbox.run_code(readme_test_code)
        print(f"📤 README modification logs: {result.logs}")
        
        if "README modification test completed" in str(result.logs):
            print("✅ README modification test PASSED!")
            return True
        else:
            print("❌ README modification test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ README modification test failed: {str(e)}")
        return False

async def test_file_operations():
    """Test various file operations in the repository"""
    print("\n🔍 Testing file operations...")
    
    e2b_api_key = os.getenv("E2B_API_KEY")
    repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    repo_name_only = "hotel-management-application"
    
    try:
        sandbox = Sandbox(api_key=e2b_api_key)
        
        file_ops_code = f"""
import subprocess
import os
import json

# Clone repository
subprocess.run(['git', 'clone', '{repo_url}'], capture_output=True, text=True)

# Change to repository directory
os.chdir('{repo_name_only}')

# Configure Git user
subprocess.run(['git', 'config', 'user.name', 'Backspace Agent'], capture_output=True, text=True)
subprocess.run(['git', 'config', 'user.email', 'agent@backspace.dev'], capture_output=True, text=True)

# Create new branch
branch_name = 'backspace-file-ops-test'
subprocess.run(['git', 'checkout', '-b', branch_name], capture_output=True, text=True)

# List all files in the repository
def list_files_recursive(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            files.append(filepath)
    return files

all_files = list_files_recursive('.')
print(f"📁 Total files in repository: {{len(all_files)}}")
print(f"📁 Sample files: {{all_files[:10]}}")

# Find README files
readme_files = [f for f in all_files if 'README' in f.upper()]
print(f"📖 README files found: {{readme_files}}")

# Find package.json files (if any)
package_files = [f for f in all_files if 'package.json' in f]
print(f"📦 Package.json files found: {{package_files}}")

# Test reading different file types
for file_path in readme_files[:2]:  # Test first 2 README files
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📖 Successfully read {{file_path}} ({{len(content)}} characters)")
    except Exception as e:
        print(f"❌ Error reading {{file_path}}: {{e}}")

print("✅ File operations test completed")
"""
        
        result = sandbox.run_code(file_ops_code)
        print(f"📤 File operations logs: {result.logs}")
        
        if "File operations test completed" in str(result.logs):
            print("✅ File operations test PASSED!")
            return True
        else:
            print("❌ File operations test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ File operations test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Code Modification Test")
    print("=" * 50)
    
    async def run_tests():
        # Test README modification
        readme_test = await test_readme_modification()
        
        # Test file operations
        file_ops_test = await test_file_operations()
        
        print("=" * 50)
        if readme_test and file_ops_test:
            print("🎉 Code modification tests PASSED!")
        else:
            print("💥 Code modification tests FAILED!")
    
    asyncio.run(run_tests()) 