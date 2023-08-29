# Main file for resume parsing

import os
from ingest import parse_pdf_without_pages, merge_hyphenated_words, fix_newlines, remove_multiple_newlines, clean_text_without_pages
from parser_openai import text_to_docs_without_pages, make_chain, start_parsing
import json
import shutil

from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from prompts import *

query = query_1




def delete_old_chroma(folder_path):
  try:
      # List all items (files and subdirectories) in the folder
      items = os.listdir(folder_path)

      # Loop through items and remove each one
      for item in items:
          item_path = os.path.join(folder_path, item)
          if os.path.isfile(item_path):
              os.remove(item_path)
              print(f"File '{item}' removed successfully.")
          elif os.path.isdir(item_path):
              shutil.rmtree(item_path)
              print(f"Folder '{item}' removed successfully.")
          else:
              print(f"Skipping '{item}' as it's neither a file nor a folder.")

      print("All files and folders removed.")

  except Exception as e:
      print(f"Error removing items from folder '{folder_path}': {e}")

def main():
    # Load env
    load_dotenv()

    FOLDER_PATH = './cv'
    DONE_PATH = './cv_processed'
    CHROMA_DIR = "chroma/cv"
    DEST_PATH = './cv_output'
    FILE_NAME = 'resume_1.pdf'
    count = 1
    
    embedding = OpenAIEmbeddings()
    
    delete_old_chroma(CHROMA_DIR)

    if FILE_NAME.endswith('.pdf'):
      print("\n---\n")
      print("...Parsing file: %s ... " % FILE_NAME)
      file_path = os.path.join(FOLDER_PATH, FILE_NAME)
        # Extract raw text
      raw_pages = parse_pdf_without_pages(file_path)
        # Step 2: Create text chunks
      cleaning_functions = [
            merge_hyphenated_words,
            fix_newlines,
            remove_multiple_newlines,
            ]
      cleaned_text_pdf = clean_text_without_pages(raw_pages, cleaning_functions)
      document_chunks = text_to_docs_without_pages(cleaned_text_pdf, chunk_size=4000)
      COLLECTION_NAME = "resume_" + str(count).zfill(3)

      vector_store = Chroma.from_documents(
        document_chunks,
        embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )

      # Save DB locally
      vector_store.persist()

      chain = make_chain(embedding, COLLECTION_NAME, CHROMA_DIR)
      try:
        start_parsing(chain, query, DEST_PATH, COLLECTION_NAME)
        # count += 1
        destination_path = os.path.join(DONE_PATH, FILE_NAME)
        shutil.move(file_path, destination_path)
        print(f"Moved '{FILE_NAME}' to '{DONE_PATH}'")
        # print(count)
      except:
        pass
    elif FILE_NAME.endswith('.docx'):
      ## TODO: Implement this function
      pass

if __name__ == '__main__':
    main()
