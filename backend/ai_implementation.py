import json
import re

MODEL_NAME="gemma2-9b-it"

def identify_and_modify_file(edit_prompt, sbx, client, repo_dir):

    print("\n📂 Scanning repo files...")
    file_listing = sbx.run_code(f"!( cd {repo_dir} && find . -type f )")
    repo_files = [f.strip().lstrip("./") for f in file_listing.logs.stdout if not f.endswith(".git")]

    if not repo_files:
        print("❌ No files found in repository.")
        return

    # Step 1: Use LLM to decide which files to create or modify
    print("🧠 LLM analyzing intent and repo file list...")

    routing_prompt = f"""
You are a smart assistant for a code-editing agent.

Given:
- A user prompt describing a desired change.
- A list of files in a repository.

Your job:
- Identify any files that need to be **created**
- Identify any files that need to be **modified**

Respond ONLY with this JSON format:
{{
  "create": [
    {{"file": "relative/path.js", "reason": "why this file is created"}}
  ],
  "modify": [
    {{"file": "relative/path.html", "reason": "why this file needs to be modified"}}
  ]
}}

User prompt:
{edit_prompt}

Repo files:
{chr(10).join(repo_files)}
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a code modification planner."},
            {"role": "user", "content": routing_prompt.strip()}
        ]
    )

    match = re.search(r"\{.*\}", response.choices[0].message.content, re.DOTALL)
    decision_json = json.loads(match.group()) if match else {"create": [], "modify": []}

    # Step 2: File Creation
    for entry in decision_json.get("create", []):
        filename = entry["file"]
        reason = entry.get("reason", "unspecified")
        print(f"\n📁 Creating new file: {filename} — {reason}")

        create_prompt = f"""
User prompt:
{edit_prompt}

Create a new file: {filename}
Reason: {reason}
Give the entire content of the file in a Python string.
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a code generator that writes full file content."},
                {"role": "user", "content": create_prompt.strip()}
            ]
        )

        file_content = response.choices[0].message.content.strip()
        if "```" in file_content:
            file_content = file_content.split("```")[1].split("```")[0]

        write_code = f"""with open('{repo_dir}/{filename}', 'w') as f:
    f.write({json.dumps(file_content)})
print("File created: {filename}")
"""
        sbx.run_code(write_code)

        # Optional: show created content
        verify = sbx.run_code(f"!( cd {repo_dir} && cat {filename} )")
        print(f"\n📄 Created {filename}:")
        for line in verify.logs.stdout:
            print(line)

    # Step 3: Modify existing files
    for entry in decision_json.get("modify", []):
        filename = entry["file"]
        file_path = f"{repo_dir}/{filename}"

        print(f"\n📝 Modifying file: {filename} — {entry.get('reason', 'unspecified')}")

        read_command = f"!( cd {repo_dir} && cat {filename} )"
        execution = sbx.run_code(read_command)
        file_content = "".join(execution.logs.stdout)

        if not file_content.strip():
            print(f"⚠️ Skipping empty or unreadable file: {filename}")
            continue

        file_type = filename.split('.')[-1].lower()
        lang_desc = {
            "py": "a Python file",
            "js": "a JavaScript file",
            "css": "a CSS file",
            "html": "an HTML file",
            "md": "a Markdown file",
        }.get(file_type, f"a .{file_type} file")

        mod_system_prompt = f"""
You're a code-editing assistant.

Generate a Python script that:
- Opens the file {file_path}
- Applies the user's edit as described
- Overwrites the file
- Prints 'Modification successful!'

Only modify what's necessary. Use string search logic, not hardcoded line numbers.

This file is {lang_desc}.
""".strip()

        mod_user_prompt = f"""
File content:
{file_content}

User request:
{edit_prompt}
""".strip()

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": mod_system_prompt},
                {"role": "user", "content": mod_user_prompt}
            ]
        )

        modification_code = response.choices[0].message.content
        if "```python" in modification_code:
            modification_code = modification_code.split("```python")[1].split("```")[0]
        elif "```" in modification_code:
            modification_code = modification_code.split("```")[1]

        print(f"\n🧾 Generated modification script:\n{modification_code}")

        execution = sbx.run_code(modification_code)

        if execution.logs.stderr:
            print("⚠️ Errors during modification:")
            for log in execution.logs.stderr:
                print(log)

        # Git diff
        diff_check = sbx.run_code(f"!( cd {repo_dir} && git diff {filename} )")
        if diff_check.logs.stdout:
            print(f"\n✅ File changed: {filename}")
            for line in diff_check.logs.stdout:
                print(line)
        else:
            print(f"\n❌ No changes detected in {filename}.")

        # Final content
        final = sbx.run_code(f"!( cd {repo_dir} && cat {filename} )")
        print(f"\n📄 Final content of {filename}:")
        for line in final.logs.stdout:
            print(line)
