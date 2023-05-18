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

        print(f"LLAMA : {LLAMA_MODEL_PATH}" + "\n")
        assert os.path.exists(LLAMA_MODEL_PATH), "\033[91m\033[1m" + f"Model can't be found." + "\033[0m\033[0m"

        self.llm = Llama(
            model_path=LLAMA_MODEL_PATH,
            # n_predict=1024,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            # use_mlock=True,
        )

        self.llm_embed = Llama(
            model_path=LLAMA_MODEL_PATH,
            # n_predict=1024,
            n_ctx=CTX_MAX,
            n_threads=LLAMA_THREADS_NUM,
            n_batch=512,
            embedding=True,
            # use_mlock=True,
        )

        self.context_db = DefaultEntriesStorage(llm_embed=self.llm_embed)

        print(f"Llama models loaded")

    def context(self, query):
        context = self.context_db.query(query=query, top_entries_num=5)
        return context

    def ask(self, prompt: str, CTX_MAX: int = 2048):
        prompt_task = f'Answer the following question: {prompt}.\n'
        context = self.context(prompt_task)
        if context:
            prompt_task += 'Take into account the following context: ' + '\n\n'.join(context)

        print(f"Final prompt: {prompt_task}")

        result = self.llm(
            prompt_task[:CTX_MAX],
            stop=["### Human"],
            echo=False,
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

    def add(self, day: Dict, entry: Entry):
        entry_id = f"{day.day_id}-{entry.timestamp}"
        metadatas = {
            "day_id": day.day_id,
            "timestamp": entry.timestamp,
            # "entry_id": entry_id,
            "entry": entry.content
        }

        # Check if the entry already exists
        if len(self.collection.get(ids=[entry_id], include=[])["ids"]) > 0:
            print(f"Entry {entry_id} already exists")
            pass
            # self.collection.update(
            #     ids=entry_id,
            #     embeddings=embeddings,
            #     documents=entry.content,
            #     metadatas=metadatas,
            # )
        else:
            print(f"Calculate embeddings for entry {entry_id}")
            embeddings = self.llm_embed.embed(entry.content)
            self.collection.add(
                ids=entry_id,
                embeddings=embeddings,
                documents=entry.content,
                metadatas=metadatas,
            )
            print(f"Entry {entry_id} added")

    def query(self, query: str, top_entries_num: int) -> List[dict]:
        count: int = self.collection.count()
        if count == 0:
            return []
        entries = self.collection.query(
            query_texts=query,
            n_results=min(top_entries_num, count),
            include=["metadatas"]
        )
        # return [f'{item["day_id"]}-{item["timestamp"]}' for item in entries["metadatas"][0]]
        return [item["entry"] for item in entries["metadatas"][0]]


class LlamaEmbeddingFunction(EmbeddingFunction):
    "Llama embedding function"

    def __init__(self, llm_embed):
        self.llm_embed = llm_embed
        return

    def __call__(self, texts: Documents) -> Embeddings:
        embeddings = []
        for t in texts:
            e = self.llm_embed.embed(t)
            embeddings.append(e)
        return embeddings
