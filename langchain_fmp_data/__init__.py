from importlib import metadata

from langchain_fmp_data.toolkits import FmpDataToolkit
from langchain_fmp_data.tools import FMPDataTool

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "FmpDataToolkit",
    "FMPDataTool",
    "__version__",
]
