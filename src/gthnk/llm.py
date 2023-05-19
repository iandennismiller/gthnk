import os
import logging
from typing import Dict, List

from llama_cpp import Llama
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

from dotenv import load_dotenv
load_dotenv()

from .model.entry import Entry
from .model.day import Day


class LLM(object):
    def __init__(self):
        CTX_MAX = 2048
        LLAMA_THREADS_NUM = int(os.getenv("LLAMA_THREADS_NUM", 8))
        LLAMA_MODEL_PATH = os.path.expanduser(os.getenv("LLAMA_MODEL_PATH"))
        logging.getLogger("gthnk").info(f"LLAMA : {LLAMA_MODEL_PATH}" + "\n")

        self.llm = Llama(
            model_path=LLAMA_MODEL_PATH,
            # n_predict=1024,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            verbose=False,
            # use_mlock=True,
        )

        self.llm_embed = Llama(
            model_path=LLAMA_MODEL_PATH,
            # n_predict=1024,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            embedding=True,
            verbose=False,
            # use_mlock=True,
        )

        self.context_db = DefaultEntriesStorage(llm_embed=self.llm_embed)

        logging.getLogger("gthnk").info(f"Llama models loaded")

    def ask(self, prompt: str, CTX_MAX: int = 2048):
        context = self.context_db.query(query=prompt, top_num=5)
        if context:
            prompt_task = 'Consider the following context:\n'
            for i, c in enumerate(context):
                item = c.replace("\n", " ")
                prompt_task += f'{i+1}. {item}\n'
            prompt_task += f'\nBased on that context, answer the following question: {prompt}'
        else:
            prompt_task = f'Answer the following question: {prompt}'

        logging.getLogger("gthnk").info(prompt_task)

        result = self.llm(
            prompt_task[:CTX_MAX],
            stop=["### Human"],
            echo=True,
            temperature=0.2
        )
        return str(result['choices'][0]['text'].strip())


class DefaultEntriesStorage(object):
    "Entries storage using local ChromaDB"

    def __init__(self, llm_embed):
        logging.getLogger('chromadb').setLevel(logging.ERROR)
        self.llm_embed = llm_embed

        # Create Chroma collection
        CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma")
        chroma_client = chromadb.Client(
            settings=chromadb.config.Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=CHROMA_PERSIST_DIR,
            )
        )

        metric = "cosine"
        embedding_function = LlamaEmbeddingFunction(self.llm_embed)

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
            logging.getLogger("gthnk").info(f"Entry {entry_id} already exists")
        else:
            logging.getLogger("gthnk").info(f"Calculate embeddings for entry {entry_id}")
            embeddings = self.llm_embed.embed(entry.content)
            self.collection.add(
                ids=entry_id,
                embeddings=embeddings,
                documents=entry.content,
                metadatas=metadatas,
            )
            logging.getLogger("gthnk").info(f"Entry {entry_id} added")

    def query(self, query: str, top_num: int) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        entries = self.collection.query(
            query_texts=query,
            n_results=min(top_num, count),
            include=["documents"]
        )
        return [doc for doc in entries["documents"][0]]


class LlamaEmbeddingFunction(EmbeddingFunction):
    "Llama embedding function"

    def __init__(self, llm_embed):
        self.llm_embed = llm_embed
        return

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        # logging.getLogger("gthnk").info(f"Calculate embeddings for texts {texts}")
        for t in texts:
            e = self.llm_embed.embed(t)
            embeddings.append(e)
        return embeddings
