# GitHub Actions Repository

This repository contains common GitHub Actions used across multiple projects. The actions are primarily developed with assistance from LLM tools.

**Always follow these instructions first and only fallback to additional search and context gathering if the information here is incomplete or found to be in error.**

## Working Effectively

### Repository Setup and Navigation
- Navigate to repository root: `cd /home/runner/work/actions/actions`
- Check repository status: `git --no-pager status` (takes <1 second)
- View repository structure: `ls -la` (takes <1 second)
- Check recent commits: `git --no-pager log --oneline -10` (takes <1 second)

### Current Repository State
**IMPORTANT**: This repository is currently in early development stage and contains:
- `Readme.md` - Basic project description
- `.github/` directory - For workflows and configurations (created as needed)
- No active GitHub Actions yet - Actions will be added incrementally

### Finding and Working with GitHub Actions
- Search for Action files: `find . -name "*.yml" -o -name "*.yaml" -o -name "action.yml" -o -name "action.yaml"` (takes <1 second)
- List all YAML files: `find . -name "*.yml" -o -name "*.yaml"` (takes <1 second)
- Check workflows directory: `ls -la .github/workflows/` (if it exists)

### Git Workflow
- Check current branch: `git --no-pager branch` (takes <1 second)
- View all branches: `git --no-pager branch -a` (takes <1 second)
- Check for uncommitted changes: `git --no-pager diff` (takes <1 second)
- Stage changes: `git add .` (takes <1 second)
- Commit changes: `git commit -m "description"` (takes <1 second)

### Creating New GitHub Actions
When adding new actions to this repository:

1. **Create action directory structure**:
   ```bash
   mkdir -p my-action
   cd my-action
   ```

2. **Create action.yml file** with standard GitHub Action metadata:
   ```yaml
   name: 'Action Name'
   description: 'Action description'
   inputs:
     input-name:
       description: 'Input description'
       required: true
   outputs:
     output-name:
       description: 'Output description'
   runs:
     using: 'composite'
     steps:
       - run: echo "Action logic here"
         shell: bash
   ```

3. **Add README.md** for the action with usage examples

4. **Test action locally** if possible before committing

## Validation

### Basic Repository Validation
- Always run `git --no-pager status` to check working directory state
- Always run `ls -la` to verify current directory contents
- Always check `git --no-pager log --oneline -5` to understand recent changes

### GitHub Actions Validation
When working with GitHub Actions:
- **NEVER CANCEL**: GitHub Action testing may take 2-10 minutes per workflow run. ALWAYS set timeout to 15+ minutes for action testing.
- Validate action.yml syntax: Use `cat action.yml` to review structure
- Check for required fields: name, description, runs
- Verify shell scripts have proper shebang and permissions
- Test composite actions by reviewing each step

### Manual Testing Requirements
- **CRITICAL**: Always test GitHub Actions in a test repository or branch before merging
- Run through complete user scenarios when creating new actions
- Verify all inputs and outputs work as expected
- Test error conditions and edge cases

## Timing Expectations
- File operations (ls, cat, etc.): <1 second
- Git operations (status, log, diff): <1 second  
- Directory navigation: <1 second
- **GitHub Action workflow runs**: 2-10 minutes per run - NEVER CANCEL, set 15+ minute timeout
- **Action marketplace publishing**: 1-5 minutes - NEVER CANCEL, set 10+ minute timeout

## Common Tasks

### Repository Structure (as of current state)
```
.
├── .git/
├── .github/
│   └── copilot-instructions.md
└── Readme.md
```

### Frequently Used Commands
```bash
# Navigate and explore
cd /home/runner/work/actions/actions
ls -la
git --no-pager status

# Search for actions
find . -name "action.yml" -o -name "action.yaml"

# Create new action directory
mkdir -p new-action-name
cd new-action-name

# Check git state before changes
git --no-pager diff
git --no-pager status
```

### README.md Content
```
repository for common github actions I use for my projects. 
many are deviled via llm.
```

## Best Practices
- Always create actions in separate directories with descriptive names
- Include comprehensive README.md for each action
- Use semantic versioning for action releases
- Test actions thoroughly before publishing
- Follow GitHub Actions naming conventions
- Use composite actions for complex multi-step workflows
- Always validate action.yml syntax before committing
- Include proper error handling in action scripts

## CI/CD Integration
- Future GitHub workflows will be added to `.github/workflows/`
- Action testing workflows should include timeout of 15+ minutes minimum
- Always validate actions work in clean environment before merging
- Use action testing best practices with matrix strategies for multiple environments

## Troubleshooting
- If action.yml validation fails: Check YAML syntax and required fields
- If workflows fail: Check logs in GitHub Actions tab, allow full execution time
- If git operations fail: Verify you're in correct directory and have proper permissions
- For LLM-generated actions: Always manually review and test thoroughly

## Notes
- This is a collection repository, not a single action
- Actions are developed incrementally with LLM assistance
- Each action should be self-contained in its own directory
- Repository serves as a library of reusable GitHub Actions