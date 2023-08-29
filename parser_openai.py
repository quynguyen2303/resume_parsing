from typing import Callable, Dict, List, Tuple
import json

import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks import get_openai_callback



# Without pages
def text_to_docs_without_pages(text: List[str], chunk_size=4000) -> List[Document]:
    """Converts list of strings to a list of Documents with metadata."""
    doc_chunks = []
    # Break to multiple chunks

    for page in text:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=200,
        )

        chunks = text_splitter.split_text(page)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
            )
            doc_chunks.append(doc)

    # Add to only one chunk
    # for page in text:
    #   doc_chunks.append(Document(page_content=page))
    print("Total chunks of this resume: " + str(len(doc_chunks)))
    return doc_chunks

# Create chain to chat with OpenAI
def make_chain(embedding, collection_name, persist_directory):
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo-16k",
        temperature="0",
        # verbose=True
    )
    embedding = OpenAIEmbeddings()

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory=persist_directory,
    )

    return ConversationalRetrievalChain.from_llm(
        model,
        retriever=vector_store.as_retriever()
        #         return_source_documents=True,
        # verbose=True,
    )

def start_parsing(chain, query, folder_path, file_name, chat_history=[]):
  # Reset chat history for remove old tokens
  chat_history = []
  with get_openai_callback() as cb:
    try:
      response = chain({"question": query, "chat_history": chat_history})
      answer = response["answer"]
      chat_history.append(HumanMessage(content=query))
      chat_history.append(AIMessage(content=response["answer"]))
      print(cb)
      # print(f"Answer: {answer}")
    except Exception as e:
      print(cb)
      print(f"Error: {e}")

  try:
    data = json.loads(answer)
    file_path = os.path.join(folder_path, file_name + '_' + data['email'] + '.json')
    with open(file_path, 'w') as json_file:
      json.dump(data, json_file, indent=4)
    print("Saved to %s completed!" % file_path)

  except json.JSONDecodeError as json_err:
    print(f"JSON decoding error: {json_err}")
  except Exception as e:
    print(f"Error: {e}")