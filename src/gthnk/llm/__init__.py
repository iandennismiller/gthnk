import os

from .context import ContextStorage
from .llama import Llama


class LLM(object):
    "An LLM with integrated prompt generation and context retrieval"

    def __init__(self):
        context_db = ContextStorage()

        self.instruct_llm = Llama(
            model_path=os.getenv("LLAMA_INSTRUCT_MODEL_PATH"),
            prompt_type="instruct",
            context_db=context_db, 
        )
        self.summary_llm = Llama(
            model_path=os.getenv("LLAMA_SUMMARY_MODEL_PATH"),
            prompt_type="summary",
            context_db=context_db, 
        )

    def summarize(self, query:str):
        "Use LLM to summarize a list of context items"
        return self.summary_llm.query(query)

    def instruct(self, query:str, context:str=None):
        "Send an instruction to the LLM and return the response"
        return self.instruct_llm.query(query, context=context)

    def cascade(self, query:str):
        "Use cascaded models to summarize, then query"
        summary = self.summary_llm.query(query)
        return self.instruct_llm.query(query, context=summary)
