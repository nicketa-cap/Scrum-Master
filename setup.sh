#!/bin/bash
# Quick-start setup script for Enhanced Scrum Master Agent

echo "🚀 Enhanced Scrum Master Agent - Quick Start Setup"
echo "=================================================="
echo ""

# Check Python version
python --version || { echo "❌ Python not found. Please install Python 3.8+"; exit 1; }

echo "✅ Python found"
echo ""

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv

    # Activate venv
    if [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate  # Windows Git Bash
    elif [ -f "venv/bin/activate" ]; then
        source venv/bin/activate      # Linux/Mac
    fi
fi

echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "🔑 Setting up API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ ANTHROPIC_API_KEY not set"
    echo ""
    echo "Set it with:"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    exit 1
else
    echo "✅ ANTHROPIC_API_KEY is set"
fi

echo ""
echo "📋 Checking Excel files..."
for file in leave-tracker.xlsx capacity-planner.xlsx dependency-matrix.xlsx; do
    if [ -f "$file" ]; then
        echo "  ✅ $file found"
    else
        echo "  ❌ $file NOT found"
    fi
done

echo ""
echo "🎯 Ready to run! Choose an option:"
echo ""
echo "1. Interactive mode (recommended):"
echo "   python enhanced_agent.py"
echo ""
echo "2. Python REPL:"
echo "   python"
echo "   >>> from enhanced_agent import ScramMasterAgent"
echo "   >>> agent = ScramMasterAgent()"
echo "   >>> agent.load_data()"
echo "   >>> agent.analyze_sprint('Your question here')"
echo ""
