import os
import logging
import subprocess


class LlamaCpp(object):

    def ask_llama_cpp(self, prompt: str):
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
