from typing import Dict, List, Optional, Tuple

from gpt_index.data_structs.node_v2 import IndexNode, Node, NodeWithScore
from gpt_index.indices.composability.graph import ComposableGraph
from gpt_index.indices.query.base import BaseQueryEngine
from gpt_index.indices.query.schema import QueryBundle
from gpt_index.response.schema import RESPONSE_TYPE


class ComposableGraphQueryEngine(BaseQueryEngine):
    """Composable graph query engine.

    This query engine can operate over a ComposableGraph.
    It can take in custom query engines for its sub-indices.

    Args:
        graph (ComposableGraph): A ComposableGraph object.
        custom_query_engines (Optional[Dict[str, BaseQueryEngine]]): A dictionary of
            custom query engines.
        recursive (bool): Whether to recursively query the graph.

    """

    def __init__(
        self,
        graph: ComposableGraph,
        custom_query_engines: Optional[Dict[str, BaseQueryEngine]] = None,
        recursive: bool = True,
    ) -> None:
        """Init params."""
        self._graph = graph
        self._custom_query_engines = custom_query_engines or {}

        # additional configs
        self._recursive = recursive

    async def _aquery(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query_index(query_bundle, index_id=None, level=0)

    def _query(self, query_bundle: QueryBundle) -> RESPONSE_TYPE:
        return self._query_index(query_bundle, index_id=None, level=0)

    def _query_index(
        self,
        query_bundle: QueryBundle,
        index_id: Optional[str] = None,
        level: int = 0,
    ) -> RESPONSE_TYPE:
        """Query a single index."""
        index_id = index_id or self._graph.root_id

        # get query engine
        if index_id in self._custom_query_engines:
            query_engine = self._custom_query_engines[index_id]
        else:
            query_engine = self._graph.get_index(index_id).as_query_engine()
        nodes = query_engine.retrieve(query_bundle)

        if self._recursive:
            # do recursion here
            nodes_for_synthesis = []
            additional_source_nodes = []
            for node_with_score in nodes:
                node_with_score, source_nodes = self._fetch_recursive_nodes(
                    node_with_score, query_bundle, level
                )
                nodes_for_synthesis.append(node_with_score)
                additional_source_nodes.extend(source_nodes)
            response = query_engine.synthesize(
                query_bundle, nodes_for_synthesis, additional_source_nodes
            )
        else:
            response = query_engine.synthesize(query_bundle, nodes)

        return response

    def _fetch_recursive_nodes(
        self,
        node_with_score: NodeWithScore,
        query_bundle: QueryBundle,
        level: int,
    ) -> Tuple[NodeWithScore, List[NodeWithScore]]:
        """Fetch nodes.

        Uses existing node if it's not an index node.
        Otherwise fetch response from corresponding index.

        """
        if isinstance(node_with_score.node, IndexNode):
            index_node = node_with_score.node
            # recursive call
            response = self._query_index(query_bundle, index_node.index_id, level + 1)

            new_node = Node(text=str(response))
            new_node_with_score = NodeWithScore(
                node=new_node, score=node_with_score.score
            )
            return new_node_with_score, response.source_nodes
        else:
            return node_with_score, []
