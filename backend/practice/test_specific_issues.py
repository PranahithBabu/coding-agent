#!/usr/bin/env python3
"""
Test specific issues the user encountered
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

# Load environment variables
load_dotenv()

async def test_specific_issues():
    print("🧪 Testing Specific User Issues")
    print("=" * 60)
    
    ai_service = AIService()
    
    # Test files similar to user's repository
    test_files = ["index.html", "index.css", "index.js"]
    
    # Issue 1: Button styling (should modify existing CSS, not create new files)
    print("\n🔍 Issue 1: Button Styling")
    print("-" * 40)
    await test_single_prompt(ai_service, "Fix the login button styling", test_files)
    
    # Issue 2: Change button class (should modify HTML and CSS intelligently)
    print("\n🔍 Issue 2: Change Button Class")
    print("-" * 40)
    await test_single_prompt(ai_service, "Change the button from success to primary style", test_files)
    
    # Issue 3: File replacement (should not overwrite entire files)
    print("\n🔍 Issue 3: File Replacement")
    print("-" * 40)
    await test_single_prompt(ai_service, "Replace the header with a new navigation menu", test_files)
    
    # Issue 4: Technology stack matching (should not create Vue/React for HTML/JS repo)
    print("\n🔍 Issue 4: Technology Stack Matching")
    print("-" * 40)
    await test_single_prompt(ai_service, "Add a new component for user profile", test_files)

async def test_single_prompt(ai_service, prompt: str, files: list):
    """Test a single prompt and show detailed results"""
    try:
        print(f"🤖 Prompt: '{prompt}'")
        print(f"📁 Files: {files}")
        
        analysis = await ai_service.analyze_prompt(prompt, files)
        
        print(f"✅ Analysis successful!")
        print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
        print("📁 Files to modify:")
        
        for i, file_change in enumerate(analysis.get("files", []), 1):
            print(f"  {i}. {file_change.get('path')} ({file_change.get('operation')})")
            print(f"     Description: {file_change.get('description')}")
            content = file_change.get('content', 'N/A')
            if len(content) > 100:
                content = content[:100] + "..."
            print(f"     Content: {content}")
        
        # Generate code
        generated_code = ai_service.generate_code_changes(analysis)
        print(f"\n🔧 Generated {len(generated_code.split(chr(10)))} lines of executable code")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_specific_issues()) 