#!/usr/bin/env python3
"""
Practice: Basic AI-powered code modification system
Step-by-step learning approach
"""

import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

# Load environment variables
load_dotenv()

async def main():
    print("🤖 Practice: Basic AI Code Modification System")
    print("=" * 50)
    
    # Check if GROQ_API_KEY is available
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please add your Groq API key to the .env file")
        return
    
    print("✅ GROQ_API_KEY found")
    
    # Initialize AI service
    try:
        ai_service = AIService()
        print("✅ AI Service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AI Service: {e}")
        return
    
    # Test basic functionality
    print("\n📝 Testing basic AI functionality...")
    
    # Simple test prompt
    test_prompt = "Add a blue button to the page"
    test_files = ["index.html", "style.css"]
    
    try:
        print(f"🤖 Analyzing prompt: '{test_prompt}'")
        print(f"📁 Available files: {test_files}")
        
        analysis = await ai_service.analyze_prompt(test_prompt, test_files)
        
        print(f"✅ AI Analysis successful!")
        print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
        print("📁 Files to modify:")
        for file_change in analysis.get("files", []):
            print(f"  - {file_change.get('path')} ({file_change.get('operation')})")
            print(f"    Description: {file_change.get('description')}")
        
        # Step 2: Generate executable code
        print("\n🔧 Generating executable code...")
        generated_code = ai_service.generate_code_changes(analysis)
        print("✅ Code generation successful!")
        print("\n📄 Generated code:")
        print("-" * 40)
        print(generated_code)
        print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 