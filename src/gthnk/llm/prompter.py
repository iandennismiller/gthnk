import os
import re


class Prompter(object):
    def __init__(self, prompt_type:str):
        if prompt_map.get(prompt_type):
            self.prompt_fmt = prompt_map.get(prompt_type)
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
            items = []

            for i, c in enumerate(context_list):
                item = c
                item = re.sub("\s+", " ", item)
                item = re.sub(r" \.\.\. ", ". ", item)
                item = re.sub(r" \.\.\.", ".", item)
                item = re.sub(r"\.\.\.", ".", item)
                item = re.sub(r"^- \[ \] ", "; ", item)
                item = re.sub(r"^- ", "; ", item)
                item = re.sub(r" - ", "; ", item)
                item = re.sub(r"^Okay.\s", "", item)
                item = re.sub(r"^So\s", "", item)
                item = re.sub(r"\n", " ", item)

                item_token_count = len(item.split(" "))
                if item_token_count > max_item_tokens:
                    item = " ".join(item.split(" ")[:max_item_tokens]) + "..."
                    item_token_count = len(item.split(" "))

                current_token_count = len("\n".join(items).split(" "))
                if current_token_count + item_token_count > max_context_tokens:
                    break
                
                # context_task += f'{i+1}. {item}\n'
                # context_task += f'{item}\n\n'
                items.append(f'- {item}')

            return "\n".join(items)
        else:
            return


###
# Filter Prompts

summary_prompt = """### Instruction: We have provided context information below.
------------
{context}
------------
Rewrite the items in this list to summarize the main ideas with as much detail as necessary.
### Response: """


filter_prompt = """### Instruction: We have provided context information below.
------------
{context}
------------
Rewrite this list, keeping only those items related to the following topic: "{query}".
### Response: """


keyword_prompt = """### Instruction: Some text is provided below.
------------
{context}
------------
Given the text, extract up to 6 keywords from the text. Avoid stopwords. Provide keywords in comma-separated format.
### Response: """


table_prompt = """### Instruction: Some text is provided below.
------------
{context}
------------
Given this text, classify each item by topic add it to a table with columns "topic" and "item".
### Response: """


###
# Directed Prompts

instruct_prompt = """### Instruction: You are {your_name}. We have provided context information below.
------------
{context}
------------
Based solely on the information above, write a response that appropriately completes this request: "{query}".
### Response: """


ask_prompt = """### Instruction: You are {your_name}. We have provided context information below.
------------
{context}
------------
Using the text above and no prior knowledge, compose a paragraph that answers the following question: "{query}".
### Response: """
# Explain which items in the text support your answer.


###
# Prompt map

prompt_map = {
    "instruct": instruct_prompt,
    "summary": summary_prompt,
    "filter": filter_prompt,
    "keyword": keyword_prompt,
    "table": table_prompt,
    "ask": ask_prompt,
}
