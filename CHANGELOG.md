# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/MehdiZare/langchain-fmp-data/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/MehdiZare/langchain-fmp-data/releases/tag/v0.1.0
