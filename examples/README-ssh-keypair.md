# SSH Key Pair Generation Workflow

## Overview

The `ssh-generate-keys.yml` workflow provides an automated way to generate SSH key pairs and store them securely in your GitHub repository:

- **Private key** → Stored in repository secrets (encrypted)
- **Public key** → Stored in repository variables (accessible)

## Quick Start

### Basic Usage
```yaml
jobs:
  generate-keys:
    uses: giobi/actions/.github/workflows/ssh-generate-keys.yml@main
```

This creates:
- Secret: `SSH_PRIVATE` (private key)  
- Variable: `SSH_PUBLIC` (public key)

### Custom Names
```yaml
jobs:
  generate-deploy-keys:
    uses: giobi/actions/.github/workflows/ssh-generate-keys.yml@main
    with:
      private_key_secret_name: "DEPLOY_SSH_PRIVATE"
      public_key_var_name: "DEPLOY_SSH_PUBLIC"
```

### Different Key Types
```yaml
jobs:
  generate-ed25519-keys:
    uses: giobi/actions/.github/workflows/ssh-generate-keys.yml@main
    with:
      key_type: "ed25519"
      key_comment: "ED25519 deployment key"
```

## Using Generated Keys

After generation, you can use the keys in other workflows:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ vars.DEPLOY_HOST }}
          username: ${{ vars.DEPLOY_USER }}
          key: ${{ secrets.SSH_PRIVATE }}  # Generated private key
          script: |
            # Your deployment commands here
            echo "Public key fingerprint from generation: ${{ needs.generate-keys.outputs.key_fingerprint }}"
```

## Manual Testing

To test the workflow in this repository:

1. **Go to Actions tab** in GitHub
2. **Select "Test SSH Key Pair Generation"** workflow
3. **Click "Run workflow"**
4. **Monitor the execution** - it should:
   - Generate an RSA 2048-bit key pair
   - Store private key in `TEST_SSH_PRIVATE` secret
   - Store public key in `TEST_SSH_PUBLIC` variable
   - Display the key fingerprint

5. **Verify results** in repository settings:
   - Go to Settings > Secrets and variables > Actions
   - Check that `TEST_SSH_PRIVATE` appears in secrets
   - Check that `TEST_SSH_PUBLIC` appears in variables

## Key Types Supported

- **RSA**: 2048 or 4096 bits (default: 4096)
- **ED25519**: Modern, secure, fast
- **ECDSA**: Elliptic curve (256-bit, 384-bit, 521-bit)

## Security Notes

- Private keys are encrypted using libsodium before storage
- Keys are generated in temporary files and immediately cleaned up
- Only the workflow with proper permissions can access repository secrets
- Public keys in variables are visible to workflows but not in logs

## Outputs Available

- `private_key_name`: Name of created secret
- `public_key_name`: Name of created variable  
- `key_fingerprint`: SSH key fingerprint for identification
- `success`: Whether operation completed successfully

## Common Patterns

See `example-generate-ssh-keypair.yml` for comprehensive examples including:
- Basic usage with defaults
- Custom naming schemes
- Different key types
- Using outputs in subsequent jobs
- Integration with deployment workflows