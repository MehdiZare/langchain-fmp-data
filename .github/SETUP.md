# GitHub Actions Setup Instructions

## Initial Setup

### 1. Create Required Labels

The PR labeler workflow requires labels to exist before it can apply them. You have two options:

#### Option A: Using GitHub Web Interface
1. Go to your repository's Settings → Issues → Labels
2. Create these labels manually:
   - `major` (color: #e11d21) - Breaking changes
   - `minor` (color: #fbca04) - New features
   - `patch` (color: #0e8a16) - Bug fixes
   - `bug` (color: #d73a4a) - Bug reports
   - `enhancement` (color: #a2eeef) - Feature requests
   - `documentation` (color: #0075ca) - Documentation
   - `maintenance` (color: #ffd700) - Maintenance tasks
   - `testing` (color: #9370db) - Test-related
   - `dependencies` (color: #0366d6) - Dependency updates

#### Option B: Using the Script
```bash
# Install requests if needed
pip install requests

# Create a GitHub personal access token with 'repo' scope
# Go to: https://github.com/settings/tokens/new

# Run the script
python scripts/create_labels.py --token YOUR_GITHUB_TOKEN --repo MehdiZare/langchain-fmp-data
```

### 2. Set Up Repository Secrets

Go to Settings → Secrets and variables → Actions, and add:

1. **PYPI_TOKEN** (Required)
   - Get from: https://pypi.org/manage/account/token/
   - Scope: Can be project-specific or global

2. **TEST_PYPI_TOKEN** (Required)
   - Get from: https://test.pypi.org/manage/account/token/
   - Scope: Can be project-specific or global

3. **CODECOV_TOKEN** (Optional)
   - Get from: https://codecov.io/gh/MehdiZare/langchain-fmp-data/settings
   - For coverage reporting

4. **FMP_TEST_API_KEY** (Optional)
   - Your FMP API key for running integration tests

5. **OPENAI_TEST_API_KEY** (Optional)
   - Your OpenAI API key for running integration tests

### 3. Create Dev Branch

```bash
# If you don't have a dev branch yet
git checkout -b dev
git push origin dev

# Set up branch protection (optional but recommended)
# Go to Settings → Branches → Add rule
# - Branch name pattern: main
# - Require pull request reviews before merging
# - Require status checks to pass before merging
```

## How It Works

### Version Bumping

The system automatically determines version bumps based on PR titles or labels:

| PR Title Keywords | Label Applied | Version Change | Example |
|------------------|---------------|----------------|---------|
| `breaking`, `BREAKING CHANGE` | `major` | 1.0.0 → 2.0.0 | "feat!: breaking API change" |
| `feat`, `feature`, `add` | `minor` | 1.0.0 → 1.1.0 | "feat: add new toolkit" |
| `fix`, `bug` | `patch` | 1.0.0 → 1.0.1 | "fix: resolve import error" |
| `docs`, `chore`, `refactor` | `patch` | 1.0.0 → 1.0.1 | "docs: update README" |

### Publishing Flow

1. **Development**: Push to `dev` → Publishes to TestPyPI with `.devYYYYMMDDHHMMSS` suffix
2. **Production**: Merge PR to `main` → Version bumps → Publishes to PyPI → Creates GitHub release

## Troubleshooting

### Labels Not Being Applied

If the PR labeler isn't working:

1. Check that labels exist in the repository
2. Verify the workflow has permissions: Settings → Actions → General → Workflow permissions → Read and write permissions
3. Check workflow runs for error messages: Actions tab → PR Labeler workflow

### Publishing Fails

If PyPI publishing fails:

1. Verify tokens are set correctly in repository secrets
2. Check that the version doesn't already exist on PyPI
3. Ensure package name is available/owned by you
4. Check workflow logs for specific error messages

### Version Not Bumping

If version isn't bumping on merge:

1. Ensure PR has appropriate labels or title keywords
2. Check that the bump-version job is running
3. Verify Poetry is installed and working in the workflow
4. Check for `[skip ci]` in commit messages

## Manual Operations

### Manually Trigger Publishing

1. Go to Actions tab
2. Select "Release Pipeline" workflow
3. Click "Run workflow"
4. Select branch and options

### Manually Bump Version

```bash
# Local version bump
poetry version patch  # or minor/major
git add pyproject.toml
git commit -m "chore: bump version"
git push
```

### Force Republish

If you need to republish the current version:

```bash
# Build locally
poetry build

# Publish to TestPyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi YOUR_TEST_TOKEN
poetry publish -r testpypi

# Publish to PyPI
poetry config pypi-token.pypi YOUR_PYPI_TOKEN
poetry publish
```
