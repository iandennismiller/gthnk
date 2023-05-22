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
from .gpt_neox import GptNeoxGgml

from . import prompts
from .vectordb import DefaultEntriesStorage


class LLM(LlamaGgml, LlamaCpp, MptGgml, GptJGgml, GptNeoxGgml):

    def __init__(self):
        logging.getLogger("gthnk").info("Initializing Vector DB...")
        self.context_db = DefaultEntriesStorage()

        self.model_type = os.getenv("LLM_TYPE", "llama_cpp")
        model_ask_method_name = f"ask_{model_type}"

        if hasattr(self, model_ask_method_name):
            self._ask_llm = getattr(self, model_ask_method_name)
            logging.getLogger("gthnk").info(f"LLM type: {model_type}")
        else:
            raise Exception(f"Unknown LLM type: {model_type}")

        self.prompt_type = os.getenv("LLM_PROMPT_TYPE", "plain")
        logging.getLogger("gthnk").info(f"LLM prompt type: {self.prompt_type}")

    def get_context(self, query, num_query_results, max_item_tokens, max_context_tokens):
        context_list = self.context_db.query(query=query, top_num=num_query_results)

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

    def get_prompt(self, query:str, context, prompt_type):
        prompt_var = f"{prompt_type}_prompt"

        if prompt_var in prompts:
            prompt_fmt = prompts[prompt_var]
            return prompt_fmt.format(
                query=query,
                context=context,
                agent_prompt=agent_prompt,
            )
        else:
            raise ValueError(f"Invalid prompt type: {prompt_type}")

    def ask(self, query: str):
        context = self.get_context(query=query, **context_params[model_type])
        prompt = self.get_prompt(query=query, context=context, prompt_type=self.prompt_type)

        logging.getLogger("gthnk").info(f"Prompting LLM: {prompt}")
        result = self._ask_llm(prompt)
        logging.getLogger("gthnk").info(f"LLM response: {result}")
        return result


context_params = {
    "llama_ggml": {
        "num_query_results": 50,
        "max_item_tokens": 96,
        "max_context_tokens": 1024,
        },
    "llama": {
        "num_query_results": 50,
        "max_item_tokens": 40,
        "max_context_tokens": 256,
        },
    "mpt": {
        "num_query_results": 100,
        "max_item_tokens": 64,
        "max_context_tokens": 2048,
        },
    "gptj": {
        "num_query_results": 50,
        "max_item_tokens": 128,
        "max_context_tokens": 1024,
        },
    "gptneox": {
        "num_query_results": 50,
        "max_item_tokens": 128,
        "max_context_tokens": 1024,
    },
}
