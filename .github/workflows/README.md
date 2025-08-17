# GitHub Actions Workflows

This repository uses GitHub Actions for CI/CD with automatic versioning and PyPI publishing.

## Workflows

### 1. CI (`ci.yml`)
- **Triggers**: On every push and PR to `main` and `dev` branches
- **Purpose**: Run tests, linting, and code quality checks
- **Jobs**:
  - Lint: Runs ruff and mypy
  - Test: Runs pytest on multiple Python versions
  - Check imports: Validates import statements

### 2. Release Pipeline (`release.yml`)
- **Triggers**: 
  - PR merge to `main` → Bump version & publish to PyPI
  - Push to `dev` → Publish to TestPyPI
- **Purpose**: Automated versioning and package publishing
- **Jobs**:
  - Test: Run full test suite
  - Bump Version: Automatically bump version based on PR labels
  - Publish to PyPI/TestPyPI: Deploy packages

### 3. PR Labeler (`pr-labeler.yml`)
- **Triggers**: When PRs are opened or edited
- **Purpose**: Automatically label PRs based on title/content
- **Labels Applied**:
  - `major`: Breaking changes (bumps x.0.0)
  - `minor`: New features (bumps 0.x.0)
  - `patch`: Bug fixes (bumps 0.0.x)
  - Type labels: `bug`, `enhancement`, `documentation`, etc.

### 4. Label Sync (`label-sync.yml`)
- **Triggers**: Manual or when labels.yml changes
- **Purpose**: Ensure all required labels exist in the repository

## Versioning Strategy

Version bumps are automatic based on PR labels:

| PR Title Contains | Label Applied | Version Bump |
|------------------|---------------|--------------|
| `breaking`, `BREAKING CHANGE` | `major` | 1.0.0 → 2.0.0 |
| `feat`, `feature`, `add` | `minor` | 1.0.0 → 1.1.0 |
| `fix`, `bug`, `patch` | `patch` | 1.0.0 → 1.0.1 |
| `docs`, `chore`, `refactor` | `patch` | 1.0.0 → 1.0.1 |

## Publishing Strategy

### Production (PyPI)
- **When**: PR merged to `main` with version label
- **Process**: 
  1. Version automatically bumped based on label
  2. Package built and published to PyPI
  3. GitHub Release created

### Testing (TestPyPI)
- **When**: Push to `dev` branch
- **Process**:
  1. Version gets `.devYYYYMMDDHHMMSS` suffix
  2. Package published to TestPyPI for testing

## Required Secrets

Configure these in repository settings:

- `PYPI_TOKEN`: PyPI API token for publishing
- `TEST_PYPI_TOKEN`: TestPyPI API token for test publishing
- `CODECOV_TOKEN`: (Optional) For coverage reporting
- `FMP_TEST_API_KEY`: (Optional) For integration tests
- `OPENAI_TEST_API_KEY`: (Optional) For integration tests

## Usage Examples

### Regular Development
1. Create feature branch from `dev`
2. Make changes and push
3. Open PR to `dev` for testing
4. After testing, open PR from `dev` to `main`

### Hotfix
1. Create branch from `main`
2. Make fix
3. Open PR to `main` with title like "fix: resolve critical bug"
4. PR gets labeled `patch` automatically
5. On merge, version bumps and publishes automatically

### New Feature
1. Create branch from `dev`
2. Develop feature
3. Open PR with title like "feat: add new toolkit"
4. PR gets labeled `minor` automatically
5. On merge to `main`, version bumps and publishes

## Manual Override

To manually trigger workflows:
- Go to Actions tab
- Select workflow
- Click "Run workflow"
- Choose branch and options