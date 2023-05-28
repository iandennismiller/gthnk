import os
import logging

from typing import Dict, List

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions

from ..model.entry import Entry
from ..model.day import Day


class ContextStorage(object):
    "Entries storage using local ChromaDB"

    def __init__(self):
        logging.getLogger('chromadb').setLevel(logging.ERROR)
        logging.getLogger("gthnk").info("Initializing Vector DB...")

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

    def generate_context(self, query, num_query_results, max_item_tokens, max_context_tokens):
        "Based on query, format the results into a context string suitable for an LLM prompt"

        context_list = self.query(query=query, top_num=num_query_results)

        if context_list:
            context_task = ''

            for i, c in enumerate(context_list):
                item = c.replace("\n", " ")
                item_token_count = len(item.split(" "))

                if item_token_count > max_item_tokens:
                    item = " ".join(item.split(" ")[:max_item_tokens]) + "..."

                context_task += f'{i+1}. {item}\n'
                # context_task += f'{item}\n'

                token_count = len(context_task.split(" "))
                if token_count > max_context_tokens:
                    break

            logging.getLogger("gthnk").info(f"Generated {i+1} context items for query: {query}")
            return context_task
        else:
            return
