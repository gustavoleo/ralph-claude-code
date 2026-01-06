#!/bin/bash

set -e

echo "🚀 Setting up Ralph for Claude Code development environment..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update -qq

# Install system dependencies
echo "📦 Installing system dependencies (tmux, jq)..."
sudo apt-get install -y tmux jq > /dev/null 2>&1

# Install BATS testing framework
echo "🧪 Installing BATS testing framework..."
npm install -g bats bats-support bats-assert --silent 2>/dev/null || true

# Install Claude Code CLI
echo "🤖 Installing Claude Code CLI..."
npm install -g @anthropic-ai/claude-code --silent 2>/dev/null || true

# Install Ralph globally
echo "🔧 Installing Ralph globally..."
chmod +x install.sh
./install.sh

# Verify installation
echo ""
echo "✅ Installation complete! Verifying..."
echo ""

# Check installed commands
if command -v ralph &> /dev/null; then
    echo "✓ ralph command available"
else
    echo "✗ ralph command not found"
fi

if command -v ralph-setup &> /dev/null; then
    echo "✓ ralph-setup command available"
else
    echo "✗ ralph-setup command not found"
fi

if command -v ralph-monitor &> /dev/null; then
    echo "✓ ralph-monitor command available"
else
    echo "✗ ralph-monitor command not found"
fi

if command -v ralph-import &> /dev/null; then
    echo "✓ ralph-import command available"
else
    echo "✗ ralph-import command not found"
fi

if command -v tmux &> /dev/null; then
    echo "✓ tmux available"
else
    echo "✗ tmux not found"
fi

if command -v jq &> /dev/null; then
    echo "✓ jq available"
else
    echo "✗ jq not found"
fi

if command -v bats &> /dev/null; then
    echo "✓ bats testing framework available"
else
    echo "✗ bats not found"
fi

echo ""
echo "🎉 Ralph development environment is ready!"
echo ""
echo "Quick Start:"
echo "  1. Run tests: npm test"
echo "  2. Create test project: ralph-setup test-project"
echo "  3. Check Ralph status: ralph --status"
echo "  4. View help: ralph --help"
echo ""
echo "See README.md for full documentation."
echo ""
