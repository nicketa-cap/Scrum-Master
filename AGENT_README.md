# Scrum Master AI Agent - Jira Integration

AI-powered sprint analysis using Claude API and Jira Cloud integration.

## Setup

### 1. Install Dependencies
```bash
bash setup.sh
```

### 2. Configure Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` — Get from https://console.anthropic.com
- `JIRA_URL` — Your Jira cloud URL (e.g., https://company.atlassian.net)
- `JIRA_EMAIL` — Your Jira email
- `JIRA_API_TOKEN` — Generate at https://id.atlassian.com/manage-profile/security/api-tokens
- `JIRA_PROJECT_KEY` — Your project key (e.g., SCRUM, PROJ)

**Set them:**
```bash
export ANTHROPIC_API_KEY='your-key'
export JIRA_URL='https://company.atlassian.net'
export JIRA_EMAIL='user@company.com'
export JIRA_API_TOKEN='your-token'
export JIRA_PROJECT_KEY='PROJ'
```

## Usage

### Interactive Mode
```bash
python agent.py
```

Then ask questions:
- "What's our sprint capacity?"
- "Who's overloaded?"
- "Show task dependencies"
- "Recommend task assignments"

### Python Integration
```python
from agent import ScramMasterAgent

agent = ScramMasterAgent()
agent.connect_jira()
agent.fetch_sprint_data()
agent.analyze_sprint("What are our sprint risks?")
```

## Features

- Fetches active sprint from Jira
- Analyzes team capacity and workload
- Identifies task dependencies
- Provides AI recommendations
- Uses Claude API with prompt caching for efficiency

## Requirements

- Python 3.8+
- Anthropic API key
- Jira Cloud account with API access
