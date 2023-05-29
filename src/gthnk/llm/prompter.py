import os


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
            context=context,
            your_name=os.getenv("LLM_YOUR_NAME", "Gthnk")
        )

    def generate_context(self, context_list, max_item_tokens, max_context_tokens):
        "Format a list of context items into a string suitable for an LLM prompt"

        if context_list:
            context_task = ''

            for i, c in enumerate(context_list):
                item = c.replace("\n", " ")
                item_token_count = len(item.split(" "))

                if item_token_count > max_item_tokens:
                    item = " ".join(item.split(" ")[:max_item_tokens]) + "..."

                # context_task += f'{i+1}. {item}\n'
                context_task += f'{item}\n\n'

                token_count = len(context_task.split(" "))
                if token_count > max_context_tokens:
                    break

            return context_task
        else:
            return


###
# Summary Prompt

summary_prompt = """[You are {your_name}. When you are given a list, you are able to summarize it with 10 detailed items expressing the main ideas of the list.

{context}]

### Instruction: What are the main ideas in list above? Respond with a detailed summary that is not a numbered list.
### Response: """

###
# Instruct Prompt

instruct_prompt = """[You are {your_name}. The following facts are true, which you will combine to answer the question below. You may not copy and paste the facts, but you will use them to answer the question. These are the facts:

{context}]

### Instruction: Refer to those facts while responding to the following: {query}
### Response: """
