# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Python 3.13 and 3.14 support
- Dev release workflow for automatic TestPyPI publishing on dev branch pushes
- Codecov configuration with flags for unit tests and integration tests
- JUnit XML test output for CI reporting
- Concurrency control in CI workflows to cancel redundant runs
- CI status aggregation job (`ci-expected`) for reliable status checks

### Changed
- **Breaking**: Migrated from Poetry to uv for dependency management
- **Breaking**: Upgraded to LangChain v1.x ecosystem:
  - `langchain-core` ^0.3.15 → ^1.0.0
  - `langchain` ^0.3.14 → ^1.0.0
  - `langchain-openai` ^0.3.0 → ^1.0.0
  - `langgraph` ^0.2.62 → ^1.0.0
  - `langchain-tests` ^0.3.5 → ^1.0.0
- **Breaking**: Upgraded fmp-data from ^1.0.0 to ^2.1.5
- Switched build backend from `poetry-core` to `hatchling`
- Updated GitHub Actions to latest versions:
  - `actions/checkout` v4 → v6
  - `actions/setup-python` v5 → v6
  - `astral-sh/setup-uv` → v7
  - `pypa/gh-action-pypi-publish` → v1.13.0
- Standardized import path for `create_vector_store` to use `fmp_data.lc`
- Updated docstring examples in toolkits.py to use modern `create_react_agent` pattern
- Changed release workflow to use PR labels (`release:major`, `release:minor`, `release:patch`)
- Release workflow now uses trusted publishing (OIDC) for PyPI
- Default Python version set to 3.12
- Ruff target version updated to py312
- Updated all dev/test dependency versions to latest

### Removed
- Poetry lock file (replaced by uv.lock)
- `langchain-community` dependency (not directly used)
- Legacy release workflow with `poetry version` commands

### Fixed
- Import sorting in tools.py after standardizing fmp_data imports

## [0.1.1] - 2024-01-20

### Added
- Comprehensive pre-commit hooks configuration with Ruff as primary linter/formatter
- Automatic version bumping based on PR labels (major, minor, patch)
- Cross-platform CI/CD support (Ubuntu, macOS, Windows)
- Extensive unit tests for agent, tools, and toolkit modules
- Test coverage reporting with pytest-cov (82% coverage achieved)
- CLAUDE.md documentation for AI assistants
- ResponseFormat enum for flexible output formats in FMPDataTool

### Changed
- Updated fmp-data dependency from ^0.3.1 to ^1.0.0 (major version upgrade)
- Migrated from separate lint.yml and test.yml to unified ci.yml workflow
- Switched to snok/install-poetry@v1 for better cross-platform Poetry installation
- Improved error handling and logging throughout the codebase
- Enhanced README with comprehensive documentation and badges

### Fixed
- Windows CI pipeline failures with Poetry installation
- PR labeler permission errors in GitHub Actions
- Code formatting inconsistencies with Ruff
- Import sorting issues in test files

### Removed
- Unused methods: validate_api_keys() and initialize_vector_store() from tools.py
- Duplicate py.typed file from root directory
- Deprecated scripts/lint_imports.sh
- Legacy GitHub Actions workflows (ci-cd.yml, lint.yml, test.yml)

## [0.1.0] - 2024-01-15

### Added
- Initial release of langchain-fmp-data
- FMPDataToolkit for query-based financial tool retrieval
- FMPDataTool for natural language financial data queries
- Integration with Financial Modeling Prep (FMP) API
- LangGraph-based agent implementation
- Vector store for intelligent tool selection
- Basic documentation and examples

[Unreleased]: https://github.com/MehdiZare/langchain-fmp-data/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/MehdiZare/langchain-fmp-data/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/MehdiZare/langchain-fmp-data/releases/tag/v0.1.0
