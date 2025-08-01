#!/usr/bin/env python3
"""
Simple test for AI service components
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

load_dotenv()

async def test_ai_components():
    print("🧪 Testing AI Service Components")
    print("=" * 50)
    
    try:
        # Test AI service initialization
        print("1️⃣ Testing AI Service Initialization...")
        ai_service = AIService()
        print("   ✅ AI Service initialized successfully!")
        
        # Test file type detection
        print("2️⃣ Testing File Type Detection...")
        test_files = ["index.html", "style.css", "script.js", "main.py", "unknown.txt"]
        for file in test_files:
            file_type = ai_service._get_file_type(file)
            print(f"   📄 {file} -> {file_type}")
        
        # Test branch name generation
        print("3️⃣ Testing Branch Name Generation...")
        branch_suffix = ai_service._generate_branch_suffix()
        print(f"   🌿 Generated branch: backspace-ai-{branch_suffix}")
        
        # Test code validation (with mock data)
        print("4️⃣ Testing Code Validation...")
        mock_analysis = {
            "files": [
                {
                    "path": "index.html",
                    "operation": "append",
                    "content": "<div>Test content</div>",
                    "description": "Test modification"
                }
            ]
        }
        validation = ai_service.validate_generated_code(mock_analysis)
        print(f"   ✅ Validation result: {'Passed' if validation['valid'] else 'Failed'}")
        
        print("\n🎉 All basic components working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nThis might be due to missing environment variables.")
        print("Required variables:")
        print("  - GROQ_API_KEY")
        print("  - E2B_API_KEY (for full functionality)")
        print("  - GITHUB_TOKEN (for full functionality)")

if __name__ == "__main__":
    asyncio.run(test_ai_components()) 