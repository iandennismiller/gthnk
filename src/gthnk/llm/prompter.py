class Prompter(object):
    def __init__(self, prompt_type:str):
        if prompt_type == "instruct":
            self.prompt_fmt = instruct_prompt
        elif prompt_type == "summary":
            self.prompt_fmt = summary_prompt
        else:
            raise ValueError(f"Invalid prompt type: {prompt_type}")

    def get_prompt(self, query:str, context:str):
        return self.prompt_fmt.format(
            query=query,
            context=context
        )


###
# Summary Prompt

summary_prompt = """You are SummarizingAgent. When you are given a list, you are able to summarize it with 10 detailed items expressing the main ideas of the list.

{context}

### Instruction: What are the main ideas in list above? Respond with a detailed summary.
### Response: """

###
# Instruct Prompt

instruct_prompt = """You are ContextAgent. When you are given context and an instruction, you have the ability to use that context while responding to the instruction. Do not respond with a list unless asked to do so. 

{context}
### Instruction: Synthesize the information above to respond to the following. {query}
### Response: """
