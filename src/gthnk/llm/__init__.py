import os
import sys
import logging
import subprocess

from dotenv import load_dotenv
load_dotenv()

from .llama_ggml import LlamaGgml
from .llama_cpp import LlamaCpp
from .mpt import MptGgml
from .gptj import GptJGgml

from .prompts import *
from .vectordb import DefaultEntriesStorage


class LLM(LlamaGgml, LlamaCpp, MptGgml, GptJGgml):

    def __init__(self):
        logging.getLogger("gthnk").info("Initializing Vector DB...")
        self.context_db = DefaultEntriesStorage()

    def get_context(self, prompt, model_type):
        logging.getLogger("gthnk").info("Generating context...")

        if model_type in ["llama_ggmlv2", "llama_ggmlv3"]:
            num_query_results = 50
            max_item_tokens = 64
            max_context_tokens = 1024
        elif model_type == "llama":
            num_query_results = 50
            max_item_tokens = 40
            max_context_tokens = 256
        elif model_type == "mpt":
            num_query_results = 100
            max_item_tokens = 64
            max_context_tokens = 2048
        elif model_type == "gptj":
            num_query_results = 50
            max_item_tokens = 32
            max_context_tokens = 384

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

    def ask(self, prompt: str):
        model_type = os.getenv("LLM_TYPE", "llama_cpp")
        prompt_type = os.getenv("LLM_PROMPT_TYPE", "plain")
        logging.getLogger("gthnk").info(f"Using LLM type: {model_type}, prompt type: {prompt_type}")

        context = self.get_context(prompt=prompt, model_type=model_type)

        if prompt_type == "wizard":
            prompt_fmt = wizard_prompt
        elif prompt_type == "manticore":
            prompt_fmt = manticore_prompt
        elif prompt_type == "vicuna":
            prompt_fmt = vicuna_prompt
        elif prompt_type == "vicuna_v1":
            prompt_fmt = vicuna_v1_prompt
        elif prompt_type == "kobold":
            prompt_fmt = kobold_prompt
        else:
            prompt_fmt = plain_prompt

        prompt = prompt_fmt.format(
            prompt=prompt,
            context=context,
            agent_prompt=agent_prompt,
        )

        logging.getLogger("gthnk").info(f"Prompting LLM: {prompt}")

        if model_type == "llama_ggmlv2":
            result = self.ask_llama_ggmlv2(prompt)
        elif model_type == "llama_ggmlv3":
            result = self.ask_llama_ggmlv3(prompt)
        elif model_type == "llama":
            result = self.ask_llama(prompt)
        elif model_type == "mpt":
            result = self.ask_mpt(prompt)
        elif model_type == "gptj":
            result = self.ask_gptj(prompt)

        logging.getLogger("gthnk").info(f"LLM response: {result}")
        return result
