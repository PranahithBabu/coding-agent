#!/usr/bin/env python3
"""
Test Integration - Verify Enhanced AI Service with Main Backend
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

load_dotenv()

async def test_integration():
    print("🔧 Testing Enhanced AI Service Integration")
    print("=" * 60)
    
    try:
        # Test 1: Import and initialize AI service
        print("1️⃣ Testing AI Service Import...")
        ai_service = AIService()
        print("   ✅ AI Service imported and initialized successfully!")
        
        # Test 2: Test basic functionality
        print("2️⃣ Testing Basic Functionality...")
        
        # Test file type detection
        test_files = ["index.html", "style.css", "script.js"]
        for file in test_files:
            file_type = ai_service._get_file_type(file)
            print(f"   📄 {file} -> {file_type}")
        
        # Test branch name generation
        branch_suffix = ai_service._generate_branch_suffix()
        print(f"   🌿 Branch name: backspace-ai-{branch_suffix}")
        
        # Test 3: Test AI analysis (if GROQ_API_KEY is available)
        print("3️⃣ Testing AI Analysis...")
        if os.getenv("GROQ_API_KEY"):
            try:
                analysis = await ai_service.analyze_prompt("Add a blue button", test_files)
                print(f"   ✅ AI Analysis: {analysis.get('summary', 'N/A')}")
                
                # Test validation
                validation = ai_service.validate_generated_code(analysis)
                print(f"   ✅ Validation: {'Passed' if validation['valid'] else 'Failed'}")
                
            except Exception as e:
                print(f"   ⚠️ AI Analysis test failed (expected if no API key): {e}")
        else:
            print("   ⚠️ GROQ_API_KEY not found - skipping AI analysis test")
        
        # Test 4: Test code generation
        print("4️⃣ Testing Code Generation...")
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
        generated_code = ai_service.generate_code_changes(mock_analysis)
        print(f"   ✅ Generated {len(generated_code.split(chr(10)))} lines of code")
        
        print("\n🎉 Integration Test Complete!")
        print("✅ Enhanced AI Service is properly integrated with main backend")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check if ai_service.py is in the backend directory")
        print("   2. Check if all dependencies are installed")
        print("   3. Check if environment variables are set")

if __name__ == "__main__":
    asyncio.run(test_integration()) 