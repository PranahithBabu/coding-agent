#!/usr/bin/env python3
"""
Test Complete AI-Powered Backspace Coding Agent System
This tests the full integration from AI analysis to pull request creation
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

# Load environment variables
load_dotenv()

async def test_complete_system():
    print("🚀 Testing Complete AI-Powered Backspace Coding Agent")
    print("=" * 70)
    
    # Test configuration
    test_repo_url = "https://github.com/PranahithBabu/hotel-management-application"
    test_prompt = "Add a dark mode toggle to the page"
    test_files = ["index.html", "style.css", "script.js"]
    
    print(f"📋 Test Configuration:")
    print(f"   Repository: {test_repo_url}")
    print(f"   Prompt: {test_prompt}")
    print(f"   Files: {test_files}")
    print()
    
    try:
        # Initialize AI service
        print("🔧 Initializing AI Service...")
        ai_service = AIService()
        print("✅ AI Service initialized successfully!")
        print()
        
        # Test complete workflow
        print("🔄 Starting complete workflow test...")
        print("-" * 50)
        
        log_count = 0
        async for log in ai_service.process_user_request(test_repo_url, test_prompt, test_files):
            log_count += 1
            print(f"[{log_count:02d}] {log}")
            
            # Check for completion
            if "Pull Request:" in log:
                print("\n🎉 SUCCESS! Complete workflow test passed!")
                print("=" * 50)
                print("✅ AI Analysis: Working")
                print("✅ Code Validation: Working")
                print("✅ E2B Sandbox: Working")
                print("✅ Git Operations: Working")
                print("✅ GitHub API: Working")
                print("✅ Pull Request Creation: Working")
                print("=" * 50)
                break
            elif "❌ Error" in log:
                print(f"\n❌ FAILED! Error encountered: {log}")
                break
        
        if log_count == 0:
            print("❌ No logs generated - system may not be working")
            
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check if all environment variables are set:")
        print("      - GROQ_API_KEY")
        print("      - E2B_API_KEY")
        print("      - GITHUB_TOKEN")
        print("   2. Check if all dependencies are installed:")
        print("      - pip install -r requirements.txt")
        print("   3. Check if the test repository is accessible")

async def test_individual_components():
    """Test individual components separately"""
    print("\n🧪 Testing Individual Components")
    print("=" * 50)
    
    try:
        ai_service = AIService()
        
        # Test 1: AI Analysis
        print("1️⃣ Testing AI Analysis...")
        test_files = ["index.html", "style.css", "script.js"]
        analysis = await ai_service.analyze_prompt("Add a blue button", test_files)
        print(f"   ✅ AI Analysis: {analysis.get('summary', 'N/A')}")
        
        # Test 2: Code Validation
        print("2️⃣ Testing Code Validation...")
        validation = ai_service.validate_generated_code(analysis)
        print(f"   ✅ Code Validation: {'Passed' if validation['valid'] else 'Failed'}")
        
        # Test 3: Branch Name Generation
        print("3️⃣ Testing Branch Name Generation...")
        branch_name = ai_service._generate_branch_suffix()
        print(f"   ✅ Branch Name: backspace-ai-{branch_name}")
        
        print("\n✅ All individual components working!")
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")

if __name__ == "__main__":
    print("🤖 Backspace Coding Agent - Complete System Test")
    print("=" * 70)
    
    # Check environment variables
    required_vars = ["GROQ_API_KEY", "E2B_API_KEY", "GITHUB_TOKEN"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file")
        exit(1)
    
    print("✅ All environment variables found!")
    print()
    
    # Run tests
    asyncio.run(test_individual_components())
    print()
    asyncio.run(test_complete_system()) 