"""FmpData tools."""

from typing import Optional, Type, Any

from langchain_core.callbacks import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.embeddings import Embeddings
from pydantic import BaseModel, Field
from fmp_data import FMPDataClient, create_vector_store, ClientConfig
import os


class FmpDataToolInput(BaseModel):
    """Input schema for FmpData tool.

    This docstring is **not** part of what is sent to the model when performing tool
    calling. The Field default values and descriptions **are** part of what is sent to
    the model when performing tool calling.
    """

    # TODO: Add input args and descriptions.
    query: str = Field(..., description="Query in natural language")


class FMPDataTool(BaseTool):  # type: ignore[override]
    """FmpData tool.

    Setup:
        # TODO: Replace with relevant packages, env vars.
        Install ``langchain-fmp-data`` and set environment variable ``FMPDATA_API_KEY``.

        .. code-block:: bash

            pip install -U langchain-fmp-data
            export FMPDATA_API_KEY="your-api-key"

    Instantiation:
        .. code-block:: python
            from fmp_data import FMPDataClient
            
            tool = FmpDataTool(
                embedding: Embeddings
            )

    Invocation with args:
        .. code-block:: python

            # TODO: invoke args
            tool.invoke({...})

        .. code-block:: python

            # TODO: output of invocation

    Invocation with ToolCall:

        .. code-block:: python

            # TODO: invoke args
            tool.invoke({"args": {...}, "id": "1", "name": tool.name, "type": "tool_call"})

        .. code-block:: python

            # TODO: output of invocation
    """  # noqa: E501

    name: str = "FMP Data"
    description: str = (
        "Use this tool for getting financial data with access to real-time market data "
        "such as stock prices, stock indexes, and financial statements."
    )
    args_schema: Type[BaseModel] = FmpDataToolInput

    client: FMPDataClient = Field(exclude=True)
    vector_store: Any = Field(exclude=True)

    def __init__(
            self,
            embeddings: Embeddings,
            api_key: Optional[str] = None,
            store_name: str = "fmp_endpoints",
            cache_dir: Optional[str] = None,
            **kwargs
    ) -> None:
        """Initialize FMP Data tool.

        Args:
            embeddings: Embeddings model for semantic search
            api_key: FMP API key (will use FMP_API_KEY env var if not provided)
            store_name: Name for the vector store
            cache_dir: Directory for storing vector store cache
            **kwargs: Additional arguments passed to BaseTool
        """
        # Initialize FMP client first
        config = ClientConfig.from_env() if api_key is None else ClientConfig(api_key=api_key)

        # Create kwargs dictionary for super().__init__
        tool_kwargs = {
            "client": FMPDataClient(config=config),
            **kwargs
        }

        # Initialize parent class
        super().__init__(**tool_kwargs)

        # Create vector store for semantic search
        self.vector_store = create_vector_store(
            fmp_api_key=config.api_key,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            store_name=store_name,
            cache_dir=cache_dir,
        )

        if not self.vector_store:
            raise RuntimeError("Failed to initialize vector store")

    def _run(
            self, query: str, *, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        fmp_client = FMPDataClient(api_key=1)
        return query

    # TODO: Implement if tool has native async functionality, otherwise delete.

    # async def _arun(
    #     self,
    #     a: int,
    #     b: int,
    #     *,
    #     run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    # ) -> str:
    #     ...
