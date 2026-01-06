# GitHub Codespaces Setup for Ralph

This directory contains the configuration for developing and testing Ralph in GitHub Codespaces - a cloud-based development environment.

## 🚀 Quick Start

### Option 1: Launch from GitHub Web
1. Go to the repository on GitHub: `https://github.com/gustavoleo/ralph-claude-code`
2. Click the **Code** button (green button)
3. Select the **Codespaces** tab
4. Click **Create codespace on [branch-name]**
5. Wait 2-3 minutes for the environment to build

### Option 2: Launch from URL
Open this URL in your browser (replace `USERNAME/REPO` with your fork):
```
https://github.com/codespaces/new?repo=USERNAME/REPO
```

## 📦 What's Included

The Codespace comes pre-configured with:

- **Ubuntu Linux** (Debian Bookworm base)
- **Node.js 20** - Latest LTS version
- **tmux** - Terminal multiplexer for Ralph monitoring
- **jq** - JSON processor for status tracking
- **BATS** - Bash testing framework
- **Claude Code CLI** - `@anthropic-ai/claude-code` package
- **Ralph** - Installed globally with all commands
- **VS Code Extensions**:
  - Bash IDE
  - ShellCheck (linting)
  - Shell Format
  - Bash Debug
  - BATS syntax support

## ✅ Verification

After the Codespace starts, verify the installation:

```bash
# Check Ralph commands
ralph --help
ralph-setup --help
ralph-monitor --help
ralph-import --help

# Check dependencies
tmux -V
jq --version
bats --version

# Run the test suite
npm test
```

## 🧪 Testing Ralph

### Run All Tests
```bash
# Full test suite (97 tests)
npm test

# Unit tests only
npm run test:unit

# Integration tests only
npm run test:integration

# Error detection tests
./tests/test_error_detection.sh
./tests/test_stuck_loop_detection.sh
```

### Create a Test Project
```bash
# Create a sample Ralph project
ralph-setup my-test-project
cd my-test-project

# Edit PROMPT.md with your requirements
# Edit @fix_plan.md with tasks

# Start Ralph (without monitoring in Codespaces)
ralph --calls 10 --timeout 5
```

### Test with Monitoring (tmux)
```bash
# Start Ralph with integrated tmux monitoring
ralph --monitor --calls 10

# tmux controls:
# Ctrl+B then D - Detach from session
# Ctrl+B then ← / → - Switch panes
```

## 🛠️ Development Workflow

### Making Changes
```bash
# Edit Ralph scripts
vim ralph_loop.sh
vim lib/circuit_breaker.sh

# Run tests to verify changes
npm test

# Test installation process
./install.sh
ralph --version
```

### Testing Installation
```bash
# Uninstall Ralph
./install.sh uninstall

# Reinstall to test installation script
./install.sh

# Verify all commands work
ralph --status
```

## 📝 Configuration Files

- **devcontainer.json** - Main Codespace configuration
  - Base image: Node.js 20 on Debian Bookworm
  - Features: Git, Common utilities, Zsh
  - VS Code extensions for bash development

- **post-create.sh** - Runs after Codespace creation
  - Installs system dependencies (tmux, jq)
  - Installs BATS testing framework
  - Installs Claude Code CLI
  - Runs Ralph installation script
  - Verifies all components

## 🔧 Customization

### Modify Dependencies
Edit `.devcontainer/post-create.sh` to add or remove packages:
```bash
# Add new system packages
sudo apt-get install -y your-package

# Add new npm packages
npm install -g your-package
```

### Change VS Code Extensions
Edit `.devcontainer/devcontainer.json` in the `customizations.vscode.extensions` section:
```json
"extensions": [
  "your-extension-id"
]
```

### Rebuild Codespace
After changing configuration:
1. Open Command Palette (F1 or Ctrl+Shift+P)
2. Select: **Codespaces: Rebuild Container**
3. Wait for rebuild to complete

## 💡 Tips

### Performance
- Codespaces run on powerful VMs (2-32 cores available)
- Perfect for running Ralph's test suite
- Ideal for testing Ralph loops with actual Claude Code CLI

### Persistence
- Files in the workspace are persisted
- Installed packages via post-create script run each time
- Use `/workspaces/ralph-claude-code` as your working directory

### Troubleshooting

**Ralph commands not found:**
```bash
# Re-run installation
./install.sh
source ~/.bashrc
```

**Tests failing:**
```bash
# Reinstall BATS
npm install -g bats bats-support bats-assert

# Check for missing dependencies
which tmux jq bats
```

**Codespace won't start:**
- Check GitHub status page
- Try rebuilding the container
- Delete and recreate the Codespace

## 🔗 Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Dev Container Specification](https://containers.dev/)
- [Ralph Documentation](../README.md)
- [VS Code in Codespaces](https://code.visualstudio.com/docs/remote/codespaces)

## 🎯 Use Cases

### For Contributors
- Test changes in clean environment
- Run full test suite on cloud VM
- Develop new features without local setup
- Verify installation process works

### For Users
- Try Ralph without installing locally
- Test Ralph on different projects
- Quick demonstration environment
- Learn Ralph in isolated sandbox

## ⚙️ Technical Details

**Container Specs:**
- Base: `mcr.microsoft.com/devcontainers/javascript-node:20-bookworm`
- User: `vscode` (UID: 1000, GID: 1000)
- Shell: Bash (with Zsh available)
- Capabilities: SYS_PTRACE for debugging

**Installation Locations:**
- Ralph commands: `~/.local/bin/`
- Ralph templates: `~/.ralph/templates/`
- Ralph scripts: `~/.ralph/`
- Libraries: `~/.ralph/lib/`

---

**Ready to develop?** Launch your Codespace and start contributing to Ralph! 🚀
