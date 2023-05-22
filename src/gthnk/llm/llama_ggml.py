import os
import logging
import subprocess


class LlamaGgml(object):

    def ask_llama_ggml(self, prompt: str):
        model_path = os.getenv("LLAMA_GGML_MODEL_PATH")
        if not model_path:
            raise Exception(f"LLAMA_GGML_MODEL_PATH not set")

        # extract model name
        model_path = os.path.expanduser(model_path)
        model_filename = os.path.basename(model_path)
        model_filename_noext = os.path.splitext(model_filename)[0]
        logging.getLogger("gthnk").info(f"Llama model: {model_filename_noext}")

        # prompt cache
        prompt_cache_path = os.getenv("LLAMA_GGML_PROMPT_CACHE_PATH", "/tmp")
        cache_filename = os.path.join(os.path.expanduser(prompt_cache_path), f"{model_filename_noext}.cache")
        logging.getLogger("gthnk").info(f"Llama prompt cache: {cache_filename}")

        # ggml binary
        binary_path = os.getenv("LLAMA_GGML_BINARY_PATH")
        if not binary_path:
            raise Exception(f"LLAMA_GGML_BINARY_PATH not set")
        binary_path = os.path.expanduser(binary_path)
        logging.getLogger("gthnk").info(f"Llama binary: {binary_path}")

        cmd = [
            binary_path,
            "--model", model_path,
            "--prompt", prompt,
            "--prompt-cache", cache_filename,
            "--temp", "0.3",
            "--ctx-size", "2048",
            "--threads", os.getenv("LLAMA_THREADS_NUM", "6"),
        ]

        # run the llama.cpp binary as a subprocess and get the result
        result_obj = subprocess.run(cmd, capture_output=True, text=True)

        if result_obj.returncode != 0:
            logging.getLogger("gthnk").error(result_obj.stderr)
            result = "Error generating response"
        else:
            # remove everything before the prompt
            result = result_obj.stdout.split(prompt)[1]
            # remove everything after the response
            result = result.split("main: mem per token = ")[0]
            result = result.strip()

        return result
