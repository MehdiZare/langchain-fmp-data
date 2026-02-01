# GitHub Actions Workflows

This repository uses GitHub Actions for CI/CD with automatic versioning and PyPI publishing.

## Workflows

### 1. CI (`ci.yml`)
- **Triggers**: On pull requests
- **Purpose**: Run tests, linting, and code quality checks
- **Jobs**:
  - Tests: Runs pytest on Python 3.10, 3.11, 3.12, 3.13, and 3.14
  - Quality Gates: Runs ruff, mypy, and bandit (on Python 3.12)
  - Coverage: Runs tests with coverage and uploads to Codecov

### 2. Release Pipeline (`release.yml`)
- **Triggers**: PR merge to `main` with release labels
- **Purpose**: Automated versioning and package publishing to PyPI
- **Labels**:
  - `release:major` - Bump major version (x.0.0)
  - `release:minor` - Bump minor version (0.x.0)
  - `release:patch` - Bump patch version (0.0.x)
- **Process**:
  1. Calculate new version based on PR label
  2. Update `pyproject.toml` with new version
  3. Commit version bump and create tag
  4. Build wheel and sdist
  5. Create GitHub Release
  6. Publish to PyPI

### 3. Dev Release (`dev-release.yml`)
- **Triggers**: Push to `dev` branch or manual trigger
- **Purpose**: Publish development versions to TestPyPI
- **Process**:
  1. Calculate dev version based on PR labels (if open PR to main exists)
  2. Build wheel and sdist
  3. Publish to TestPyPI

### 4. Guard Main Origin (`guard-main-origin.yml`)
- **Triggers**: PRs targeting `main`
- **Purpose**: Ensure PRs to main only come from allowed branches
- **Allowed branches**: `dev`, `hotfix-*`, `updates-*`, `fea/*`

### 5. PR Labeler (`pr-labeler.yml`)
- **Triggers**: PR opened, edited, or synchronized
- **Purpose**: Automatically add labels based on PR title
- **Labels added**:
  - `release:major` for "breaking" changes
  - `release:minor` for "feat" or "feature"
  - `release:patch` for "fix", "bug", "docs", "chore", "refactor"
  - Type labels: `bug`, `enhancement`, `documentation`, `testing`, `maintenance`

### 6. Label Sync (`label-sync.yml`)
- **Triggers**: Push to main (when `.github/labels.yml` changes) or manual
- **Purpose**: Sync repository labels from `.github/labels.yml`

## Release Workflow

1. Create feature branch from `dev` (e.g., `fea/my-feature`)
2. Make changes and create PR to `dev`
3. PR gets auto-labeled based on title
4. Merge to `dev` → dev version published to TestPyPI
5. Create PR from `dev` to `main`
6. Add appropriate `release:*` label if not auto-added
7. Merge to `main` → version bumped and published to PyPI

## Environments

This repository uses GitHub Environments for secure publishing:

- **pypi**: For production releases to PyPI (uses OIDC trusted publishing)
- **testpypi**: For development releases to TestPyPI (uses OIDC trusted publishing)

## Dependencies

All workflows use:
- `uv` for fast Python dependency management
- `hatchling` for building packages
- OIDC trusted publishing for PyPI (no API tokens needed)
