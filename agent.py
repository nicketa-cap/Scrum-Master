#!/usr/bin/env python3
"""
Enhanced Scrum Master AI Agent - Sprint Capacity & Leave Optimizer
Uses Claude API with prompt caching for intelligent analysis and interactive Q&A
"""

import os
import json
import pandas as pd
from datetime import datetime
import anthropic

class ScramMasterAgent:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = "claude-opus-4-7"
        self.leave_df = None
        self.capacity_df = None
        self.dependency_df = None
        self.sprint_context = None

    def load_data(self):
        """Load data from Excel files"""
        try:
            self.leave_df = pd.read_excel("leave-tracker.xlsx")
            self.capacity_df = pd.read_excel("capacity-planner.xlsx")
            self.dependency_df = pd.read_excel("dependency-matrix.xlsx")
            print("✅ Data loaded successfully\n")
            return True
        except Exception as e:
            print(f"❌ Error loading files: {e}")
            return False

    def prepare_sprint_context(self):
        """Prepare comprehensive sprint context for caching"""
        context = f"""
# SPRINT DATA CONTEXT
Generated: {datetime.now().isoformat()}

## LEAVE SCHEDULE
{self.leave_df.to_markdown(index=False)}

## TEAM CAPACITY
{self.capacity_df.to_markdown(index=False)}

## TASK DEPENDENCIES
{self.dependency_df.to_markdown(index=False)}

## CAPACITY SUMMARY
"""

        # Add capacity analysis
        total_available = self.capacity_df['Available Hours'].sum()
        total_allocated = self.capacity_df['Allocated Work'].sum()
        utilization = (total_allocated / total_available * 100) if total_available > 0 else 0

        context += f"""
- Total Available Hours: {total_available}
- Total Allocated Work: {total_allocated}
- Team Utilization: {utilization:.1f}%
- Overload Count: {len(self.capacity_df[self.capacity_df['Allocated Work'] > self.capacity_df['Available Hours']])}

## RISK SUMMARY
"""

        # Add risk analysis
        leave_conflicts = 0
        for date, group in self.leave_df.groupby("Date"):
            if len(group) > 1:
                leave_conflicts += 1

        dependency_risks = len(self.dependency_df[
            (self.dependency_df['Backup Resource'].isna()) |
            (self.dependency_df['Backup Resource'] == "")
        ])

        context += f"""
- Leave Conflicts: {leave_conflicts} date(s) with multiple people on leave
- Dependency Risks: {dependency_risks} task(s) without backup coverage
- Capacity Gaps: {len(self.capacity_df[self.capacity_df['Allocated Work'] > self.capacity_df['Available Hours']])} overloaded team member(s)
"""

        self.sprint_context = context
        return context

    def analyze_sprint(self, user_query: str):
        """
        Analyze sprint using Claude API with prompt caching

        Caches the sprint context to avoid reprocessing on each query
        """
        if not self.sprint_context:
            self.prepare_sprint_context()

        system_prompt = [
            {
                "type": "text",
                "text": """You are an expert Scrum Master AI agent specialized in sprint planning, team capacity management, and risk mitigation.

Your capabilities include:
1. **Leave Conflict Analysis**: Identify overlapping leaves that impact sprint delivery
2. **Capacity Planning**: Assess team workload and identify overloaded resources
3. **Dependency Risk Assessment**: Highlight critical tasks without backup coverage
4. **Risk Scoring**: Quantify sprint risks on a scale of 1-10
5. **Recommendations**: Provide actionable advice to improve sprint planning

When analyzing, consider:
- Impact on sprint delivery
- Team member availability
- Backup resource availability
- Workload balance
- Critical path dependencies

Provide clear, structured responses with specific metrics and recommendations."""
            },
            {
                "type": "text",
                "text": self.sprint_context,
                "cache_control": {"type": "ephemeral"}
            }
        ]

        messages = [
            {
                "role": "user",
                "content": user_query
            }
        ]

        print(f"\n🔍 Analyzing: {user_query}")
        print("=" * 60)

        # Stream the response
        with self.client.messages.stream(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=messages,
            thinking={
                "type": "adaptive"
            }
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

        # Print usage stats
        final_message = stream.get_final_message()
        usage = final_message.usage

        print("\n" + "=" * 60)
        print(f"\n📊 Token Usage:")
        print(f"  Input: {usage.input_tokens}")
        print(f"  Cache Write: {getattr(usage, 'cache_creation_input_tokens', 0)}")
        print(f"  Cache Read: {getattr(usage, 'cache_read_input_tokens', 0)}")
        print(f"  Output: {usage.output_tokens}")

        if getattr(usage, 'cache_read_input_tokens', 0) > 0:
            savings = (getattr(usage, 'cache_read_input_tokens', 0) /
                      (usage.input_tokens + getattr(usage, 'cache_read_input_tokens', 0)))
            print(f"  💰 Cache Efficiency: {savings*100:.1f}% of input from cache")

        return full_response

    def generate_risk_score(self):
        """Generate comprehensive sprint risk score"""
        risk_prompt = """Based on the sprint data provided, generate a comprehensive risk assessment.

Provide:
1. Overall Sprint Risk Score (1-10, where 10 is highest risk)
2. Risk breakdown by category:
   - Leave Impact Risk
   - Capacity Risk
   - Dependency Risk
3. Risk Matrix (High/Medium/Low)
4. Top 3 mitigation strategies

Format as JSON for easy parsing."""

        return self.analyze_sprint(risk_prompt)

    def interactive_session(self):
        """Start interactive Q&A session with the agent"""
        print("\n🤖 SCRUM MASTER AI AGENT - Interactive Session")
        print("=" * 60)
        print("Ask questions about sprint planning, capacity, and risks.")
        print("Type 'exit' to end, 'risk' for risk assessment, 'summary' for overview.\n")

        sample_prompts = {
            "risk": "Generate a comprehensive risk assessment for this sprint",
            "summary": "Provide an executive summary of the sprint status",
            "conflicts": "What are the key leave conflicts and their impact?",
            "capacity": "Which team members are overloaded and by how much?",
            "dependencies": "What are the critical dependency risks?",
            "recommendations": "What are the top 5 recommendations to improve this sprint?"
        }

        while True:
            user_input = input("\n💬 Your question (or shortcut): ").strip()

            if user_input.lower() == "exit":
                print("\n✅ Session ended. Goodbye!")
                break

            if user_input.lower() in sample_prompts:
                query = sample_prompts[user_input.lower()]
            elif not user_input:
                print("⚠️ Please enter a question or shortcut")
                continue
            else:
                query = user_input

            self.analyze_sprint(query)

def main():
    """Main entry point"""
    agent = ScramMasterAgent()

    # Load data
    if not agent.load_data():
        return

    # Prepare sprint context (done once, then cached)
    print("📋 Preparing sprint context...")
    agent.prepare_sprint_context()

    # Demo: Show the caching benefit with multiple queries
    print("\n📌 DEMO: Testing Prompt Caching Benefits")
    print("=" * 60)

    # First query - writes to cache
    print("\n🔹 Query 1: Generate risk assessment (cache write)")
    agent.analyze_sprint(
        "Generate a risk assessment summary. What's the overall sprint health score and top 3 risks?"
    )

    # Second query - reads from cache
    print("\n\n🔹 Query 2: Capacity analysis (cache read)")
    agent.analyze_sprint(
        "Analyze team capacity distribution. Are there any bottlenecks?"
    )

    # Third query - reads from cache
    print("\n\n🔹 Query 3: Dependency review (cache read)")
    agent.analyze_sprint(
        "Review critical dependencies. Which tasks have no backup coverage?"
    )

    # Interactive session
    print("\n\n" + "=" * 60)
    print("🎯 Starting interactive Q&A session...")
    print("(Subsequent queries will benefit from cached sprint data)\n")
    agent.interactive_session()

if __name__ == "__main__":
    main()
