"""Vector store retriever — loads an existing ChromaDB index and queries it."""

import asyncio
import logging

import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

logger = logging.getLogger(__name__)


class Retriever:
    """Wraps a ChromaDB-backed VectorStoreIndex and exposes async semantic search."""

    def __init__(self, persist_dir: str, collection_name: str, embedding_model: str) -> None:
        """Load an existing ChromaDB collection and build a queryable index.

        Args:
            persist_dir: Path to the ChromaDB persistence directory.
            collection_name: ChromaDB collection to query.
            embedding_model: HuggingFace model name used to embed queries.
        """
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        self._collection = chroma_client.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=self._collection)
        embed_model = HuggingFaceEmbedding(model_name=embedding_model)
        self._index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )
        doc_count = self._collection.count()
        logger.info("Retriever loaded index from '%s' (%d docs)", persist_dir, doc_count)

    def is_ready(self) -> bool:
        """Return True if the collection contains at least one embedded document."""
        try:
            return self._collection.count() > 0
        except Exception:
            return False

    async def retrieve(self, query: str, top_k: int) -> list[NodeWithScore]:
        """Return the top_k most relevant chunks for the given query.

        Runs the synchronous llama_index retriever in a thread pool to avoid
        blocking the async event loop during local embedding inference.

        Args:
            query: The user's question.
            top_k: Maximum number of chunks to return.

        Returns:
            List of NodeWithScore objects ordered by relevance.
        """
        retriever = self._index.as_retriever(similarity_top_k=top_k)
        nodes: list[NodeWithScore] = await asyncio.to_thread(retriever.retrieve, query)
        logger.debug("Retrieved %d chunk(s) for query: %.60s…", len(nodes), query)
        return nodes
