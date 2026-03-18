"""Document ingestion — load, chunk, embed, and persist to ChromaDB."""

import logging
from pathlib import Path

import chromadb
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from core.config import get_settings

logger = logging.getLogger(__name__)


def build_index(
    data_dir: str,
    persist_dir: str,
    collection_name: str,
    embedding_model: str,
    chunk_size: int,
    chunk_overlap: int,
) -> VectorStoreIndex:
    """Load documents from data_dir, chunk, embed, and store in ChromaDB.

    Args:
        data_dir: Directory containing PDF/Markdown source files.
        persist_dir: Path where ChromaDB persists its data on disk.
        collection_name: ChromaDB collection to write into.
        embedding_model: HuggingFace model name used for embedding.
        chunk_size: Maximum token count per chunk.
        chunk_overlap: Token overlap between consecutive chunks.

    Returns:
        A VectorStoreIndex backed by the ChromaDB collection.

    Raises:
        FileNotFoundError: If data_dir is missing or contains no files.
    """
    source = Path(data_dir)
    if not source.exists() or not any(source.iterdir()):
        raise FileNotFoundError(
            f"No documents found in '{data_dir}'. "
            "Run 'uv run python scripts/download_dataset.py' first."
        )

    logger.info("Loading documents from %s", data_dir)
    documents = SimpleDirectoryReader(str(source)).load_data()
    logger.info("Loaded %d document(s)", len(documents))

    parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = parser.get_nodes_from_documents(documents)
    logger.info("Created %d chunk(s)", len(nodes))

    embed_model = HuggingFaceEmbedding(model_name=embedding_model)

    chroma_client = chromadb.PersistentClient(path=persist_dir)
    chroma_collection = chroma_client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    logger.info("Building index — embedding %d chunks (this may take a minute)…", len(nodes))
    index = VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        embed_model=embed_model,
    )
    logger.info("Index built and persisted at '%s'", persist_dir)
    return index


def main() -> None:
    """CLI entry-point: read settings and run document ingestion."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    settings = get_settings()
    build_index(
        data_dir=str(settings.project_root / "data" / "documents"),
        persist_dir=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection_name,
        embedding_model=settings.embedding_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    logger.info("✅ Ingestion complete.")


if __name__ == "__main__":
    main()
