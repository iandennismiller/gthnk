import os
import logging

from .context import ContextStorage
from .llama import Llama


class LLM(object):
    "An LLM with integrated prompt generation and context retrieval"

    def __init__(self, gthnk):
        self.gthnk = gthnk

    @property
    def context_db(self):
        if not hasattr(self, "_context_db"):
            self._context_db = ContextStorage()
        return self._context_db

    def get_llama(self, model_size:str, prompt_type:str):
        "Return the LLM object for a given model size and prompt type"

        if model_size == "big":
            model_path = os.getenv("LLAMA_BIG_MODEL_PATH")
        elif model_size == "small":
            model_path = os.getenv("LLAMA_SMALL_MODEL_PATH")

        return Llama(
            model_path=model_path,
            prompt_type=prompt_type,
            context_db=self.context_db,
        )

    def refresh_embeddings(self):
        logging.getLogger("gthnk").info(f"Refreshing Chroma DB embeddings for entries...")

        created_count = 0
        exists_count = 0

        for day in self.gthnk.journal.days.values():
            for entry in day.entries.values():
                created = self.context_db.add(entry)
                if created:
                    created_count += 1
                else:
                    exists_count += 1

        logging.getLogger("gthnk").info(f"Refreshed entries in LLM context db: created {created_count}, exists {exists_count}")

    def summarize(self, query:str):
        "Use LLM to summarize a list of context items"
        return self.get_llama(model_size="big", prompt_type="summary").query(query)

    def instruct(self, query:str):
        "Send an instruction to the LLM and return the response"
        return self.get_llama(model_size="big", prompt_type="instruct").query(query)

    def table(self, query:str):
        "Use LLM to summarize a table"
        return self.get_llama(model_size="small", prompt_type="table").query(query)

    def keywords(self, query:str):
        "Use LLM to extract keywords from a list"
        return self.get_llama(model_size="big", prompt_type="keyword").query(query)

    def ask(self, query:str):
        "Use LLM to extract keywords from a list"
        return self.get_llama(model_size="big", prompt_type="ask").query(query)

    def cascade_summarize(self, query:str):
        "Use cascaded models to summarize, then query"
        summary_llm = self.get_llama(model_size="small", prompt_type="summary")
        instruct_llm = self.get_llama(model_size="big", prompt_type="instruct")
        context = summary_llm.query(query)
        return instruct_llm.query(query, context=context)

    def cascade_filtered(self, query:str):
        "Use cascaded models to filter, then query"
        filter_llm = self.get_llama(model_size="small", prompt_type="filter")
        instruct_llm = self.get_llama(model_size="big", prompt_type="instruct")
        context = filter_llm.query(query)
        return instruct_llm.query(query, context=context)

