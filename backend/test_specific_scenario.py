#!/usr/bin/env python3
"""
Test specific scenarios that the user encountered
"""

import asyncio
import os
from ai_service import AIService

async def test_specific_scenarios():
    print("🤖 Testing Specific User Scenarios")
    print("=" * 50)
    
    # Test with repository structure similar to user's repo
    repo_structure = ['README.md', 'index.html', 'index.css', 'index.js']
    
    ai_service = AIService()
    
    # Scenario 1: Change button styling (should modify existing CSS)
    print("\n📝 Scenario 1: Fix the login button styling")
    print("-" * 40)
    try:
        analysis = await ai_service.analyze_prompt("Fix the login button styling", repo_structure)
        print(f"✅ AI Analysis: {analysis}")
        print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
        print("📁 Files to modify:")
        for file_change in analysis.get("files", []):
            print(f"  - {file_change.get('path')} ({file_change.get('operation')})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Scenario 2: Change button from success to primary
    print("\n📝 Scenario 2: Change button from success to primary")
    print("-" * 40)
    try:
        analysis = await ai_service.analyze_prompt("Change the button from success to primary style", repo_structure)
        print(f"✅ AI Analysis: {analysis}")
        print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
        print("📁 Files to modify:")
        for file_change in analysis.get("files", []):
            print(f"  - {file_change.get('path')} ({file_change.get('operation')})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Specific Scenarios Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_specific_scenarios()) 