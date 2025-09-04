# Laravel Framework Actions

This folder contains GitHub Actions and workflows specifically designed for Laravel applications.

## Available Actions

### CI/CD Pipeline
- Automated testing with PHPUnit
- Code quality checks with PHP_CodeSniffer and PHPStan
- Dependency installation with Composer
- Laravel-specific optimizations

### Deployment
- Laravel application deployment workflows
- Environment configuration management
- Database migration handling
- Asset compilation and optimization

## Getting Started

1. Copy the relevant workflow files to your `.github/workflows/` directory
2. Customize the configuration variables for your project
3. Ensure your Laravel application has proper test coverage

## Requirements

- PHP 8.0+
- Composer
- Laravel 9.0+

## Examples

See the individual workflow files in this directory for specific implementation examples.

## Best Practices

- Always run tests before deployment
- Use proper environment variable management
- Implement database seeding for testing environments
- Cache dependencies to speed up builds