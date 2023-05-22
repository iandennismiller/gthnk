import os
import logging
import subprocess


class GptNeoxGgml(object):

    def ask_gpt_neox(self, prompt: str):
        binary_path = os.getenv("GPT_NEOX_BINARY_PATH")
        model_path = os.getenv("GPT_NEOX_MODEL_PATH")
        if not binary_path or not model_path:
            raise Exception("GPT_NEOX_BINARY_PATH or GPT_NEOX_MODEL_PATH not set")
        
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
