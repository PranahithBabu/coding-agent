# import asyncio
# import os
# from e2b import Sandbox
# from dotenv import load_dotenv

# # To load environment variables from .env file
# load_dotenv()

# # Configuring environment variables
# # E2B_API_KEY = os.getenv("E2B_API_KEY")

# async def test_e2b_basic():
#     """Test basic E2B sandbox functionality"""
#     print("🔍 Testing E2B API key...")
    
#     # Check if E2B API key is set
#     e2b_api_key = os.getenv("E2B_API_KEY")
#     if not e2b_api_key:
#         print("❌ E2B_API_KEY not found in environment variables")
#         return False
    
#     print("✅ E2B_API_KEY found")
    
#     try:
#         print("🔒 Creating E2B sandbox...")
#         sandbox = await Sandbox(
#             # template="base",
#             api_key=e2b_api_key
#         )
        
#         print("✅ Sandbox created successfully")
        
#         try:
#             print("🧪 Running test command...")
#             result = await sandbox.process.start_and_wait("echo 'Hello from E2B sandbox!'")
            
#             if result.exit_code == 0:
#                 print("✅ Test command executed successfully")
#                 print(f"📤 Output: {result.stdout}")
#                 return True
#             else:
#                 print("❌ Test command failed")
#                 print(f"📤 Error: {result.stderr}")
#                 return False
                
#         finally:
#             print("🔒 Closing sandbox...")
#             await sandbox.close()
#             print("✅ Sandbox closed")
            
#     except Exception as e:
#         print(f"❌ E2B test failed: {str(e)}")
#         return False

# if __name__ == "__main__":
#     print("🚀 Starting E2B Basic Test")
#     print("=" * 50)
    
#     result = asyncio.run(test_e2b_basic())
    
#     print("=" * 50)
#     if result:
#         print("🎉 E2B test PASSED!")
#     else:
#         print("�� E2B test FAILED!") 


import os
from dotenv import load_dotenv
load_dotenv()
from e2b_code_interpreter import Sandbox

sbx = Sandbox(api_key=os.getenv("E2B_API_KEY")) # By default the sandbox is alive for 5 minutes
execution = sbx.run_code("print('hello world')") # Execute Python inside the sandbox
print(execution.logs)

files = sbx.files.list("/")
print(files)