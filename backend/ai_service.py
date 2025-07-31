# import os
# import json
# import aiohttp
# from typing import Dict, List, Optional
# from dotenv import load_dotenv

# load_dotenv()

# class AIService:
#     def __init__(self):
#         self.api_key = os.getenv("GROQ_API_KEY")
#         if not self.api_key:
#             raise ValueError("GROQ_API_KEY not found in environment variables")
#         self.base_url = "https://api.groq.com/openai/v1"
#         self.model = "llama3-8b-8192"  # Fast and efficient model
    
#     async def analyze_prompt(self, prompt: str, repo_structure: List[str]) -> Dict:
#         """
#         Analyze user prompt and determine what changes to make
#         """
#         system_prompt = """You are an AI coding assistant that helps users modify GitHub repositories based on natural language prompts.

# Your job is to:
# 1. Understand what the user wants to change
# 2. Determine which files need to be modified
# 3. Generate the specific code changes needed
# 4. Provide clear instructions for implementation

# Available files in the repository:
# {repo_files}

# IMPORTANT: You must respond with ONLY a valid JSON object. Do not include any other text, markdown, or explanations.

# CRITICAL RULES:
# - ALWAYS work with existing files first. Only create new files if absolutely necessary.
# - For HTML files: Use "modify" operation to intelligently update specific elements, not "replace" to overwrite entire files.
# - For CSS styling: Look for existing CSS files (index.css, style.css, etc.) and modify them.
# - For button styling: Modify the existing CSS file to add/update button styles.
# - Match the existing technology stack: If repo has HTML/JS, don't create Vue/React files.

# Respond with this exact JSON format:
# {{
#     "action": "create|modify|delete",
#     "files": [
#         {{
#             "path": "file_path",
#             "operation": "create|modify|append|replace",
#             "content": "new content or modifications",
#             "description": "what this change does"
#         }}
#     ],
#     "summary": "brief description of all changes"
# }}

# Examples:
# - For "Fix login button styling": Modify existing CSS file to add button styles
# - For "Change button from success to primary": Update the button class in HTML and ensure CSS has primary styles
# - For "Add error handling": Modify existing JavaScript files to add try-catch blocks
# - For "Update README": Modify README.md file
# """

#         user_prompt = f"""
# User request: {prompt}

# Please analyze this request and provide the necessary code changes in JSON format.
# """

#         try:
#             headers = {
#                 "Authorization": f"Bearer {self.api_key}",
#                 "Content-Type": "application/json"
#             }
            
#             payload = {
#                 "model": self.model,
#                 "messages": [
#                     {"role": "system", "content": system_prompt.format(repo_files="\n".join(repo_structure))},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 "temperature": 0.1,
#                 "max_tokens": 2000
#             }
            
#             async with aiohttp.ClientSession() as session:
#                 async with session.post(
#                     f"{self.base_url}/chat/completions",
#                     headers=headers,
#                     json=payload
#                 ) as response:
#                     if response.status == 200:
#                         data = await response.json()
#                         content = data["choices"][0]["message"]["content"]
                        
#                         print(f"🤖 Raw AI response: {content}")
                        
#                         # Clean and parse the response
#                         content = content.strip()
                        
#                         # Remove any markdown code blocks
#                         if content.startswith('```json'):
#                             content = content[7:]
#                         if content.startswith('```'):
#                             content = content[3:]
#                         if content.endswith('```'):
#                             content = content[:-3]
                        
#                         content = content.strip()
                        
#                         try:
#                             # Try to parse the cleaned content directly
#                             return json.loads(content)
#                         except json.JSONDecodeError as e:
#                             print(f"JSON parsing error: {e}")
#                             print(f"Cleaned content: {content}")
                            
#                             # Try to find JSON within the content
#                             json_start = content.find('{')
#                             json_end = content.rfind('}') + 1
                            
#                             if json_start != -1 and json_end != 0:
#                                 json_str = content[json_start:json_end]
#                                 try:
#                                     return json.loads(json_str)
#                                 except json.JSONDecodeError:
#                                     # Try to clean up the JSON string further
#                                     json_str = json_str.replace('\n', ' ').replace('    ', ' ')
#                                     json_str = json_str.replace('\\n', ' ').replace('\\t', ' ')
#                                     return json.loads(json_str)
#                             else:
#                                 print("Could not find JSON in AI response")
#                                 raise
#                     else:
#                         error_text = await response.text()
#                         print(f"Groq API error: {response.status} - {error_text}")
#                         raise Exception(f"Groq API error: {response.status}")
                
#         except Exception as e:
#             print(f"Error in AI analysis: {e}")
            
#             # Smart fallback based on prompt type
#             prompt_lower = prompt.lower()
            
#             if any(word in prompt_lower for word in ['readme', 'documentation', 'docs', 'document']):
#                 # Documentation-related request
#                 return {
#                     "action": "modify",
#                     "files": [
#                         {
#                             "path": "README.md",
#                             "operation": "append",
#                             "content": f"\n\n**Note:** {prompt}",
#                             "description": f"Add user request to README: {prompt}"
#                         }
#                     ],
#                     "summary": f"Add user request to README: {prompt}"
#                 }
#             elif any(word in prompt_lower for word in ['style', 'css', 'button', 'ui', 'design', 'layout']):
#                 # UI/Styling request - modify existing CSS file or create one
#                 css_files = [f for f in repo_structure if f.endswith('.css')]
#                 if css_files:
#                     # Use existing CSS file
#                     css_file = css_files[0]
#                     return {
#                         "action": "modify",
#                         "files": [
#                             {
#                                 "path": css_file,
#                                 "operation": "append",
#                                 "content": f"\n/* {prompt} */\n\n.primary {{\n    background-color: #007bff;\n    color: white;\n    padding: 10px 20px;\n    border: none;\n    border-radius: 5px;\n    cursor: pointer;\n}}\n\n.primary:hover {{\n    background-color: #0056b3;\n}}",
#                                 "description": f"Add button styling to existing CSS file: {prompt}"
#                             }
#                         ],
#                         "summary": f"Add button styling to {css_file}: {prompt}"
#                     }
#                 else:
#                     # Create new CSS file
#                     return {
#                         "action": "create",
#                         "files": [
#                             {
#                                 "path": "styles.css",
#                                 "operation": "create",
#                                 "content": f"/* {prompt} */\n\n.primary {{\n    background-color: #007bff;\n    color: white;\n    padding: 10px 20px;\n    border: none;\n    border-radius: 5px;\n    cursor: pointer;\n}}\n\n.primary:hover {{\n    background-color: #0056b3;\n}}",
#                                 "description": f"Create CSS file for: {prompt}"
#                             }
#                         ],
#                         "summary": f"Create CSS styling for: {prompt}"
#                     }
#             elif any(word in prompt_lower for word in ['api', 'endpoint', 'function', 'method', 'code']):
#                 # Code/API request - create a JavaScript file
#                 return {
#                     "action": "create",
#                     "files": [
#                         {
#                             "path": "api.js",
#                             "operation": "create",
#                             "content": f"// {prompt}\n\n// Add your API endpoint or function here\nfunction handleRequest() {{\n    // Implementation for: {prompt}\n    console.log('Handling request for: {prompt}');\n}}\n\nmodule.exports = {{ handleRequest }};",
#                             "description": f"Create API/function for: {prompt}"
#                         }
#                     ],
#                     "summary": f"Create API/function for: {prompt}"
#                 }
#             else:
#                 # Generic request - create a new file
#                 return {
#                     "action": "create",
#                     "files": [
#                         {
#                             "path": "changes.md",
#                             "operation": "create",
#                             "content": f"# Changes for: {prompt}\n\n## Description\nThis file contains changes requested: {prompt}\n\n## Implementation\nAdd your implementation here based on the request.\n\n## Notes\n- Request: {prompt}\n- Status: Pending implementation\n- Created by: Backspace Coding Agent",
#                             "description": f"Create changes file for: {prompt}"
#                         }
#                     ],
#                     "summary": f"Create changes file for: {prompt}"
#                 }
    
#     async def generate_code_changes(self, analysis: Dict, sandbox_files: List[str]) -> str:
#         """
#         Generate the actual code to execute based on AI analysis
#         """
#         code_parts = []
        
#         code_parts.append("import os")
#         code_parts.append("import subprocess")
#         code_parts.append("")
#         code_parts.append("print('🤖 AI-powered code changes starting...')")
#         code_parts.append("")
        
#         # List current files
#         code_parts.append("print('📁 Current directory contents:')")
#         code_parts.append("files = os.listdir('.')")
#         code_parts.append("for file in files:")
#         code_parts.append("    print(f'  - {file}')")
#         code_parts.append("")
        
#         # Process each file change
#         for file_change in analysis.get("files", []):
#             file_path = file_change.get("path", "")
#             operation = file_change.get("operation", "append")
#             content = file_change.get("content", "")
#             description = file_change.get("description", "")
            
#             code_parts.append(f"# {description}")
            
#             if operation == "create":
#                 code_parts.append(f"print('📝 Creating file: {file_path}')")
#                 code_parts.append(f"os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
#                 code_parts.append(f"with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 # Escape quotes in content
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f'    f.write("""{escaped_content}""")')
#                 code_parts.append(f"print('✅ Created {file_path}')")
                
#             elif operation == "modify":
#                 code_parts.append(f"print('📝 Modifying file: {file_path}')")
#                 code_parts.append(f"if os.path.exists('{file_path}'):")
#                 code_parts.append(f"    with open('{file_path}', 'r', encoding='utf-8') as f:")
#                 code_parts.append("        current_content = f.read()")
#                 # For now, append content (can be enhanced for more complex modifications)
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f"    new_content = current_content + '\\n\\n' + '{escaped_content}'")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 code_parts.append("        f.write(new_content)")
#                 code_parts.append(f"    print('✅ Modified {file_path}')")
#                 code_parts.append("else:")
#                 code_parts.append(f"    print('❌ File {file_path} not found, creating it instead')")
#                 # Create the file if it doesn't exist
#                 code_parts.append(f"    os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f'        f.write("""{escaped_content}""")')
#                 code_parts.append(f"    print('✅ Created {file_path}')")
                
#             elif operation == "append":
#                 code_parts.append(f"print('📝 Appending to file: {file_path}')")
#                 code_parts.append(f"if os.path.exists('{file_path}'):")
#                 code_parts.append(f"    with open('{file_path}', 'r', encoding='utf-8') as f:")
#                 code_parts.append("        current_content = f.read()")
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f"    new_content = current_content + '\\n\\n' + '{escaped_content}'")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 code_parts.append("        f.write(new_content)")
#                 code_parts.append(f"    print('✅ Appended to {file_path}')")
#                 code_parts.append("else:")
#                 code_parts.append(f"    print('❌ File {file_path} not found, creating it instead')")
#                 # Create the file if it doesn't exist
#                 code_parts.append(f"    os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f'        f.write("""{escaped_content}""")')
#                 code_parts.append(f"    print('✅ Created {file_path}')")
            
#             elif operation == "replace":
#                 code_parts.append(f"print('📝 Replacing file: {file_path}')")
#                 code_parts.append(f"if os.path.exists('{file_path}'):")
#                 code_parts.append(f"    print('⚠️  WARNING: Replace operation will overwrite entire file')")
#                 code_parts.append(f"    # Backup original content")
#                 code_parts.append(f"    with open('{file_path}', 'r', encoding='utf-8') as f:")
#                 code_parts.append(f"        original_content = f.read()")
#                 code_parts.append(f"    print(f'📄 Original file size: {{len(original_content)}} characters')")
#                 code_parts.append(f"    # Write new content")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f'        f.write("""{escaped_content}""")')
#                 code_parts.append(f"    print('✅ Replaced {file_path}')")
#                 code_parts.append(f"else:")
#                 code_parts.append(f"    print('❌ File {file_path} not found, creating it instead')")
#                 code_parts.append(f"    os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
#                 code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
#                 escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
#                 code_parts.append(f'        f.write("""{escaped_content}""")')
#                 code_parts.append(f"    print('✅ Created {file_path}')")
            
#             code_parts.append("")
        
#         code_parts.append("print('✅ AI-powered code changes completed')")
        
#         return "\n".join(code_parts) 


# ai_service.py

import openai
import os
import json
import re
import logging
from dotenv import load_dotenv
import requests

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

REPO_FILE_LIMIT = 20

class AIService:
    def __init__(self):
        self.model = GROQ_MODEL
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

    def analyze_prompt(self, prompt, repo_structure):
        system_prompt = self._build_system_prompt(repo_structure)
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1800,
            "temperature": 0.4
        }

        try:
            response = requests.post(GROQ_ENDPOINT, headers=self.headers, json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"].strip()

            with open("llm_debug_log.json", "w") as f:
                json.dump({"system_prompt": system_prompt, "user_prompt": prompt, "response": content}, f, indent=2)

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                match = re.search(r'\{.*\}', content, re.DOTALL)
                if match:
                    return json.loads(match.group())
                else:
                    raise ValueError("LLM output could not be parsed as JSON")

        except Exception as e:
            logging.exception("LLM call failed")
            raise e

    def generate_code_changes(self, file_path, edits):
        lines = [f"with open(\"{file_path}\", \"r\") as f:",
                 "    lines = f.readlines()"]

        for edit in edits:
            if isinstance(edit, dict) and "line" in edit and "content" in edit:
                line_num = edit["line"]
                content = edit["content"]
                insert_index = max(0, line_num - 1)
                lines.append(f"lines.insert({insert_index}, \"{content}\\n\")")
            else:
                logging.warning(f"Skipping invalid edit entry: {edit}")

        lines.append(f"with open(\"{file_path}\", \"w\") as f:")
        lines.append("    f.writelines(lines)")
        return "\n".join(lines)

    def _build_system_prompt(self, repo_structure):
        trimmed = repo_structure[:REPO_FILE_LIMIT]
        return f"""
You are an AI coding assistant. Based on the user's prompt and the structure of a GitHub repository, respond with a JSON object specifying what code to modify.

Only respond with valid JSON. No commentary. Use this format:
{{
  "file": "path/to/file",
  "edits": [
    {{ "line": 12, "content": "// added line" }},
    {{ "line": 25, "content": "console.log('done');" }}
  ]
}}

Each edit must be an object with both "line" and "content" fields. Do NOT return just an array of strings.

Repo Structure:
{chr(10).join(trimmed)}
        """
