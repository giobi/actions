# GitHub Actions Repository

This repository contains a collection of common GitHub Actions and workflow configurations that I use across my projects.

## Overview

This repository is organized to provide reusable GitHub Actions, workflow templates, and documentation for various frameworks and development scenarios.

## Structure

- **`.github/workflows/`**: Reusable workflows that can be called from other repositories
- **`examples/`**: Example usage files showing how to use the reusable workflows
- **`github/`**: Original GitHub-related workflow templates
- **`laravel/`**: Original Laravel-specific workflow templates

## Reusable Workflows

The repository now provides **reusable workflows** that follow GitHub's official conventions. These can be called from any repository:

- **`reusable-issue-close.yml`**: Automatically close old user issues
- **`reusable-issue-duplicate-check.yml`**: Remove duplicate issues based on title matching  
- **`reusable-laravel-deploy.yml`**: Deploy Laravel applications via SSH git pull

See [`.github/workflows/README.md`](.github/workflows/README.md) for complete documentation and usage examples.

## Getting Started

1. **For reusable workflows**: Check the [`.github/workflows/README.md`](.github/workflows/README.md) for detailed usage instructions
2. **For original templates**: Browse the `github/` and `laravel/` folders for standalone workflow templates
3. **For examples**: Look at the `examples/` directory to see real-world usage patterns

## Contributing

Many of these actions and workflows are developed with assistance from LLM tools to ensure best practices and efficiency.

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
