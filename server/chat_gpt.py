from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import PyPDFLoader
from .chroma_qa import get_retrieval_qa_result, load_pdfs
import os

pdf_file_paths = load_pdfs()
loaders = [PyPDFLoader(pdf_path) for pdf_path in pdf_file_paths]
index = VectorstoreIndexCreator().from_loaders(loaders)

template = """KATE is a large language model trained by OpenAI.

KATE is designed to answer questions on a range of topics, but it specifically focuses on High School Subjects (as provided for in the app). As a language model, KATE is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

KATE is always friendly, patient, helpful and delightful. 

{history}
Human: {human_input}
KATE:"""

prompt = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

kate_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=5),
)

def ask_kate(human_input):
    # Perform retrieval-based question-answering to find context from indexed PDFs
    question = human_input.strip()
    context = ""  # You can provide a context here if necessary
    retrieval_result = get_retrieval_qa_result(question, context)
    found_context = retrieval_result["context"]

    # If a context is found, include it in the conversation with KATE
    if found_context:
        kate_input = f"Context: {found_context}\nHuman: {question}"
    else:
        kate_input = question

    response = kate_chain.predict(human_input=kate_input)
    return response
