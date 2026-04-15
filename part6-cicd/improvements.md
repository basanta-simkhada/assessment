# Task 6: CI/CD Pipeline Analysis

## Problem in the current pipeline

  **No Build Artifact Management**
    a. Code is deployed directly from the repository.
    b. No immutable artifact (e.g., Docker image, versioned package).
    c. Result: non-reproducible deployments and inconsistent environments.

  **Missing Environment Separation**
    a. Only main branch triggers deployment.
    b. No distinction between dev, staging, and production.
    c. Result: untested code goes directly to production.

  **No Approval or Governance**
    a. Deployment is automatic on every push.
    b. No manual review or approval step.
    c. Result: no change control.

  **No Security Controls**
    No:
      Dependency scanning
      Static code analysis
      Secret detection

  **Unsafe Deployment Method**
    a. Direct rsync to server:
        No atomic deployment
        No health checks
        No rollback
    b. Result: high downtime risk and fragile releases.

  **No Observability Integration**
    a. No post-deployment validation or monitoring hooks.
    b. Result: failures may go undetected.

  **No Rollback Strategy**
    a. If deployment fails, there is no fallback.
    b. Result: manual recovery required under pressure.

## Recommendations

1. Security Scanning
    a. Dependency Scanning
    b. Static Application Security Testing

2. Testing Strategy
    a. Unit Tests
    b. Integration Tests

3. Artifact Creation
4. Rollback Mechanism
    a. Keep previous Docker images
    b. Rollback by redeploying last stable version

5. Environments (Dev → Staging → Prod)

## Improvement Pipeline Example

name: CI/CD Pipeline

on:
  push:
    branches: [develop, main]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Run Tests
        run: pytest --cov=app --cov-fail-under=80

      - name: Security Scan
        run: |
          pip install pip-audit bandit
          pip-audit
          bandit -r .

      - name: Build Docker Image
        run: docker build -t app:${{ github.sha }} .

  deploy-dev:
    if: github.ref == 'refs/heads/develop'
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Dev
        run: echo "Deploying to Dev"

  deploy-prod:
    if: github.ref == 'refs/heads/main'
    needs: build-test
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: echo "Deploying to Production"
