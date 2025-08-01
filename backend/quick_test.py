#!/usr/bin/env python3
"""
Quick test to verify AI service integration
"""

import asyncio
from ai_service import AIService

async def quick_test():
    print("🧪 Quick AI Service Test")
    print("=" * 30)
    
    try:
        # Test initialization
        ai_service = AIService()
        print("✅ AI Service initialized")
        
        # Test file type detection
        file_type = ai_service._get_file_type("index.html")
        print(f"✅ File type detection: {file_type}")
        
        # Test branch generation
        branch = ai_service._generate_branch_suffix()
        print(f"✅ Branch generation: {branch}")
        
        # Test code generation
        mock_analysis = {
            "files": [{"path": "test.html", "operation": "append", "content": "<div>test</div>", "description": "test"}]
        }
        code = ai_service.generate_code_changes(mock_analysis)
        print(f"✅ Code generation: {len(code.split(chr(10)))} lines")
        
        print("\n🎉 All tests passed! Integration successful!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test()) 