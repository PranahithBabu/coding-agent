#!/usr/bin/env python3
"""
Practice: Basic AI Service for code modification
Starting with simple functionality - will be enhanced step by step
"""

import os
import json
import aiohttp
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama3-8b-8192"
    
    async def analyze_prompt(self, prompt: str, repo_structure: List[str]) -> Dict:
        """
        Step 4: Enhanced prompt analysis with file content understanding
        This analyzes existing files to make intelligent decisions
        """
        system_prompt = """You are an AI coding assistant that helps users modify code.

Your job is to:
1. Understand what the user wants to change
2. Analyze existing file content to make intelligent decisions
3. Determine which files need to be modified
4. Generate specific code changes

Available files in the repository:
{repo_files}

File content analysis:
{file_analysis}

CRITICAL RULES:
- Respond with ONLY a valid JSON object
- ALWAYS provide complete content for each file
- For CSS files: Include actual CSS rules, not empty strings
- For HTML files: Include complete HTML elements
- For JavaScript files: Include complete functions
- Use file content analysis to make intelligent decisions about operations
- If a file exists and has content, prefer "append" over "create"
- If modifying existing content, be specific about what to change

JSON format:
{{
    "action": "create|modify",
    "files": [
        {{
            "path": "file_path",
            "operation": "create|modify|append",
            "content": "complete code content here",
            "description": "what this change does"
        }}
    ],
    "summary": "brief description of all changes"
}}

Examples:
- For "Add a blue button": 
  - HTML: "<button class=\"blue-btn\">Click me</button>"
  - CSS: ".blue-btn {{ background-color: blue; color: white; padding: 10px 20px; }}"
- For "Change button color": 
  - CSS: ".button {{ background-color: red; }}"
- For "Add new function": 
  - JS: "function newFunction() {{ console.log('Hello'); }}"
"""

        # Step 4: Analyze existing file content
        file_analysis = {}
        for file_path in repo_structure:
            analysis = await self.analyze_file_content(file_path)
            file_analysis[file_path] = analysis
        
        # Format file analysis for the prompt
        file_analysis_text = ""
        for file_path, analysis in file_analysis.items():
            if analysis["exists"]:
                file_analysis_text += f"\n{file_path}:"
                file_analysis_text += f"\n  - Type: {analysis['file_type']}"
                file_analysis_text += f"\n  - Size: {analysis['size']} characters, {analysis['lines']} lines"
                file_analysis_text += f"\n  - Has CSS: {analysis['has_css']}"
                file_analysis_text += f"\n  - Has JS: {analysis['has_js']}"
                file_analysis_text += f"\n  - Has HTML: {analysis['has_html']}"
            else:
                file_analysis_text += f"\n{file_path}: File does not exist (will be created if needed)"

        user_prompt = f"""
User request: {prompt}

Please analyze this request and provide the necessary code changes in JSON format.
Use the file content analysis to make intelligent decisions about operations.
"""

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt.format(
                        repo_files="\n".join(repo_structure),
                        file_analysis=file_analysis_text
                    )},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        
                        print(f"🤖 Raw AI response: {content}")
                        
                        # Simple JSON parsing
                        content = content.strip()
                        
                        # Remove markdown code blocks if present
                        if content.startswith('```json'):
                            content = content[7:]
                        if content.startswith('```'):
                            content = content[3:]
                        if content.endswith('```'):
                            content = content[:-3]
                        
                        content = content.strip()
                        
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError as e:
                            print(f"JSON parsing error: {e}")
                            print(f"Cleaned content: {content}")
                            
                            # Try to find JSON within the content
                            json_start = content.find('{')
                            json_end = content.rfind('}') + 1
                            
                            if json_start != -1 and json_end != 0:
                                json_str = content[json_start:json_end]
                                try:
                                    return json.loads(json_str)
                                except json.JSONDecodeError:
                                    # Try to clean up the JSON string further
                                    json_str = json_str.replace('\n', ' ').replace('    ', ' ')
                                    json_str = json_str.replace('\\n', ' ').replace('\\t', ' ')
                                    try:
                                        return json.loads(json_str)
                                    except json.JSONDecodeError:
                                        # If still failing, try to complete the JSON
                                        if json_str.count('{') > json_str.count('}'):
                                            json_str += '}'
                                        if json_str.count('[') > json_str.count(']'):
                                            json_str += ']'
                                        return json.loads(json_str)
                            else:
                                raise Exception("Could not find JSON in AI response")
                    else:
                        error_text = await response.text()
                        print(f"Groq API error: {response.status} - {error_text}")
                        raise Exception(f"Groq API error: {response.status}")
                        
        except Exception as e:
            print(f"Error in AI analysis: {e}")
            # Simple fallback
            return {
                "action": "modify",
                "files": [
                    {
                        "path": "index.html",
                        "operation": "append",
                        "content": f"<!-- {prompt} -->",
                        "description": f"Add comment for: {prompt}"
                    }
                ],
                "summary": f"Add comment for: {prompt}"
            }
    
    def generate_code_changes(self, analysis: Dict) -> str:
        """
        Step 4: Generate intelligent executable code based on AI analysis
        This converts the AI analysis into actual Python code that can be executed
        """
        code_parts = []
        
        code_parts.append("import os")
        code_parts.append("import re")
        code_parts.append("")
        code_parts.append("print('🤖 Executing AI-generated code changes...')")
        code_parts.append("")
        
        # List current files
        code_parts.append("print('📁 Current directory contents:')")
        code_parts.append("files = os.listdir('.')")
        code_parts.append("for file in files:")
        code_parts.append("    print(f'  - {file}')")
        code_parts.append("")
        
        # Process each file change
        for file_change in analysis.get("files", []):
            file_path = file_change.get("path", "")
            operation = file_change.get("operation", "append")
            content = file_change.get("content", "")
            description = file_change.get("description", "")
            
            code_parts.append(f"# {description}")
            
            if operation == "create":
                code_parts.append(f"print('📝 Creating file: {file_path}')")
                code_parts.append(f"os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
                code_parts.append(f"with open('{file_path}', 'w', encoding='utf-8') as f:")
                escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
                code_parts.append(f'    f.write("""{escaped_content}""")')
                code_parts.append(f"print('✅ Created {file_path}')")
                
            elif operation == "modify":
                code_parts.append(f"print('📝 Intelligently modifying file: {file_path}')")
                code_parts.append(f"if os.path.exists('{file_path}'):")
                code_parts.append(f"    with open('{file_path}', 'r', encoding='utf-8') as f:")
                code_parts.append("        current_content = f.read()")
                code_parts.append("    print(f'📄 Current file size: {{len(current_content)}} characters')")
                code_parts.append("    # Intelligent modification based on file type")
                escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
                code_parts.append(f"    new_content = current_content + '\\n\\n' + '{escaped_content}'")
                code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
                code_parts.append("        f.write(new_content)")
                code_parts.append(f"    print('✅ Modified {file_path}')")
                code_parts.append("else:")
                code_parts.append(f"    print('❌ File {file_path} not found, creating it instead')")
                code_parts.append(f"    os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
                code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
                escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
                code_parts.append(f'        f.write("""{escaped_content}""")')
                code_parts.append(f"    print('✅ Created {file_path}')")
                
            elif operation == "append":
                code_parts.append(f"print('📝 Appending to file: {file_path}')")
                code_parts.append(f"if os.path.exists('{file_path}'):")
                code_parts.append(f"    with open('{file_path}', 'r', encoding='utf-8') as f:")
                code_parts.append("        current_content = f.read()")
                code_parts.append("    print(f'📄 Current file size: {{len(current_content)}} characters')")
                escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
                code_parts.append(f"    new_content = current_content + '\\n\\n' + '{escaped_content}'")
                code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
                code_parts.append("        f.write(new_content)")
                code_parts.append(f"    print('✅ Appended to {file_path}')")
                code_parts.append("else:")
                code_parts.append(f"    print('❌ File {file_path} not found, creating it instead')")
                code_parts.append(f"    os.makedirs(os.path.dirname('{file_path}'), exist_ok=True)")
                code_parts.append(f"    with open('{file_path}', 'w', encoding='utf-8') as f:")
                escaped_content = content.replace('"', '\\"').replace('\n', '\\n')
                code_parts.append(f'        f.write("""{escaped_content}""")')
                code_parts.append(f"    print('✅ Created {file_path}')")
            
            code_parts.append("")
        
        code_parts.append("print('✅ AI-powered code changes completed')")
        
        return "\n".join(code_parts)
    
    def validate_generated_code(self, analysis: Dict) -> Dict:
        """
        Step 5: Validate generated code for syntax and logic
        This ensures the generated code is safe and functional
        """
        validation_results = {
            "valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        for file_change in analysis.get("files", []):
            file_path = file_change.get("path", "")
            operation = file_change.get("operation", "")
            content = file_change.get("content", "")
            
            # Validate file path
            if not file_path:
                validation_results["errors"].append(f"Missing file path in file change")
                validation_results["valid"] = False
                continue
            
            # Validate operation
            valid_operations = ["create", "modify", "append", "replace"]
            if operation not in valid_operations:
                validation_results["warnings"].append(f"Unknown operation '{operation}' for {file_path}")
            
            # Validate content
            if not content and operation != "replace":
                validation_results["warnings"].append(f"Empty content for {file_path} with operation {operation}")
            
            # File type specific validation
            file_type = self._get_file_type(file_path)
            
            if file_type == "html":
                if not content.startswith('<') and not content.startswith('<!--'):
                    validation_results["warnings"].append(f"HTML content for {file_path} doesn't start with HTML tag")
            
            elif file_type == "css":
                if not any(char in content for char in ['{', ':', ';']):
                    validation_results["warnings"].append(f"CSS content for {file_path} doesn't look like valid CSS")
            
            elif file_type == "javascript":
                if not any(char in content for char in ['function', 'const', 'let', 'var', '//']):
                    validation_results["warnings"].append(f"JavaScript content for {file_path} doesn't look like valid JS")
        
        return validation_results
    
    async def analyze_file_content(self, file_path: str) -> Dict:
        """
        Step 4: Analyze existing file content to make intelligent decisions
        This helps the AI understand what's already in the files before making changes
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "exists": False,
                    "content": "",
                    "file_type": self._get_file_type(file_path),
                    "size": 0
                }
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "exists": True,
                "content": content,
                "file_type": self._get_file_type(file_path),
                "size": len(content),
                "lines": len(content.split('\n')),
                "has_css": 'style' in content.lower() or '.css' in content.lower(),
                "has_js": 'script' in content.lower() or 'function' in content.lower(),
                "has_html": '<html' in content.lower() or '<body' in content.lower()
            }
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
            return {
                "exists": False,
                "content": "",
                "file_type": self._get_file_type(file_path),
                "size": 0,
                "error": str(e)
            }
    
    def _get_file_type(self, file_path: str) -> str:
        """Determine file type based on extension"""
        ext = file_path.lower().split('.')[-1] if '.' in file_path else ''
        if ext in ['html', 'htm']:
            return 'html'
        elif ext == 'css':
            return 'css'
        elif ext in ['js', 'javascript']:
            return 'javascript'
        elif ext == 'py':
            return 'python'
        else:
            return 'unknown' 