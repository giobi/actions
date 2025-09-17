# Generic Git Pull Workflow

## Overview

The `git-pull.yml` workflow provides a generic, reusable solution for deploying any type of project via SSH git pull. Unlike framework-specific workflows, this one is designed to work with any project by allowing custom post-pull commands.

## Key Features

- **Generic**: Works with any project type (Node.js, Python, Go, PHP, etc.)
- **Flexible post-commands**: Define custom commands to run after git pull
- **USERHOST format**: Uses the standardized SSH connection format
- **Error handling**: Proper error handling and status reporting
- **Environment support**: Works with GitHub environments

## Quick Start

### Basic Usage (Git Pull Only)
```yaml
jobs:
  deploy:
    uses: giobi/actions/.github/workflows/git-pull.yml@main
    with:
      branch: "main"
      environment: "production"
    secrets:
      SSHPRIVATE: ${{ secrets.SSH_PRIVATE_KEY }}
      USERHOST: ${{ secrets.USERHOST }}
```

### With Custom Commands
```yaml
jobs:
  deploy-with-build:
    uses: giobi/actions/.github/workflows/git-pull.yml@main
    with:
      branch: "main"
      run_post_commands: true
      post_commands: |
        npm install --production
        npm run build
        pm2 restart myapp
      environment: "production"
    secrets:
      SSHPRIVATE: ${{ secrets.SSH_PRIVATE_KEY }}  
      USERHOST: ${{ secrets.USERHOST }}
```

## Required Secrets

### SSHPRIVATE
Your SSH private key for connecting to the server. Generate with:
```bash
ssh-keygen -t rsa -b 4096 -C "github-actions@yourproject.com"
```

### USERHOST
SSH connection string in the format: `user@host.domain.com:port/path/to/project`

Examples:
- Basic: `deployuser@myserver.com`
- With port: `deployuser@myserver.com:2222`
- With path: `deployuser@myserver.com/var/www/myproject`
- Full: `deployuser@myserver.com:2222/var/www/myproject`

### SSHPUBLIC (Optional)
SSH public key, mainly for documentation/verification purposes.

## Common Use Cases

### Node.js/React Application
```yaml
post_commands: |
  npm ci --production
  npm run build
  pm2 restart myapp
```

### Python/Django Application
```yaml
post_commands: |
  source venv/bin/activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py collectstatic --noinput
  sudo systemctl restart gunicorn
```

### Go Application
```yaml
post_commands: |
  go mod tidy
  go build -o app
  sudo systemctl restart myapp
```

### Static Website
```yaml
post_commands: |
  npm run build
  rsync -av dist/ /var/www/html/
```

## Outputs

The workflow provides these outputs that you can use in subsequent jobs:

- `deployment_status`: "success" or "failure"
- `branch_deployed`: The branch that was deployed
- `post_commands_run`: "true" if post commands were executed

### Using Outputs
```yaml
jobs:
  deploy:
    uses: giobi/actions/.github/workflows/git-pull.yml@main
    with:
      # ... inputs

  notify:
    needs: deploy
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Send notification
        run: |
          echo "Deployment status: ${{ needs.deploy.outputs.deployment_status }}"
          echo "Branch deployed: ${{ needs.deploy.outputs.branch_deployed }}"
```

## Comparison with Laravel Workflow

| Feature | Generic Git Pull | Laravel Git Pull |
|---------|------------------|------------------|
| Target | Any project type | Laravel projects |
| Post commands | Fully customizable | Laravel-specific (artisan, composer) |
| Secret naming | SSHPRIVATE, USERHOST, SSHPUBLIC | SSH_PRIVATE_KEY, USERHOST |
| Flexibility | High | Medium (Laravel-focused) |

## Security Best Practices

1. **Use environment protection rules** for production deployments
2. **Limit SSH key permissions** on the target server
3. **Use specific version tags** instead of `@main` in production
4. **Review post-commands** carefully to avoid security issues
5. **Rotate SSH keys** regularly

## Troubleshooting

### Common Issues

1. **SSH Connection Failed**
   - Verify USERHOST format
   - Check SSH key permissions
   - Ensure public key is in server's authorized_keys

2. **Git Commands Failed**
   - Ensure project directory exists and is a git repository
   - Check if the specified branch exists
   - Verify git permissions on the server

3. **Post Commands Failed**
   - Check command syntax
   - Verify required tools are installed on server
   - Check file permissions

4. **USERHOST Parsing Errors**
   - **Empty USERHOST**: Ensure the secret is set in repository settings
   - **Invalid format**: Must contain `@` symbol (user@host format)
   - **Missing components**: Check that user and host are properly specified
   
   **Valid USERHOST formats:**
   ```
   deployuser@myserver.com                              # Basic
   deployuser@myserver.com:2222                         # With port
   deployuser@myserver.com/var/www/myproject           # With path
   deployuser@myserver.com:2222/var/www/myproject      # Full format
   master_user@209.38.212.16/complex/path/structure/   # Complex paths
   ```

### Debug Mode
Enable debug output by adding to post_commands:
```bash
set -x  # Enable debug output
```

### Verifying USERHOST Secret

If you see parsing errors with empty components, check:

1. **Repository Secrets**: Go to Settings > Secrets and variables > Actions
2. **Secret Name**: Must be exactly `USERHOST` (case-sensitive)
3. **Secret Value**: Should not be empty and must follow the format `user@host:port/path`

Example workflow to test USERHOST parsing:
```yaml
jobs:
  test-userhost:
    runs-on: ubuntu-latest
    steps:
      - name: Test USERHOST parsing
        run: |
          USERHOST="${{ secrets.USERHOST }}"
          if [ -z "$USERHOST" ]; then
            echo "❌ USERHOST secret is empty!"
            exit 1
          fi
          echo "✅ USERHOST secret is set: $USERHOST"
```

## Integration Examples

See `example-git-pull.yml` for comprehensive examples including:
- Basic deployment without post-commands
- Node.js application deployment
- Python/Django application deployment
- Go application deployment
- Using different USERHOST formats