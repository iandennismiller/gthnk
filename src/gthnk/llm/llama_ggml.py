import os
import logging
import subprocess


class LlamaGgml(object):

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
        model_filename = os.path.basename(model_path)
        model_filename_noext = os.path.splitext(model_filename)[0]

        cmd = [
            binary_path,
            "--model", model_path,
            "--prompt", prompt,
            "--prompt-cache", os.path.expanduser(f"~/.ai/cache/{model_filename_noext}.cache"),
            "--temp", "0.2",
            "--ctx-size", "2048",
            "--threads", LLAMA_THREADS_NUM,
        ]
        logging.getLogger("gthnk").info(f"Running LLAMA: {model_path}" + "\n")
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
