## SSH Connection Format (USERHOST)

For all SSH-related workflows in this repository, we use a unified `USERHOST` variable format that combines all SSH connection parameters into a single string:

### Format
```
user@host.domain.com:port/path/to/project
```

### Components
- **user** (required): SSH username
- **host.domain.com** (required): SSH hostname or IP address
- **:port** (optional): SSH port number (defaults to 22 if not specified)
- **/path/to/project** (optional): Project path on the server (defaults to /var/www/html if not specified)

### Examples

#### Basic format (user and host only):
```
deployuser@myserver.com
```
- User: `deployuser`
- Host: `myserver.com`
- Port: `22` (default)
- Path: `/var/www/html` (default)

#### With custom port:
```
deployuser@myserver.com:2222
```
- User: `deployuser`
- Host: `myserver.com`
- Port: `2222`
- Path: `/var/www/html` (default)

#### With custom path:
```
deployuser@myserver.com/var/www/myapp
```
- User: `deployuser`
- Host: `myserver.com`
- Port: `22` (default)
- Path: `/var/www/myapp`

#### Full format with port and path:
```
deployuser@myserver.com:2222/var/www/myapp
```
- User: `deployuser`
- Host: `myserver.com`
- Port: `2222`
- Path: `/var/www/myapp`

#### Using IP address:
```
deploy@192.168.1.100:22/home/user/project
```
- User: `deploy`
- Host: `192.168.1.100`
- Port: `22`
- Path: `/home/user/project`

### Usage in Workflows

When using SSH-related workflows, provide the USERHOST as a secret:

```yaml
secrets:
  SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
  USERHOST: ${{ secrets.USERHOST }}
```

## Reusable Workflows

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

### 3. Laravel Git Pull (`laravel-git-pull.yml`)

Deploys Laravel applications by pulling code from Git and running optimization commands via SSH.

**Usage:**
```yaml
name: Deploy Laravel via Git Pull
on:
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        type: environment

jobs:
  deploy:
    uses: giobi/actions/.github/workflows/laravel-git-pull.yml@main
    with:
      branch: "main"
      run_post_commands: true
      environment: ${{ github.event.inputs.environment }}
    secrets:
      SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
      USERHOST: ${{ secrets.USERHOST }}
```

**Inputs:**
- `branch` (optional): Branch to pull (default: "main")
- `run_post_commands` (optional): Run post-pull commands (default: true)
- `environment` (required): Target environment for deployment

**Secrets:**
- `SSH_PRIVATE_KEY` (required): SSH private key for server access
- `USERHOST` (required): SSH connection string in format: user@host.domain.com:port/path/to/project (port and path optional)

**Outputs:**
- `deployment_status`: Status of the deployment (success/failure)
- `branch_deployed`: Branch that was deployed
- `post_commands_run`: Whether post-deployment commands were executed

### 4. Laravel Git Pull Deployment (`laravel-deploy.yml`)

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


### 5. Telegram Notification (`telegram-notification.yml`)

Sends notifications to Telegram using the Bot API. Requires TELEGRAM_SECRET and TELEGRAM_CHAT secrets.

**Usage:**
```yaml
name: Send Telegram Notification
on:
  push:
    branches: [main]

jobs:
  notify:
    uses: giobi/actions/.github/workflows/telegram-notification.yml@main
    with:
      message: |
        🚀 New push to ${{ github.repository }}
        
        Branch: ${{ github.ref_name }}
        Author: ${{ github.actor }}
        Commit: ${{ github.event.head_commit.message }}
      parse_mode: "HTML"
      disable_web_page_preview: false
    secrets:
      TELEGRAM_SECRET: ${{ secrets.TELEGRAM_SECRET }}
      TELEGRAM_CHAT: ${{ secrets.TELEGRAM_CHAT }}
```

**Inputs:**
- `message` (required): Message to send to Telegram
- `parse_mode` (optional): Message parse mode - "HTML", "Markdown", or "MarkdownV2" (default: "HTML")
- `disable_web_page_preview` (optional): Disable web page preview for links (default: false)
- `disable_notification` (optional): Send message silently without sound (default: false)

**Secrets:**
- `TELEGRAM_SECRET` (required): Telegram bot token (get from @BotFather)
- `TELEGRAM_CHAT` (required): Telegram chat ID where to send the message

**Outputs:**
- `success`: Whether the notification was sent successfully
- `message_id`: ID of the sent message (if successful)
- `response`: Full API response from Telegram


### 6. ntfy.sh Notifications (`notification-ntfy.yml`)

Send notifications to ntfy.sh topics for real-time alerts and updates.

**Usage:**
```yaml
name: Send ntfy Notification
on:
  workflow_dispatch:
    inputs:
      message:
        description: "Notification message"
        required: true
        type: string

jobs:
  notify:
    uses: giobi/actions/.github/workflows/notification-ntfy.yml@main
    with:
      ntfy_topic: "my-project-alerts"
      message: ${{ github.event.inputs.message }}
      title: "🚀 GitHub Actions"
      priority: "4"
      tags: "rocket,github"
      click_url: "https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

**Inputs:**
- `ntfy_topic` (required): ntfy.sh topic name to send notification to
- `message` (required): Notification message body
- `title` (optional): Notification title
- `priority` (optional): Message priority (1=min, 2=low, 3=default, 4=high, 5=max)
- `tags` (optional): Comma-separated list of tags/emojis
- `actions` (optional): JSON string of actions (buttons/links)
- `click_url` (optional): URL to open when notification is clicked
- `attach_url` (optional): URL of attachment to include
- `delay` (optional): Delay delivery (e.g., '30m', '2h', '1d')
- `email` (optional): Email address for email forwarding

**Outputs:**
- `notification_status`: Status of the notification (success/failure)
- `ntfy_response`: Response from ntfy.sh API
- `topic_used`: Topic that was used for the notification


### 7. PR Branch Cleanup (`pr-branch-cleanup.yml`)

Automatically deletes branches from old pull requests to keep the repository clean.

**Usage:**
```yaml
name: Cleanup Old PR Branches
on:
  # Run manually
  workflow_dispatch:
    inputs:
      days:
        description: "Days threshold for branch deletion"
        required: false
        default: "3"
        type: string
      dry_run:
        description: "Run in dry-run mode"
        required: false
        default: true
        type: boolean

  # Run automatically weekly
  schedule:
    - cron: '0 2 * * 0'  # Sunday at 2 AM UTC

jobs:
  cleanup-branches:
    uses: giobi/actions/.github/workflows/pr-branch-cleanup.yml@main
    with:
      days: ${{ github.event.inputs.days || 3 }}
      dry_run: ${{ github.event.inputs.dry_run == 'true' || false }}
      exclude_branches: "main,master,develop,dev,staging,production,prod"
      include_open_prs: false
```

**Inputs:**
- `days` (optional): Number of days to look back for old PR branches (default: 3)
- `dry_run` (optional): Run in dry-run mode without actually deleting branches (default: false)
- `exclude_branches` (optional): Comma-separated list of branch patterns to exclude (default: "main,master,develop,dev,staging,production,prod")
- `include_open_prs` (optional): Also delete branches from open PRs older than specified days (default: false)

**Outputs:**
- `total_prs_checked`: Total number of PRs checked for branch cleanup
- `branches_deleted`: Number of branches deleted
- `branches_skipped`: Number of branches skipped (protected or not found)
- `error_count`: Number of errors encountered

### 8. Generate SSH Key Pair (`generate-ssh-keypair.yml`)

Generates an SSH key pair and automatically stores the private key in repository secrets and the public key in repository variables.

**Usage:**
```yaml
name: Generate SSH Keys for Deployment
on:
  workflow_dispatch:
    inputs:
      key_type:
        description: "SSH key type"
        required: false
        default: "rsa"
        type: choice
        options:
          - rsa
          - ed25519
          - ecdsa

jobs:
  generate-keys:
    uses: giobi/actions/.github/workflows/generate-ssh-keypair.yml@main
    with:
      private_key_secret_name: "SSH_PRIVATE"
      public_key_var_name: "SSH_PUBLIC"
      key_type: ${{ github.event.inputs.key_type }}
      key_comment: "Generated for automated deployments"
```

**Inputs:**
- `private_key_secret_name` (optional): Name for the private key secret (default: "SSH_PRIVATE")
- `public_key_var_name` (optional): Name for the public key variable (default: "SSH_PUBLIC")
- `key_type` (optional): SSH key type - rsa, ed25519, or ecdsa (default: "rsa")
- `key_bits` (optional): Key bits for RSA keys (default: 4096)
- `key_comment` (optional): Comment for the SSH key (default: "generated by GitHub Actions")

**Outputs:**
- `private_key_name`: Name of the private key secret that was created
- `public_key_name`: Name of the public key variable that was created
- `key_fingerprint`: SSH key fingerprint for identification
- `success`: Whether the key generation and storage was successful

### 9. Documentation Enforcement (`documentation-enforcement.yml`)

**Inputs:**
- `days` (optional): Number of days to look back for closed issues (default: 14)
- `target_docs` (optional): Comma-separated list of documentation files to target (default: "readme.md,agents.md,docs/,help/")
- `dry_run` (optional): Run in dry-run mode without creating issues (default: false)

**Secrets:**
- `OPENROUTER_API_KEY` (optional): OpenRouter API key for AI analysis (if not provided, uses manual analysis)

**Outputs:**
- `issues_analyzed`: Number of issues analyzed
- `features_found`: Number of feature implementations found
- `documentation_issue_created`: Whether a documentation update issue was created
- `documentation_issue_number`: Number of the created documentation issue
=======
- `days` (optional): Number of days to look back for closed issues and PRs (default: "7")
- `language` (optional): Language for the summary - "italian" or "english" (default: "italian")
- `label` (optional): Label to apply to the created summary issue (default: "TOPIC")

**Secrets:**
- `OPENROUTER_API_KEY` (required): OpenRouter API key for AI summary generation

**Outputs:**
- `issue_number`: Number of the created summary issue
- `issue_url`: URL of the created summary issue
- `issues_count`: Number of closed issues found
- `pull_requests_count`: Number of closed pull requests found

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