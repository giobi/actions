# Reusable Workflows

This directory contains reusable GitHub Actions workflows that can be called from other repositories.

## Available Reusable Workflows

### 1. Auto Close User Issues (`issue-close.yml`)

Automatically closes issues created by a specific user after a configurable number of days.

**Usage:**
```yaml
name: Close Old User Issues
on:
  workflow_dispatch:
    inputs:
      username:
        description: "Username whose issues to close"
        required: true
        type: string

jobs:
  close-issues:
    uses: giobi/actions/.github/workflows/issue-close.yml@main
    with:
      user: ${{ github.event.inputs.username }}
      dry_run: false
      days: 10
```

**Inputs:**
- `user` (required): Username whose issues should be closed
- `dry_run` (optional): Run in dry-run mode without actually closing issues
- `days` (optional): Number of days to look back for old issues (default: 10)

**Outputs:**
- `total_issues`: Total number of user issues found
- `closed_count`: Number of issues closed
- `marked_for_deletion_count`: Number of issues marked for deletion
- `error_count`: Number of errors encountered

### 2. Remove Duplicate Issues (`issue-duplicate-check.yml`)

Checks for and removes duplicate issues based on title matching.

**Usage:**
```yaml
name: Check for Duplicates
on:
  issues:
    types: [opened, edited]

jobs:
  check-duplicates:
    uses: giobi/actions/.github/workflows/issue-duplicate-check.yml@main
    with:
      issue_number: ${{ github.event.issue.number }}
      issue_title: ${{ github.event.issue.title }}
      issue_state: ${{ github.event.issue.state }}
      skip_if_closed: true
```

**Inputs:**
- `issue_number` (required): Issue number to check for duplicates
- `issue_title` (required): Issue title to check for duplicates
- `issue_state` (optional): Current state of the issue (default: "open")
- `skip_if_closed` (optional): Skip processing if issue is closed (default: true)

**Outputs:**
- `duplicates_found`: Number of duplicate issues found
- `duplicates_closed`: Number of duplicate issues that were closed
- `current_issue_closed`: Whether the current issue was closed as a duplicate

### 3. Laravel Git Pull Deployment (`laravel-deploy.yml`)

Deploys Laravel applications by pulling code from Git and running optimization commands.

**Usage:**
```yaml
name: Deploy to Production
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: environment

jobs:
  deploy:
    uses: giobi/actions/.github/workflows/laravel-deploy.yml@main
    with:
      branch: "main"
      run_post_commands: true
      environment: ${{ github.event.inputs.environment }}
    secrets:
      SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
      SSH_HOST: ${{ secrets.SSH_HOST }}
      SSH_USER: ${{ secrets.SSH_USER }}
      SSH_PORT: ${{ secrets.SSH_PORT }}
      PROJECT_PATH: ${{ secrets.PROJECT_PATH }}
```

**Inputs:**
- `branch` (optional): Branch to pull (default: "main")
- `run_post_commands` (optional): Run post-pull commands (default: true)
- `environment` (required): Target environment for deployment

**Secrets:**
- `SSH_PRIVATE_KEY` (required): SSH private key for server access
- `SSH_HOST` (required): SSH host/server address
- `SSH_USER` (required): SSH username
- `SSH_PORT` (optional): SSH port (defaults to 22)
- `PROJECT_PATH` (optional): Path to project directory (defaults to /var/www/html)

**Outputs:**
- `deployment_status`: Status of the deployment (success/failure)
- `branch_deployed`: Branch that was deployed
- `post_commands_run`: Whether post-deployment commands were executed

## General Usage Guidelines

1. **Reference the workflow**: Use the format `owner/repo/.github/workflows/workflow-file.yml@ref`
2. **Specify inputs**: Pass required inputs using the `with:` keyword
3. **Pass secrets**: Use the `secrets:` keyword for sensitive data
4. **Access outputs**: Use the job ID to access outputs from reusable workflows

## Example Repository Structure

```
your-repo/
├── .github/
│   └── workflows/
│       ├── issue-management.yml
│       ├── deploy-prod.yml
│       └── deploy-staging.yml
└── ...
```

## Security Considerations

- Always use specific version tags or commit SHAs instead of `@main` in production
- Review the reusable workflow code before using it
- Limit secrets to only what's necessary for the workflow
- Use environment protection rules for production deployments

## Contributing

To suggest improvements or report issues with these reusable workflows, please open an issue in the repository.