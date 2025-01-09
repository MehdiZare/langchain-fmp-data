from typing import AsyncGenerator, Generator

import pytest
from langchain_fmp_data.vectorstores import FmpDataVectorStore
from langchain_core.vectorstores import VectorStore
from langchain_tests.integration_tests import (
    AsyncReadWriteTestSuite,
    ReadWriteTestSuite,
)


class TestFmpDataVectorStoreSync(ReadWriteTestSuite):
    @pytest.fixture()
    def vectorstore(self) -> Generator[VectorStore, None, None]:  # type: ignore
        """Get an empty vectorstore for unit tests."""
        store = FmpDataVectorStore()
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass


class TestFmpDataVectorStoreAsync(AsyncReadWriteTestSuite):
    @pytest.fixture()
    async def vectorstore(self) -> AsyncGenerator[VectorStore, None]:  # type: ignore
        """Get an empty vectorstore for unit tests."""
        store = FmpDataVectorStore()
        # note: store should be EMPTY at this point
        # if you need to delete data, you may do so here
        try:
            yield store
        finally:
            # cleanup operations, or deleting data
            pass
