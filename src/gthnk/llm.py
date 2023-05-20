import os
import sys
import random
import logging
import subprocess

from typing import Dict, List
from contextlib import redirect_stderr, redirect_stdout

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from chromadb.utils import embedding_functions

from dotenv import load_dotenv
load_dotenv()

from .model.entry import Entry
from .model.day import Day


class LLM(object):

    def __init__(self):
        logging.getLogger("gthnk").info("Initializing Vector DB...")
        self.context_db = DefaultEntriesStorage()

    def get_context(self, prompt, model_type):
        logging.getLogger("gthnk").info("Generating context...")

        if model_type in ["llama_ggmlv2", "llama_ggmlv3"]:
            num_query_results = 50
            max_item_tokens = 40
            max_context_tokens = 1024
        elif model_type == "llama":
            num_query_results = 50
            max_item_tokens = 40
            max_context_tokens = 256
        elif model_type == "mpt":
            num_query_results = 50
            max_item_tokens = 32
            max_context_tokens = 128

        context_list = self.context_db.query(query=prompt, top_num=num_query_results)

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

            return context_task
        else:
            return

    def ask_llama(self, prompt: str):
        from llama_cpp import Llama

        LLAMA_THREADS_NUM = int(os.getenv("LLAMA_THREADS_NUM", 8))
        if os.getenv("LLAMA_MODEL_PATH"):
            LLAMA_MODEL_PATH = os.path.expanduser(os.getenv("LLAMA_MODEL_PATH"))
            logging.getLogger("gthnk").info(f"Loading LLAMA: {LLAMA_MODEL_PATH}" + "\n")
        else:
            raise Exception("LLAMA_MODEL_PATH not set")

        # with open('/dev/null', 'w') as f:
        #     with redirect_stderr(f):
        #         with redirect_stdout(f):
        if not hasattr(self, "llm"):
            self.llm = Llama(
                model_path=LLAMA_MODEL_PATH,
                n_ctx=2048,
                n_threads=LLAMA_THREADS_NUM,
                n_batch=512,
                verbose=False,
                # n_predict=1024,
                # use_mlock=True,
            )

        # prompt += "\n### Assistant: "
        result_raw = self.llm(
            prompt,
            stop=["### Human"],
            echo=False,
            temperature=0.2
        )
        result_str = str(result_raw['choices'][0]['text'].strip())

        # for Vicuna
        results = result_str.split("### Assistant: ")
        if len(results) >= 2:
            result = results[1]
        else:
            result = result_str

        return result

    def ask_llama_ggmlv3(self, prompt: str):
        return self.ask_llama_ggml(prompt, model_type="ggmlv3")

    def ask_llama_ggmlv2(self, prompt: str):
        return self.ask_llama_ggml(prompt, model_type="ggmlv2")

    def ask_llama_ggml(self, prompt: str, model_type: str="ggmlv3"):
        if model_type == "ggmlv3":
            binary_path = os.getenv("LLAMA_GGMLV3_BINARY_PATH")
            model_path = os.getenv("LLAMA_GGMLV3_MODEL_PATH")
        elif model_type == "ggmlv2":
            binary_path = os.getenv("LLAMA_GGMLV2_BINARY_PATH")
            model_path = os.getenv("LLAMA_GGMLV2_MODEL_PATH")
        else:
            raise Exception("Invalid model type")

        if not binary_path or not model_path:
            raise Exception(f"LLAMA_{model_type.toupper()}_BINARY_PATH or LLAMA_{model_type.toupper()}_MODEL_PATH not set")

        LLAMA_THREADS_NUM = os.getenv("LLAMA_THREADS_NUM", "8")

        # run the mpt binary as a subprocess and get the result
        binary_path = os.path.expanduser(binary_path)
        model_path = os.path.expanduser(model_path)

        cmd = [
            binary_path,
            "--model", model_path,
            "--prompt", prompt,
            "--temp", "0.3",
            "--ctx-size", "2048",
            "--threads", LLAMA_THREADS_NUM,
            "--repeat_penalty", "1.1"
        ]
        result_obj = subprocess.run(cmd, capture_output=True, text=True)

        if result_obj.returncode != 0:
            result = "Error generating response"
        else:
            # remove everything before the prompt
            result = result_obj.stdout.split(prompt)[1]
            # remove everything after the response
            result = result.split("main: mem per token = ")[0]
            result = result.strip()

        return result

    def ask_mpt(self, prompt: str):
        mpt_binary_path = os.getenv("MPT_BINARY_PATH")
        mpt_model_path = os.getenv("MPT_MODEL_PATH")
        if not mpt_binary_path or not mpt_model_path:
            raise Exception("MPT_BINARY_PATH or MPT_MODEL_PATH not set")
        
        # run the mpt binary as a subprocess and get the result
        mpt_binary_path = os.path.expanduser(mpt_binary_path)
        mpt_model_path = os.path.expanduser(mpt_model_path)
        mpt_cmd = [
            mpt_binary_path,
            "--model", mpt_model_path,
            "--prompt", prompt,
            "--threads", "7",
            "--temp", "0.2",
            "--n_predict", "256",
        ]
        result_raw = subprocess.run(mpt_cmd, capture_output=True, text=True).stdout

        # remove everything before the prompt
        result = result_raw.split(prompt)[1]
        # remove everything after the response
        result = result.split("main: mem per token = ")[0]

        return result

    def ask(self, prompt: str):
        model_type = os.getenv("LLM_TYPE", "llama_cpp")
        prompt_type = os.getenv("LLM_PROMPT_TYPE", "plain")
        logging.getLogger("gthnk").info(f"Using LLM type: {model_type}, prompt type: {prompt_type}")

        context = self.get_context(prompt=prompt, model_type=model_type)

        if prompt_type == "wizard":
            prompt_fmt = wizard_prompt
        else:
            prompt_fmt = plain_prompt
        prompt = prompt_fmt.format(prompt=prompt, context=context)

        logging.getLogger("gthnk").info(f"Prompting LLM: {prompt}")

        if model_type == "llama_ggmlv2":
            result = self.ask_llama_ggmlv2(prompt)
        elif model_type == "llama_ggmlv3":
            result = self.ask_llama_ggmlv3(prompt)
        elif model_type == "llama":
            result = self.ask_llama(prompt)
        elif model_type == "mpt":
            result = self.ask_mpt(prompt)

        logging.getLogger("gthnk").info(f"LLM response: {result}")
        return result


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

wizard_prompt = """Below is context and an instruction that describes a task. Write a response that appropriately completes the request.
### Context:
{context}
### Instruction:
{prompt}
### Response:"""

plain_prompt = """Consider this list of statements, which provide context for the following question:

{context}

Based on that context, answer the following question: {prompt}'"""