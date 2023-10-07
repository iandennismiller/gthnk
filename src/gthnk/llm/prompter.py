import os


class Prompter(object):
    def __init__(self, prompt_type:str, model_type:str, your_name:str):
        self.model_setup = model_setup.get("llama")
        self.your_name = your_name

    def get_prompt(self, query:str, context:str):
        prompt_fmt = self.model_setup["turn_template"]
        return prompt_fmt.format(
            setting=self.model_setup["setting"],
            query=query,
            context=context,
            your_name = self.your_name,
        )

###
# Symbols used to prompt various models

model_setup = {
    "guanaco": {
        "setting": "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n",
        "turn_template": "{setting}\n### Human: {instruction_1}\n------------\n{context}\n------------\n{instruction_2}\n### Assistant: ",
    },
    "vicuna": {
        "setting": "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n",
        "turn_template": "{setting}\nUSER: {instruction_1}\n------------\n{context}\n------------\n{instruction_2}\nASSISTANT: ",
    },
    "alpaca": {
        "setting": "Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.",
        "turn_template": "{setting}\n\n### Instruction:\n{instruction_1} {instruction_2}\n\n### Input:\n{context}\n\n### Response:\n",
    },
    "based": {
        "setting": "A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.\n",
        "turn_template": "{setting}\nHuman: {instruction_1}\n------------\n{context}\n------------\n{instruction_2}\nAssistant: ",
    },
    "orca": {
        "setting": "",
        "turn_template": "### System:\nYou are an AI assistant named {your_name} that follows instruction extremely well. Help as much as you can.\n\n### User:\n{query}\n\n### Input:\nThe following are your journal entries, which can help in completing this task.\n{context}\n\n### Response:\n",
    },
    "mistral": {
        "setting": "",
        "turn_template": "### System:\nYou are an AI assistant named {your_name} that follows instruction extremely well. Help as much as you can.\n\n### User:\n{query}\n\n### Input:\nThe following are your journal entries, which can help in completing this task.\n{context}\n\n### Response:\n",
    },
    "scarlett": {
        "setting": "",
        "turn_template": "### System:\nYou are an AI assistant named {your_name} that follows instruction extremely well. Help as much as you can.\n\n### User:\n{query}\n\n### Input:\nThe following are your journal entries, which can help in completing this task.\n{context}\n\n### Response:\n",
    },
    "hermes": {
        "setting": "",
        "turn_template": "### System:\nYou are an AI assistant named {your_name} that follows instruction extremely well. Help as much as you can.\n\n### User:\n{query}\n\n### Input:\nThe following are your journal entries, which can help in completing this task.\n{context}\n\n### Response:\n",
    },
    "llama": {
        "setting": "",
        "turn_template": "### System:\nYou are an AI assistant named '{your_name}' that answers queries by referring to your own journal entries. For each query you receive, you will also be provided with relevant journal entries that can help respond to the query.\n\n### Input:\nThe following journal entries may be relevant to this query:\n\n{context}\n\n### User:\n{query}\n\n### Response:\n",
    },
}
