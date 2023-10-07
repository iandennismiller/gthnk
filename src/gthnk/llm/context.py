import os
import re
import logging

from typing import Dict, List

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions

from ..model.entry import Entry
from ..model.day import Day


class ContextStorage(object):
    "Entries storage using local ChromaDB"

    def __init__(self, chroma_persist_dir):
        logging.getLogger('chromadb').setLevel(logging.ERROR)
        logging.getLogger("gthnk").info("Initializing Vector DB...")

        # Create Chroma collection
        chroma_client = chromadb.PersistentClient(
            path=chroma_persist_dir,
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

    def add(self, entry:Entry):
        day = entry.day
        timestamp = f"{day.datestamp}-{entry.timestamp}"
        metadatas = {
            "timestamp": timestamp,
            "datestamp": day.datestamp,
            "timestamp": entry.timestamp,
        }

        # Check if the entry already exists
        if len(self.collection.get(ids=[timestamp], include=[])["ids"]) > 0:
            logging.getLogger("gthnk").debug(f"Entry {timestamp} already exists")
            return
        else:
            self.collection.add(
                ids=timestamp,
                documents=entry.content,
                metadatas=metadatas,
            )
            logging.getLogger("gthnk").info(f"Calculate embeddings for entry {timestamp}")
            return True

    def query(self, query:str, top_num:int=50) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        entries = self.collection.query(
            query_texts=[query],
            n_results=min(top_num, count),
            include=["documents"]
        )
        return [doc for doc in entries["documents"][0]]

    def as_string(self, context_list, max_item_tokens, max_context_tokens):
        "Format a list of context items into a string suitable for an LLM prompt"

        if context_list:
            items = []

            for i, c in enumerate(context_list):
                item = c
                item = re.sub("\s+", " ", item)
                item = re.sub(r" \.\.\. ", ". ", item)
                item = re.sub(r" \.\.\.", ".", item)
                item = re.sub(r"\.\.\.", ".", item)
                item = re.sub(r"^- \[ \] ", "; ", item)
                item = re.sub(r"^- ", "; ", item)
                item = re.sub(r" - ", "; ", item)
                item = re.sub(r"^Okay.\s", "", item)
                item = re.sub(r"^So\s", "", item)
                item = re.sub(r"\n", " ", item)

                item_token_count = len(item.split(" "))
                if item_token_count > max_item_tokens:
                    item = " ".join(item.split(" ")[:max_item_tokens]) + "..."
                    item_token_count = len(item.split(" "))

                current_token_count = len("\n".join(items).split(" "))
                if current_token_count + item_token_count > max_context_tokens:
                    break
                
                # context_task += f'{i+1}. {item}\n'
                # context_task += f'{item}\n\n'
                items.append(f'- {item}')

            return "\n".join(items)
        else:
            return

