import os
import logging
import subprocess


class MptGgml(object):

    def ask_mpt(self, prompt: str):
        mpt_binary_path = os.getenv("MPT_BINARY_PATH")
        mpt_model_path = os.getenv("MPT_MODEL_PATH")
        if not mpt_binary_path or not mpt_model_path:
            raise Exception("MPT_BINARY_PATH or MPT_MODEL_PATH not set")
        
        # run the mpt binary as a subprocess and get the result
        mpt_binary_path = os.path.expanduser(mpt_binary_path)
        mpt_model_path = os.path.expanduser(mpt_model_path)
        mpt_cmd = [
            mpt_binary_path,
            "--model", mpt_model_path,
            "--prompt", prompt,
            "--threads", "7",
            "--temp", "0.2",
            "--n_predict", "256",
        ]
        result_raw = subprocess.run(mpt_cmd, capture_output=True, text=True).stdout

        # remove everything before the prompt
        result = result_raw.split(prompt)[1]
        # remove everything after the response
        result = result.split("main: mem per token = ")[0]

        return result
