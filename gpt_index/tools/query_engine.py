from typing import Any, Optional, cast
from gpt_index.indices.query.base import BaseQueryEngine
from gpt_index.tools.types import BaseTool, ToolMetadata


DEFAULT_NAME = "Query Engine Tool"
DEFAULT_DESCRIPTION = """Useful for running a natural language query
against a knowledge base and get back a natural language response.
"""


class QueryEngineTool(BaseTool):
    """Query engine tool.

    A tool making use of a query engine.

    Args:
        query_engine (BaseQueryEngine): A query engine.
        metadata (ToolMetadata): The associated metadata of the query engine.
    """

    def __init__(
        self,
        query_engine: BaseQueryEngine,
        metadata: ToolMetadata,
    ) -> None:
        self._query_engine = query_engine
        self._metadata = metadata

    @classmethod
    def from_defaults(
        cls,
        query_engine: BaseQueryEngine,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> "QueryEngineTool":
        name = name or DEFAULT_NAME
        description = description or DEFAULT_DESCRIPTION
        metadata = ToolMetadata(name=name, description=description)
        return cls(query_engine=query_engine, metadata=metadata)

    @property
    def query_engine(self) -> BaseQueryEngine:
        return self._query_engine

    @property
    def metadata(self) -> ToolMetadata:
        return self._metadata

    def __call__(self, input: Any) -> Any:
        query_str = cast(str, input)
        response = self._query_engine.query(query_str)
        return str(response)
