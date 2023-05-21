import os
import logging

from typing import Dict, List

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions

from ..model.entry import Entry
from ..model.day import Day


class DefaultEntriesStorage(object):
    "Entries storage using local ChromaDB"

    def __init__(self):
        logging.getLogger('chromadb').setLevel(logging.ERROR)

        # Create Chroma collection
        CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma")
        chroma_client = chromadb.Client(
            settings=chromadb.config.Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=CHROMA_PERSIST_DIR,
                anonymized_telemetry=False,
            )
        )

        # ~/.cache/torch/sentence_transformers/sentence-transformers_all-mpnet-base-v2
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-mpnet-base-v2"
        )

        metric = "cosine"
        self.collection = chroma_client.get_or_create_collection(
            name="gthnk",
            metadata={"hnsw:space": metric},
            embedding_function=embedding_function,
        )

    def add(self, entry: Entry):
        day = entry.day
        entry_id = f"{day.day_id}-{entry.timestamp}"
        metadatas = {
            "entry_id": entry_id,
            "day_id": day.day_id,
            "timestamp": entry.timestamp,
        }

        # Check if the entry already exists
        if len(self.collection.get(ids=[entry_id], include=[])["ids"]) > 0:
            logging.getLogger("gthnk").debug(f"Entry {entry_id} already exists")
            return
        else:
            self.collection.add(
                ids=entry_id,
                documents=entry.content,
                metadatas=metadatas,
            )
            logging.getLogger("gthnk").info(f"Calculate embeddings for entry {entry_id}")
            return True

    def query(self, query: str, top_num: int) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        entries = self.collection.query(
            query_texts=[query],
            n_results=min(top_num, count),
            include=["documents"]
        )
        return [doc for doc in entries["documents"][0]]
