from abc import ABC, abstractmethod
from typing import List
from gpt_index.data_structs.node_v2 import NodeWithScore

from gpt_index.indices.query.schema import QueryBundle, QueryType


class BaseRetriever(ABC):
    """Base retriever."""

    def retrieve(self, str_or_query_bundle: QueryType) -> List[NodeWithScore]:
        """Retrieve nodes given query.

        Args:
            str_or_query_bundle (QueryType): Either a query string or
                a QueryBundle object.

        """
        if isinstance(str_or_query_bundle, str):
            str_or_query_bundle = QueryBundle(str_or_query_bundle)
        return self._retrieve(str_or_query_bundle)

    @abstractmethod
    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query.

        Implemented by the user.

        """
        pass
