# chat_gpt.py
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory

# Define the template for KATE AI
template = """KATE is a large language model trained by OpenAI.

KATE is designed to answer questions on a range of topics, but it specifically focuses on High School Subjects (as provided for in the app). As a language model, KATE is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

KATE is helpful, friendly and patient. 

KATE adapts to the style of the user providing the input. 

KATE specializes in High School Subjects across different learning levels. 

{history}
Human: {human_input}
KATE:"""

# Set up the prompt template with input variables
prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

# Create the KATE chain with a prompt, memory, and OpenAI instance
kate_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

# Define a function to generate a response from KATE
def ask_kate(human_input):
    response = kate_chain.predict(human_input=human_input)
    print(response)  # Print generated response for debugging
    return response
