"""Test FmpData embeddings."""

from typing import Type

from langchain_fmp_data.embeddings import FmpDataEmbeddings
from langchain_tests.integration_tests import EmbeddingsIntegrationTests


class TestParrotLinkEmbeddingsIntegration(EmbeddingsIntegrationTests):
    @property
    def embeddings_class(self) -> Type[FmpDataEmbeddings]:
        return FmpDataEmbeddings

    @property
    def embedding_model_params(self) -> dict:
        return {"model": "nest-embed-001"}
