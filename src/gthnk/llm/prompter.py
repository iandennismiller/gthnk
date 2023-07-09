import os


class Prompter(object):
    def __init__(self, prompt_type:str, model_type:str, your_name:str):
        # self.model_type = model_type
        self.model_setup = model_setup.get(model_type)
        # self.prompt_type = prompt_type
        self.prompt_data = prompts[prompt_type]
        self.your_name = your_name

    def get_prompt(self, query:str, context:str):
        prompt_fmt = self.model_setup["turn_template"]
        prompt_resolved_1 = prompt_fmt.format(
            setting=self.model_setup["setting"],
            instruction_1=self.prompt_data["instruction_1"],
            instruction_2=self.prompt_data["instruction_2"],
            context=context,
        )
        prompt_resolved_2 = prompt_resolved_1.format(
            your_name=self.your_name,
            query=query,
        )
        return prompt_resolved_2

    @classmethod
    def classify_model(cls, model_path:str):
        model_path_lower = model_path.lower()

        # determine model type from model path
        if "guanaco" in model_path_lower:
            return "guanaco"
        elif "vicuna" in model_path_lower:
            return "vicuna"
        elif "alpaca" in model_path_lower:
            return "alpaca"
        elif "hermes" in model_path_lower:
            return "alpaca"
        elif "orca" in model_path_lower:
            return "orca"

###
# Prompt map

prompts = {
    "instruct": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Using the context and no prior knowledge, write a response that appropriately completes this request: \"{query}\"",
    },
    "summary": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Summarize the main ideas with as much detail as necessary.",
    },
    "filter": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Rewrite the context, keeping only those items related to the following topic: \"{query}\".",
    },
    "keyword": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Given this information, extract up to 6 keywords from the text. Avoid stopwords. Provide keywords in comma-separated format.",
    },
    "table": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Given this context, classify each item by topic add it to a table with columns \"topic\" and \"item\".",
    },
    "ask": {
        "instruction_1": "Your name is {your_name}. The context information below was retrieved from {your_name}'s journal.",
        "instruction_2": "Using the context and no prior knowledge, compose a paragraph that answers the following question: \"{query}\"", # Explain which items in the text support your answer.
    },
}


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
        "turn_template": "### System:\nYou are an AI assistant named {{your_name}} that follows instruction extremely well. Help as much as you can.\n\n### User:\n{{query}}\n\n### Input:\nThe following are your journal entries, which can help in completing this task.\n{context}\n\n### Response:\n",
    }
}
