# langchain-fmp-data

This package contains the LangChain integration with FMPData

## Installation

```bash
pip install -U langchain-fmp-data
```

## ToolBox

You can pass a natural language query indicating what type of tools you want to have. ToolKit return list of num_results tools that best match your query.

OpenAI is used for getting embedding so we can run similarity search on tools.

```python
import os
from langchain_fmp_data import FMPDataToolkit

os.environ["FMP_API_KEY"] = "your-fmp-api-key" # pragma: allowlist secret
os.environ["OPENAI_API_KEY"] = "your-openai-api-key" # pragma: allowlist secret

query = "Stock market prices, fundamental and technical data"

fmp_toolkit = FMPDataToolkit(query=query, num_results=10)

tools = fmp_toolkit.get_tools()
```

## Tool

Tool gives you a lang-graph based agent that can answer your questions. Under the hood, the agent retrieve tools relevant to your query and call Open AI to answer your question.

```python
import os
from langchain_fmp_data import FMPDataTool

os.environ["FMP_API_KEY"] = "your-fmp-api-key" # pragma: allowlist secret
os.environ["OPENAI_API_KEY"] = "your-openai-api-key" # pragma: allowlist secret

query = "What is the latest price of Bitcoin?"

tool = FMPDataTool()

response = tool.invoke({"query": query})
print(response)
```
