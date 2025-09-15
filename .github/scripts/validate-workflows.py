#!/usr/bin/env python3
"""
GitHub Actions Workflow Validator

Validates GitHub Actions workflow files for common issues:
- YAML syntax errors
- Invalid permission scopes
- Required fields
"""

import os
import yaml
import sys
from pathlib import Path

# Valid GitHub Actions permission scopes
VALID_PERMISSIONS = {
    'actions', 'checks', 'contents', 'deployments', 'id-token',
    'issues', 'discussions', 'packages', 'pages', 'pull-requests',
    'repository-projects', 'security-events', 'statuses'
}

def validate_workflow_file(file_path):
    """Validate a single workflow file."""
    errors = []
    
    try:
        with open(file_path, 'r') as f:
            workflow = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"YAML syntax error: {e}")
        return errors
    except Exception as e:
        errors.append(f"File read error: {e}")
        return errors
    
    # Check for jobs section
    if not workflow.get('jobs'):
        errors.append("No 'jobs' section found")
        return errors
    
    # Validate permissions in each job
    for job_name, job_config in workflow['jobs'].items():
        permissions = job_config.get('permissions', {})
        if permissions and isinstance(permissions, dict):
            for perm in permissions.keys():
                if perm not in VALID_PERMISSIONS:
                    errors.append(
                        f"Job '{job_name}': Invalid permission '{perm}'. "
                        f"Valid permissions: {', '.join(sorted(VALID_PERMISSIONS))}"
                    )
    
    return errors

def main():
    """Main validation function."""
    workflows_dir = Path('.github/workflows')
    
    if not workflows_dir.exists():
        print("No .github/workflows directory found")
        return 1
    
    total_errors = 0
    
    for workflow_file in workflows_dir.glob('*.yml'):
        print(f"Validating {workflow_file}...")
        errors = validate_workflow_file(workflow_file)
        
        if errors:
            print(f"  ❌ {len(errors)} error(s):")
            for error in errors:
                print(f"    - {error}")
            total_errors += len(errors)
        else:
            print(f"  ✅ Valid")
    
    if total_errors > 0:
        print(f"\nTotal errors found: {total_errors}")
        return 1
    else:
        print(f"\n✅ All workflow files are valid!")
        return 0

if __name__ == '__main__':
    sys.exit(main())