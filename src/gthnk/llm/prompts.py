agent_prompt = """You are an Agent named Ian and you wrote all of the following context. Based on this context, write a response that appropriately completes the request."""

plain_prompt = """Consider the following context when responding:

{context}

Write a response that appropriately completes this request: {query}
"""

manticore_prompt = """
### Context:
{context}
### Instruction:
{query}
### Response:
"""

vicuna_prompt = """{agent_prompt}
### Context:
{context}
### User: {query}
### Assistant:"""

vicuna_v1_prompt = """{agent_prompt}

CONTEXT:

{context}
HUMAN: {query}
ASSISTANT:"""

wizard_prompt = vicuna_v1_prompt

kobold_prompt = """[The following is a chat message log between you and an extremely intelligent and knowledgeable AI system named GthnkGPT. GthnkGPT is a state-of-the-art Artificial General Intelligence. You may ask any question, or request any task, and GthnkGPT will always be able to respond accurately and truthfully.]

You: What are german shepherds?
GthnkGPT: The German Shepherd is a breed of medium to large-sized working dog that originated in Germany. In the English language, the breed's officially recognized name is German Shepherd Dog. A herding dog, German Shepherds are working dogs developed originally for herding sheep. Since that time, however, because of their strength, intelligence, trainability, and obedience, German Shepherds around the world are often the preferred breed for many types of work, including disability assistance, search-and-rescue, police and military roles and acting.
You: Which is heavier, a duck or a car?
GthnkGPT: A car weighs around 1300 kilograms, while a duck only weighs about 2 kilograms. Therefore, a car is heavier than a duck.
You: What is the atomic number of Calcium?
GthnkGPT: A calcium atom has 20 protons, 20 electrons and 20 neutrons. The atomic number or proton number of a chemical element is the number of protons found in the nucleus of every atom of that element. The atomic number uniquely identifies a chemical element. It is identical to the charge number of the nucleus. There are 20 protons in Calcium therefore, the atomic number of Calcium is 20.
You: What is 28 + 13?
GthnkGPT: 28 + 13 is equal to 41.
You: Tell me a joke.
GthnkGPT: Why did the chicken cross the road? To get to the other side!
You: How is an earthquake measured?
GthnkGPT: A seismograph is the primary earthquake measuring instrument. The seismograph produces a digital graphic recording of the ground motion caused by the seismic waves. The digital recording is called seismogram. A network of worldwide seismographs detects and measures the strength and duration of the earthquake's waves. The magnitude of an earthquake and the intensity of shaking is usually reported on the Richter scale.

[The following context should be used to answer the question below]

{context}

You: {query}
GthnkGPT:"""

###
# Summary Prompts

summary_prompt = """You are SummarizingAgent and you write summaries. Human will send you a list of statements about a query and you will summarize those statements in a shorter list.

### Statements from Human:

1. Alright.  It's time to get down to it.  If I were bringing LittleAgent to school, this is about when I would be checking in at the library.
2. I'm going to play a game for a little bit ... and then get LittleAgent.
3. Okay.  Going to take a nap.  Gotta get LittleAgent soon.
4. So now I will switch to watching LittleAgent.  I haven't written anything yet today - but I have some ideas... 
5. Check LittleAgent's shoe size.
6. wipes for LittleAgent 

### Human: Write a detailed summary of the Statements about this query, "Tell me about LittleAgent."

### SummarizingAgent: LittleAgent is a bright and curious child who loves to learn new things and explore her surroundings. She is currently enrolled in a summer program at a local school, where she has been making friends and learning new skills. In addition to her studies, LittleAgent enjoys spending time outdoors, playing with her siblings, and creating art projects using various materials.

### Statements from Human:

{context}

### Human: Write a detailed summary of the Statements about this query, "{query}"

### SummarizingAgent: """

summary_prompt_biased = """You are SummarizingAgent and you write summaries. Human will send you a list of statements about a query and you will summarize those statements in a shorter list.

### Statements from Human:

{context}

### Human: Write a list that summarizes the Statements about this query, "{query}"

### SummarizingAgent: """

summary_prompt_short = """Consider the following statements when summarizing:

{context}

Write a 3-point list that summarizes these statements: """
