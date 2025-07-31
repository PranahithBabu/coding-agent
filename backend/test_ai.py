import asyncio
import os
from dotenv import load_dotenv
from ai_service import AIService

load_dotenv()

async def test_ai_analysis():
    """Test the AI service with a sample prompt"""
    
    # Check if GROQ_API_KEY is set
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please add GROQ_API_KEY=your_key_here to your .env file")
        return
    
    ai_service = AIService()
    
    # Sample repository structure
    repo_files = [
        "README.md",
        "package.json",
        "src/index.js",
        "src/components/App.js",
        "public/index.html"
    ]
    
    # Test prompts
    test_prompts = [
        "Add a new feature to display user profile information",
        "Update the README with installation instructions",
        "Create a new API endpoint for user authentication",
        "Fix the login button styling",
        "Add error handling to the main component"
    ]
    
    print("🤖 Testing AI Integration")
    print("=" * 50)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n📝 Test {i}: {prompt}")
        print("-" * 30)
        
        try:
            analysis = await ai_service.analyze_prompt(prompt, repo_files)
            print(f"✅ AI Analysis successful!")
            print(f"📋 Summary: {analysis.get('summary', 'No summary')}")
            print(f"📁 Files to modify: {len(analysis.get('files', []))}")
            
            for file_change in analysis.get('files', []):
                print(f"  - {file_change.get('path')} ({file_change.get('operation')})")
                
        except Exception as e:
            print(f"❌ AI Analysis failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 AI Integration Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_ai_analysis()) 