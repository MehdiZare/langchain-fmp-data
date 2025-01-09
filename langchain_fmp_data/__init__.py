from importlib import metadata

from langchain_fmp_data.chat_models import ChatFmpData
from langchain_fmp_data.document_loaders import FmpDataLoader
from langchain_fmp_data.embeddings import FmpDataEmbeddings
from langchain_fmp_data.retrievers import FmpDataRetriever
from langchain_fmp_data.toolkits import FmpDataToolkit
from langchain_fmp_data.tools import FmpDataTool
from langchain_fmp_data.vectorstores import FmpDataVectorStore

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ChatFmpData",
    "FmpDataVectorStore",
    "FmpDataEmbeddings",
    "FmpDataLoader",
    "FmpDataRetriever",
    "FmpDataToolkit",
    "FmpDataTool",
    "__version__",
]
