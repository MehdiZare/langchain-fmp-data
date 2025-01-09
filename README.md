# langchain-fmp-data

This package contains the LangChain integration with FmpData

## Installation

```bash
pip install -U langchain-fmp-data
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Chat Models

`ChatFmpData` class exposes chat models from FmpData.

```python
from langchain_fmp_data import ChatFmpData

llm = ChatFmpData()
llm.invoke("Sing a ballad of LangChain.")
```

## Embeddings

`FmpDataEmbeddings` class exposes embeddings from FmpData.

```python
from langchain_fmp_data import FmpDataEmbeddings

embeddings = FmpDataEmbeddings()
embeddings.embed_query("What is the meaning of life?")
```

## LLMs
`FmpDataLLM` class exposes LLMs from FmpData.

```python
from langchain_fmp_data import FmpDataLLM

llm = FmpDataLLM()
llm.invoke("The meaning of life is")
```
