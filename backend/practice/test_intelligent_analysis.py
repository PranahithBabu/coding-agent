#!/usr/bin/env python3
"""
Test intelligent file content analysis
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

# Load environment variables
load_dotenv()

async def test_intelligent_analysis():
    print("🧠 Testing Intelligent File Content Analysis")
    print("=" * 60)
    
    # Change to test_files directory
    os.chdir("test_files")
    
    ai_service = AIService()
    
    # Test files that actually exist
    test_files = ["index.html", "index.css", "index.js"]
    
    print("📁 Available test files:")
    for file in test_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} (not found)")
    
    # Test 1: Change button class (should be intelligent about existing content)
    print("\n🔍 Test 1: Change button from success to primary")
    print("-" * 50)
    await test_with_real_files(ai_service, "Change the button from success to primary style", test_files)
    
    # Test 2: Add new feature (should understand existing structure)
    print("\n🔍 Test 2: Add a dark mode toggle")
    print("-" * 50)
    await test_with_real_files(ai_service, "Add a dark mode toggle to the page", test_files)
    
    # Test 3: Modify existing functionality (should be smart about existing code)
    print("\n🔍 Test 3: Add email validation")
    print("-" * 50)
    await test_with_real_files(ai_service, "Add email validation to the login form", test_files)

async def test_with_real_files(ai_service, prompt: str, files: list):
    """Test with real files that exist"""
    try:
        print(f"🤖 Prompt: '{prompt}'")
        print(f"📁 Files: {files}")
        
        # Show file analysis
        print("\n📊 File Content Analysis:")
        for file_path in files:
            analysis = await ai_service.analyze_file_content(file_path)
            if analysis["exists"]:
                print(f"  📄 {file_path}:")
                print(f"    - Type: {analysis['file_type']}")
                print(f"    - Size: {analysis['size']} chars, {analysis['lines']} lines")
                print(f"    - Has CSS: {analysis['has_css']}")
                print(f"    - Has JS: {analysis['has_js']}")
                print(f"    - Has HTML: {analysis['has_html']}")
            else:
                print(f"  ❌ {file_path}: File does not exist")
        
        # Analyze prompt with file content understanding
        analysis = await ai_service.analyze_prompt(prompt, files)
        
        print(f"\n✅ Analysis successful!")
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
        
        # Step 5: Validate generated code
        print(f"\n🔍 Validating generated code...")
        validation = ai_service.validate_generated_code(analysis)
        
        if validation["valid"]:
            print("✅ Code validation passed!")
        else:
            print("❌ Code validation failed!")
        
        if validation["warnings"]:
            print("⚠️  Warnings:")
            for warning in validation["warnings"]:
                print(f"   - {warning}")
        
        if validation["errors"]:
            print("❌ Errors:")
            for error in validation["errors"]:
                print(f"   - {error}")
        
        if validation["suggestions"]:
            print("💡 Suggestions:")
            for suggestion in validation["suggestions"]:
                print(f"   - {suggestion}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_intelligent_analysis()) 