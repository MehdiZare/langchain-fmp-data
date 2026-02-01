# langchain-fmp-data

[![CI](https://github.com/MehdiZare/langchain-fmp-data/actions/workflows/ci.yml/badge.svg)](https://github.com/MehdiZare/langchain-fmp-data/actions/workflows/ci.yml)
[![Release](https://github.com/MehdiZare/langchain-fmp-data/actions/workflows/release.yml/badge.svg)](https://github.com/MehdiZare/langchain-fmp-data/actions/workflows/release.yml)
[![PyPI version](https://badge.fury.io/py/langchain-fmp-data.svg)](https://badge.fury.io/py/langchain-fmp-data)
[![Python Versions](https://img.shields.io/pypi/pyversions/langchain-fmp-data.svg)](https://pypi.org/project/langchain-fmp-data/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A LangChain integration for Financial Modeling Prep (FMP) API, providing easy access to financial data through LangChain tools and agents.

## Features

- **FMPDataToolkit**: Query-based toolkit for retrieving specific financial data tools
- **FMPDataTool**: AI-powered agent for natural language financial data queries
- **Comprehensive Financial Data**: Access to stock prices, financial statements, economic indicators, and more
- **LangGraph Integration**: Built on LangGraph for reliable agent workflows
- **Vector Search**: Intelligent tool selection using embeddings and similarity search

## Installation

```bash
pip install -U langchain-fmp-data
```

## Quick Start

### Prerequisites

You'll need API keys for:
- Financial Modeling Prep (FMP) - [Get your API key](https://financialmodelingprep.com/developer)
- OpenAI - [Get your API key](https://platform.openai.com/api-keys)

Set them as environment variables:

```bash
export FMP_API_KEY="your-fmp-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### Using FMPDataToolkit

The toolkit allows you to retrieve specific financial data tools based on your query:

```python
import os
from langchain_fmp_data import FMPDataToolkit

os.environ["FMP_API_KEY"] = "your-fmp-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Get tools for specific financial data needs
query = "Stock market prices, fundamental and technical data"
fmp_toolkit = FMPDataToolkit(query=query, num_results=10)

tools = fmp_toolkit.get_tools()
for tool in tools:
    print(f"- {tool.name}: {tool.description}")
```

### Using FMPDataTool

The FMPDataTool provides an AI agent that can answer complex financial questions:

```python
import os
from langchain_fmp_data import FMPDataTool

os.environ["FMP_API_KEY"] = "your-fmp-api-key"
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize the tool
tool = FMPDataTool()

# Ask financial questions in natural language
response = tool.invoke({"query": "What is the latest price of Bitcoin?"})
print(response)

# Get structured data
response = tool.invoke({
    "query": "Show me Apple's revenue for the last 4 quarters",
    "response_format": "data_structure"
})
print(response)
```

### Response Formats

The FMPDataTool supports three response formats:

- `natural_language`: Human-readable text response (default)
- `data_structure`: Structured JSON data
- `both`: Both natural language and structured data

```python
from langchain_fmp_data import FMPDataTool, ResponseFormat

tool = FMPDataTool()

# Natural language response
response = tool.invoke({
    "query": "What is Tesla's P/E ratio?",
    "response_format": ResponseFormat.NATURAL_LANGUAGE
})

# Structured data response
response = tool.invoke({
    "query": "Get AAPL stock data",
    "response_format": ResponseFormat.DATA_STRUCTURE
})

# Both formats
response = tool.invoke({
    "query": "Show me Microsoft's financial metrics",
    "response_format": ResponseFormat.BOTH
})
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/MehdiZare/langchain-fmp-data.git
cd langchain-fmp-data
```

2. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:
```bash
uv sync --extra dev --extra test
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/langchain_fmp_data --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit_tests/test_tools.py
```

### Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: Fast Python linter and formatter
- **Mypy**: Static type checking

```bash
# Linting
uv run ruff check src/langchain_fmp_data/

# Formatting
uv run ruff format src/langchain_fmp_data/

# Type checking
uv run mypy src/langchain_fmp_data/
```

## CI/CD

### GitHub Actions Workflows

- **CI**: Runs on all PRs and pushes to main/dev branches
  - Linting with Ruff
  - Type checking with Mypy
  - Tests on Python 3.10, 3.11, 3.12, 3.13, 3.14
  - Cross-platform testing (Ubuntu, macOS, Windows)
  - Code coverage reporting to Codecov

- **Release**: Automated version management and publishing
  - Tag-based versioning from PR labels
  - Publishing to PyPI with trusted publishing
  - GitHub release creation with notes

- **Dev Release**: Development releases to TestPyPI
  - Automatic dev version calculation
  - Published on every push to dev branch

### PR Labels for Versioning

- `release:major`: Bumps major version (1.0.0 → 2.0.0)
- `release:minor`: Bumps minor version (1.0.0 → 1.1.0)
- `release:patch`: Bumps patch version (1.0.0 → 1.0.1)

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and ensure tests pass
4. Commit your changes with a descriptive message
5. Push to your fork and open a Pull Request

### Commit Message Format

Follow conventional commits format:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## Project Structure

```
langchain-fmp-data/
├── langchain_fmp_data/     # Main package code
│   ├── __init__.py         # Package exports
│   ├── agent.py            # LangGraph agent implementation
│   ├── tools.py            # FMPDataTool implementation
│   └── toolkits.py         # FMPDataToolkit implementation
├── tests/                  # Test suite
│   ├── unit_tests/         # Unit tests
│   └── integration_tests/  # Integration tests
├── scripts/                # Utility scripts
├── .github/                # GitHub Actions workflows
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── CLAUDE.md               # AI assistant documentation
```

## Dependencies

- **Python**: 3.10 - 3.14
- **LangChain**: ^1.0.0
- **LangChain Core**: ^1.0.0
- **LangChain OpenAI**: ^1.0.0
- **LangGraph**: ^1.0.0
- **FMP-Data**: ^2.1.5 with LangChain extras

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Issue Tracker](https://github.com/MehdiZare/langchain-fmp-data/issues)
- [Discussions](https://github.com/MehdiZare/langchain-fmp-data/discussions)

## Acknowledgments

- [Financial Modeling Prep](https://financialmodelingprep.com/) for providing comprehensive financial data APIs
- [LangChain](https://www.langchain.com/) for the excellent framework
- [OpenAI](https://openai.com/) for embedding and language models

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.

---

Made with ❤️ by [Mehdi Zare](https://github.com/MehdiZare)
