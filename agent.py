#!/usr/bin/env python3
"""
Scrum Master AI Agent - Jira Cloud Integration
Uses Claude API with Jira API for sprint analysis
"""

import os
import json
from datetime import datetime
import anthropic
from jira import JIRA

class ScramMasterAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-7"
        self.jira_url = os.environ.get("JIRA_URL")
        self.jira_email = os.environ.get("JIRA_EMAIL")
        self.jira_token = os.environ.get("JIRA_API_TOKEN")
        self.jira_project = os.environ.get("JIRA_PROJECT_KEY")
        self.jira = None
        self.sprint_data = None

    def connect_jira(self):
        """Connect to Jira Cloud"""
        try:
            self.jira = JIRA(
                server=self.jira_url,
                basic_auth=(self.jira_email, self.jira_token)
            )
            print("[OK] Jira connected successfully\n")
            return True
        except Exception as e:
            print(f"[ERROR] Jira connection failed: {e}")
            return False

    def fetch_sprint_data(self):
        """Fetch active sprint from Jira"""
        try:
            board = self.jira.boards(projectKey=self.jira_project)[0]
            sprints = self.jira.sprints(board.id, state='active')

            if not sprints:
                print("[ERROR] No active sprint found")
                return False

            sprint = sprints[0]
            issues = self.jira.search_issues(f'sprint={sprint.id}')

            self.sprint_data = {
                'sprint_name': sprint.name,
                'sprint_id': sprint.id,
                'issues': []
            }

            for issue in issues:
                self.sprint_data['issues'].append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                    'story_points': issue.fields.customfield_10016 or 0,
                    'status': issue.fields.status.name,
                    'priority': issue.fields.priority.name if issue.fields.priority else 'None'
                })

            print(f"[OK] Sprint loaded: {len(issues)} issues\n")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to fetch sprint data: {e}")
            return False

    def analyze_sprint(self, question):
        """Analyze sprint with Claude"""
        if not self.sprint_data:
            print("[ERROR] No sprint data. Call fetch_sprint_data() first")
            return

        context = f"""
# JIRA SPRINT DATA
Generated: {datetime.now().isoformat()}
Sprint: {self.sprint_data['sprint_name']}

## ISSUES ({len(self.sprint_data['issues'])} total)
{json.dumps(self.sprint_data['issues'], indent=2)}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=[
                    {"type": "text", "text": "You are a Scrum Master AI assistant analyzing Jira sprint data."},
                    {"type": "text", "text": context, "cache_control": {"type": "ephemeral"}}
                ],
                messages=[{"role": "user", "content": question}]
            )
            print(response.content[0].text)
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")

    def interactive_mode(self):
        """Start interactive Q&A"""
        print("Scrum Master AI - Interactive Mode")
        print("Type 'exit' to quit\n")

        while True:
            question = input("Ask about sprint: ").strip()
            if question.lower() == 'exit':
                break
            if question:
                self.analyze_sprint(question)
                print()

if __name__ == "__main__":
    agent = ScramMasterAgent()

    if not agent.connect_jira():
        exit(1)

    if not agent.fetch_sprint_data():
        exit(1)

    agent.interactive_mode()
