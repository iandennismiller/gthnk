import os
import logging
import datetime
import subprocess

from .prompter import Prompter
from llama_cpp import Llama as LlamaCpp


class Llama(object):
    """
    Llama is a wrapper around the llama.cpp binary, which must be installed separately.
    """

    def __init__(self, model_path, prompt_type, context_db):
        # determine model type from model path
        if "guanaco" in model_path.lower():
            model_type = "guanaco"
        elif "vicuna" in model_path.lower():
            model_type = "vicuna"
        elif "alpaca" in model_path.lower():
            model_type = "alpaca"
        elif "hermes" in model_path.lower():
            model_type = "alpaca"

        self.prompter = Prompter(model_type=model_type, prompt_type=prompt_type)

        # extract model name
        self.model_path = os.path.expanduser(model_path)
        model_filename = os.path.basename(model_path)
        model_filename_noext = os.path.splitext(model_filename)[0]
        logging.getLogger("gthnk").info(f"Llama(prompt='{prompt_type}', model='{model_filename_noext}')")
        
        # prompt cache
        prompt_cache_path = os.getenv("LLAMA_PROMPT_CACHE_PATH", "/tmp")
        self.cache_filename = os.path.join(os.path.expanduser(prompt_cache_path), f"{model_filename_noext}.cache")
        logging.getLogger("gthnk").debug(f"Llama prompt cache: {self.cache_filename}")

        # ggml binary
        binary_path = os.getenv("LLAMA_BINARY_PATH")
        if not binary_path:
            raise Exception(f"LLAMA_BINARY_PATH not set")
        self.binary_path = os.path.expanduser(binary_path)
        logging.getLogger("gthnk").debug(f"Llama binary: {self.binary_path}")

        # store queries and results in a separate file (i.e. not the main log)
        self.log_filename = os.path.expanduser(os.getenv("LLM_LOG", "/tmp/gthnk-llm.log"))
        self.num_threads = os.getenv("LLAMA_NUM_THREADS", "6")
        self.context_db = context_db

    def save_interaction(self, message: str):
        with open(self.log_filename, "a") as f:
            # get date and time as YYYY-MM-DD HHMM
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H%M")
            f.write(f"{datetime_str}\n\n> {message}\n\n")

    def get_context(self, query: str):
        "Generate context from ContextStorage with parameters suitable for LLAMA"
        context_list = self.context_db.query(query=query)
        logging.getLogger("gthnk").info(f"Generated {len(context_list)+1} context items for query: {query}")

        return self.context_db.as_string(
            context_list=context_list,
            max_item_tokens = 64,
            max_context_tokens = 384,
        )

    def query(self, query_str:str, context:str=None, prompt_type:str="instruct"):
        self.save_interaction(message=query_str)
        prompt = self.prompter.get_prompt(
            query=query_str,
            context=context if context else self.get_context(query_str)
        )
        result = self.send(prompt)
        self.save_interaction(message=result)
        return result

    def send(self, prompt: str):
        "Send prompt to the llama.cpp binary and return the response"

        cmd = [
            self.binary_path,
            "--prompt", prompt,
            "--model", self.model_path,
            "--temp", "0.4",
            "--ctx-size", "2048",
            "--batch-size", self.num_threads,
            "--n-predict", "384",
            "--threads", self.num_threads,
            # "--prompt-cache", self.cache_filename,
            # "--prompt-cache-all",
        ]

        # log the prompt and start time
        logging.getLogger("gthnk").info(f"LLM prompt: {prompt}")
        start_time = datetime.datetime.now()

        # run the llama.cpp binary as a subprocess and get the result
        result_obj = subprocess.run(cmd, capture_output=True, text=True)

        # log the result and end time
        end_time = datetime.datetime.now()
        logging.getLogger("gthnk").info(f"LLM elapsed time: {end_time - start_time}")

        # process the result
        if result_obj.returncode != 0:
            logging.getLogger("gthnk").error(result_obj.stderr)
            result = "Error generating response"
        else:
            # remove everything before the prompt
            result = result_obj.stdout.split(prompt)[1]

            # remove everything after the response
            result = result.split("main: mem per token = ")[0]
            result = result.strip()
            logging.getLogger("gthnk").info(f"LLM response: {result}")

        return result

    def send_prompt_pythonic(self, prompt: str):
        LLAMA_THREADS_NUM = int(os.getenv("LLAMA_THREADS_NUM", 6))
        if os.getenv("LLAMA_MODEL_PATH"):
            LLAMA_MODEL_PATH = os.path.expanduser(os.getenv("LLAMA_MODEL_PATH"))
            logging.getLogger("gthnk").info(f"Loading LLAMA: {LLAMA_MODEL_PATH}" + "\n")
        else:
            raise Exception("LLAMA_MODEL_PATH not set")

        # with open('/dev/null', 'w') as f:
        #     with redirect_stderr(f):
        #         with redirect_stdout(f):
        if not hasattr(self, "llm"):
            self.llm = LlamaCpp(
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
