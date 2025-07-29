# 🤖 Autonomus PR submission capable Coding Agent

This is a sandboxed AI coding agent that can automatically create GitHub pull requests based on natural language prompts. Users provide a public GitHub repository URL and a coding prompt, and the agent clones the repo, edits the code, and submits a pull request, all of this in an isolated sandbox environment.

---

## ✨ Features

- 🌐 Clean, minimal Swiss-style frontend (Next.js)
- 🧠 AI agent responds to coding prompts
- 📂 GitHub repo cloned in a sandbox (Docker)
- ✏️ Agent edits files based on prompt
- 🔀 Git operations: commit, branch, and PR creation
- 📡 Real-time status updates via Server-Sent Events (SSE)
- 💾 History of code fixes stored in `localStorage` promoting privacy-first application

---

## 🧰 Tech Stack

| Layer       | Technology         |
|-------------|--------------------|
| Frontend    | React, Next.js     |
| Backend     | FastAPI            |
| Sandboxing  | Docker             |
| Agent Logic | Gemini             |
| GitHub      | REST API + Git CLI |

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Node.js 18+
- Python 3.10+
- Docker
- GitHub Personal Access Token (for PR creation)

---

### 🔜 More instructions rolling out soon.
