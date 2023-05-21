import os
import logging
import subprocess


class GptJGgml(object):

    def ask_gptj(self, prompt: str):
        binary_path = os.getenv("GPTJ_BINARY_PATH")
        model_path = os.getenv("GPTJ_MODEL_PATH")
        if not binary_path or not model_path:
            raise Exception("GPTJ_BINARY_PATH or GPTJ_MODEL_PATH not set")
        
        # run the mpt binary as a subprocess and get the result
        binary_path = os.path.expanduser(binary_path)
        model_path = os.path.expanduser(model_path)
        cmd = [
            binary_path,
            "--model", model_path,
            "--prompt", prompt,
            "--threads", "8",
            "--temp", "0.3",
            "--n_predict", "256",
        ]
        result_raw = subprocess.run(cmd, capture_output=True, text=True).stdout

        # remove everything before the prompt
        result = result_raw.split(prompt)[1]
        # remove everything after the response
        result = result.split("main: mem per token = ")[0]
        result = result.replace('<|endoftext|>', '')

        return result
