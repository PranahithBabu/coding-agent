#!/usr/bin/env python3
"""
Test different prompts to see how the AI handles various scenarios
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

# Load environment variables
load_dotenv()

async def test_prompt(prompt: str, files: list, test_name: str = ""):
    """Test a single prompt and show results"""
    print(f"\n{'='*60}")
    if test_name:
        print(f"🧪 TEST: {test_name}")
    else:
        print(f"🧪 TEST: {prompt}")
    print(f"{'='*60}")
    
    try:
        ai_service = AIService()
        
        print(f"🤖 Prompt: '{prompt}'")
        print(f"📁 Files: {files}")
        
        analysis = await ai_service.analyze_prompt(prompt, files)
        
        print(f"✅ Analysis successful!")
        print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
        print("📁 Files to modify:")
        for file_change in analysis.get("files", []):
            print(f"  - {file_change.get('path')} ({file_change.get('operation')})")
            print(f"    Description: {file_change.get('description')}")
            print(f"    Content: {file_change.get('content', 'N/A')[:100]}...")
        
        # Generate code
        generated_code = ai_service.generate_code_changes(analysis)
        print(f"\n🔧 Generated {len(generated_code.split(chr(10)))} lines of code")
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def run_tests():
    print("🤖 AI Prompt Testing Suite")
    print("=" * 60)
    
    # Test files (simulating a typical web project)
    test_files = ["index.html", "style.css", "script.js"]
    
    # Test cases
    test_cases = [
        {
            "name": "Simple UI Change",
            "prompt": "Change the button color to red",
            "files": test_files
        },
        {
            "name": "Content Modification", 
            "prompt": "Add a new paragraph about features",
            "files": test_files
        },
        {
            "name": "Functionality Request",
            "prompt": "Add a function to validate email",
            "files": test_files
        },
        {
            "name": "Complex Multi-file",
            "prompt": "Add a dark mode toggle that changes both CSS and HTML",
            "files": test_files
        },
        {
            "name": "Edge Case",
            "prompt": "Fix the broken login form",
            "files": test_files
        }
    ]
    
    for test_case in test_cases:
        await test_prompt(
            test_case["prompt"], 
            test_case["files"], 
            test_case["name"]
        )
    
    print(f"\n{'='*60}")
    print("🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(run_tests()) 