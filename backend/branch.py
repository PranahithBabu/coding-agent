import requests


def list_branches(token, username, repo_name):
    """
    Lists branches in a GitHub repository using GitHub REST API v3 and suggests a new branch name.
    """
    url = f"https://api.github.com/repos/{username}/{repo_name}/branches"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    suggested_branch_name = None

    if response.status_code == 200:
        branches = response.json()
        branch_names = [branch["name"] for branch in branches]
        print(f"\n✅ Branches in {username}/{repo_name}:")
        for branch_name in branch_names:
            print(f"- {branch_name}")

        # Check for existing 'backspace-agent' branches and suggest a new name
        agent_branches = [name for name in branch_names if name.startswith("backspace-agent")]
        if agent_branches:
            # Find the highest number used in the suffix
            max_num = 0
            for branch in agent_branches:
                parts = branch.split('-')
                if len(parts) > 2 and parts[2].isdigit():
                    max_num = max(max_num, int(parts[2]))
            suggested_branch_name = f"backspace-agent-{max_num + 1}"
            print(f"\nSuggested new branch name: {suggested_branch_name}")
        else:
            suggested_branch_name = "backspace-agent-1"
            print("\nSuggested new branch name: backspace-agent-1")

    else:
        print(f"\n❌ Failed to list branches. Status Code: {response.status_code}")
        print("Response:", response.json())

    return suggested_branch_name
