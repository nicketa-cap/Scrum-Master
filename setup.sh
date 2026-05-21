#!/bin/bash
# Quick-start setup for Scrum Master Agent - Jira Integration

echo "Scrum Master Agent - Jira Integration Setup"
echo "==========================================="
echo ""

# Check Python
python --version || { echo "[ERROR] Python not found. Install Python 3.8+"; exit 1; }
echo "[OK] Python found"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python -m venv venv
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    elif [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    fi
fi

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "[INFO] Setting up environment variables..."
echo ""
echo "Required:"
echo "  export ANTHROPIC_API_KEY='your-api-key'"
echo "  export JIRA_URL='https://your-org.atlassian.net'"
echo "  export JIRA_EMAIL='your-email@company.com'"
echo "  export JIRA_API_TOKEN='your-jira-token'"
echo "  export JIRA_PROJECT_KEY='PROJ'"
echo ""

if [ -z "$ANTHROPIC_API_KEY" ] || [ -z "$JIRA_URL" ]; then
    echo "[WARNING] API keys not set. Run setup commands above."
    echo ""
fi

echo "[OK] Setup complete. Run: python agent.py"
