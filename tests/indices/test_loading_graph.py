from pathlib import Path
from typing import List
from gpt_index.indices.composability.graph import ComposableGraph
from gpt_index.indices.list.base import GPTListIndex
from gpt_index.indices.loading import load_graph_from_storage
from gpt_index.indices.service_context import ServiceContext
from gpt_index.indices.vector_store.base import GPTVectorStoreIndex

from gpt_index.readers.schema.base import Document
from gpt_index.storage.storage_context import StorageContext


def test_load_graph_from_storage_simple(
    documents: List[Document],
    tmp_path: Path,
    mock_service_context: ServiceContext,
) -> None:
    # construct simple (i.e. in memory) storage context
    storage_context = StorageContext.from_defaults()

    # construct index
    vector_index = GPTVectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    # construct index
    list_index = GPTListIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    # construct graph
    graph = ComposableGraph.from_indices(
        GPTListIndex,
        children_indices=[vector_index, list_index],
        index_summaries=["vector index", "list index"],
        storage_context=storage_context,
        service_context=mock_service_context,
    )

    query_engine = graph.as_query_engine()
    response = query_engine.query("test query")

    # persist storage to disk
    storage_context.persist(str(tmp_path))

    # load storage context
    new_storage_context = StorageContext.from_defaults(persist_dir=str(tmp_path))

    # load index
    new_graph = load_graph_from_storage(
        new_storage_context, root_id=graph.root_id, service_context=mock_service_context
    )

    new_query_engine = new_graph.as_query_engine()
    new_response = new_query_engine.query("test query")

    assert str(response) == str(new_response)
