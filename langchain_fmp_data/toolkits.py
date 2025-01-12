"""FMPData toolkit for accessing financial market data."""

import os
from typing import Any, List, Optional

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import PrivateAttr


class FMPDataToolkit(BaseToolkit):
    """FMPData toolkit for accessing financial market data.

    The FMPDataToolkit provides tools to interact
    with Financial Modeling Prep (FMP) data,
    allowing retrieval and analysis of
    financial market information using natural language queries.

    Examples:
        Basic usage with environment variables:
        ```python
        from langchain_fmp_data import FMPDataToolkit

        # API keys set via environment variables
        toolkit = FMPDataToolkit(
            query="Show me Apple's revenue growth and profit margins",
            num_results=3
        )
        tools = toolkit.get_tools()
        ```

        Usage with explicit API keys:
        ```python
        toolkit = FMPDataToolkit(
            query="Compare Tesla and Ford's debt ratios",
            num_results=5,
            fmp_api_key="your-fmp-key", # pragma: allowlist secret
            openai_api_key="your-openai-key" # pragma: allowlist secret
        )
        ```

        Integration with LangChain agent:
        ```python
        from langchain_openai import ChatOpenAI
        from langchain.agents import create_openai_functions_agent
        from langchain.agents import AgentExecutor

        # Initialize the LLM
        llm = ChatOpenAI(temperature=0)

        # Create toolkit and get tools
        toolkit = FMPDataToolkit(
            query="Analyze Microsoft's financial health",
            num_results=3
        )
        tools = toolkit.get_tools()

        # Create and run agent
        agent = create_openai_functions_agent(llm, tools)
        agent_executor = AgentExecutor(agent=agent, tools=tools)

        response = agent_executor.invoke({
            "input": "What are Microsoft's key financial metrics?"
        })
        print(response["output"])
        ```

        Example with async usage:
        ```python
        async def analyze_financials():
            toolkit = FMPDataToolkit(
                query="Show me Netflix's cash flow analysis",
                num_results=3
            )
            agent_executor = await create_agent(toolkit.get_tools())
            result = await agent_executor.ainvoke({
                "input": "What is Netflix's free cash flow trend?"
            })
            return result["output"]
        ```

    Requirements:
        - FMP Data API key (get from https://financialmodelingprep.com/developer)
        - OpenAI API key
        - Python packages: langchain-fmp-data, langchain, fmp-data

    Environment Variables:
        - FMPDATA_API_KEY: Your FMP Data API key
        - OPENAI_API_KEY: Your OpenAI API key

    Notes:
        - The toolkit uses vector similarity search to find relevant financial data
        - Number of results can be adjusted via num_results parameter
        - API keys can be provided either
            as environment variables or constructor arguments
        - The query parameter accepts natural language input to find relevant tools
    """

    _vector_store: Any = PrivateAttr()
    _tools: List[BaseTool] = PrivateAttr()
    fmp_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    query: Optional[str]
    num_results: int = 3

    def __init__(self, query: str, **data) -> None:
        try:
            from fmp_data.lc import create_vector_store
        except ImportError:
            raise ImportError(
                "Could not import fmp_data python package. "
                "Please install it with `pip install 'fmp_data[langchain]'`."
            )
        all_data = {"query": query, **data}
        super().__init__(**all_data)
        if not self.query:
            raise ValueError("query parameter is required")

        # Get API keys with environment variable fallback
        self._validate_and_set_api_keys()

        # Initialize vector store and tools
        self._vector_store = create_vector_store(
            fmp_api_key=self.fmp_api_key, openai_api_key=self.openai_api_key
        )
        self._tools = self._vector_store.get_tools(query=self.query, k=self.num_results)

    def _validate_and_set_api_keys(self) -> None:
        """Validate and set API keys from arguments or environment variables."""
        self.fmp_api_key = self.fmp_api_key or os.environ.get("FMP_API_KEY")
        self.openai_api_key = self.openai_api_key or os.environ.get("OPENAI_API_KEY")

        missing_keys = []
        if not self.fmp_api_key:
            missing_keys.append("FMP_API_KEY")
        if not self.openai_api_key:
            missing_keys.append("OPENAI_API_KEY")

        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}. "
                "Please either set them as "
                "environment variables or pass them as arguments."
            )

    def get_tools(self) -> List[BaseTool]:
        """Get the list of tools provided by this toolkit.

        Returns:
            List[BaseTool]: A list of tools for interacting with financial data.
        """
        return self._tools
