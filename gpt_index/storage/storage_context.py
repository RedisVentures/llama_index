from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from gpt_index.storage.docstore.simple_docstore import SimpleDocumentStore
from gpt_index.storage.docstore.types import BaseDocumentStore
from gpt_index.storage.docstore.types import DEFAULT_PERSIST_FNAME as DOCSTORE_FNAME
from gpt_index.storage.index_store.types import (
    DEFAULT_PERSIST_FNAME as INDEX_STORE_FNAME,
)
from gpt_index.vector_stores.simple import DEFAULT_PERSIST_FNAME as VECTOR_STORE_FNAME

from gpt_index.storage.index_store.simple_index_store import SimpleIndexStore
from gpt_index.storage.index_store.types import BaseIndexStore
from gpt_index.vector_stores.simple import SimpleVectorStore
from gpt_index.vector_stores.types import VectorStore

DEFAULT_PERSIST_DIR = "./storage"


@dataclass
class StorageContext:
    """Storage context.

    The storage context container is a utility container for storing nodes,
    indices, and vectors. It contains the following:
    - docstore: BaseDocumentStore
    - index_store: BaseIndexStore
    - vector_store: VectorStore

    """

    docstore: BaseDocumentStore
    index_store: BaseIndexStore
    vector_store: VectorStore

    @classmethod
    def from_defaults(
        cls,
        docstore: Optional[BaseDocumentStore] = None,
        index_store: Optional[BaseIndexStore] = None,
        vector_store: Optional[VectorStore] = None,
        persist_dir: Optional[str] = None,
    ) -> "StorageContext":
        """Create a StorageContext from defaults.

        Args:
            docstore (Optional[BaseDocumentStore]): document store
            index_store (Optional[BaseIndexStore]): index store
            vector_store (Optional[VectorStore]): vector store

        """
        if persist_dir is None:
            docstore = docstore or SimpleDocumentStore()
            index_store = index_store or SimpleIndexStore()
            vector_store = vector_store or SimpleVectorStore()
        else:
            docstore = docstore or SimpleDocumentStore.from_persist_dir(persist_dir)
            index_store = index_store or SimpleIndexStore.from_persist_dir(persist_dir)
            vector_store = vector_store or SimpleVectorStore.from_persist_dir(
                persist_dir
            )

        return cls(docstore, index_store, vector_store)

    def persist(
        self,
        persist_dir: str = DEFAULT_PERSIST_DIR,
        docstore_fname: str = DOCSTORE_FNAME,
        index_store_fname: str = INDEX_STORE_FNAME,
        vector_store_fname: str = VECTOR_STORE_FNAME,
    ) -> None:
        """Persist the storage context.

        Args:
            persist_dir (str): directory to persist the storage context

        """
        docstore_path = str(Path(persist_dir) / docstore_fname)
        index_store_path = str(Path(persist_dir) / index_store_fname)
        vector_store_path = str(Path(persist_dir) / vector_store_fname)
        self.docstore.persist(persist_path=docstore_path)
        self.index_store.persist(persist_path=index_store_path)
        self.vector_store.persist(persist_path=vector_store_path)
