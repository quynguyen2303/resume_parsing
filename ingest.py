import os
import re
import pdfplumber
from typing import Callable, Dict, List, Tuple





def merge_hyphenated_words(text: str) -> str:
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)

def fix_newlines(text: str) -> str:
    return re.sub(r"(?<!\n)\n(?!\n)", " ", text)

def remove_multiple_newlines(text: str) -> str:
    return re.sub(r"\n{2,}", "\n", text)

  #Without pages
def parse_pdf_without_pages(file_path: str) -> Tuple[List[str], Dict[str, str]]:
    """
    Extracts the title and text from each page of the PDF.

    :param file_path: The path to the PDF file.
    :return: A tuple containing the title and a list of tuples with page numbers and extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    pages = extract_text_from_pdf(file_path)

    return pages

# Without pages
def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Extracts the text from each page of the PDF.

    :param file_path: The path to the PDF file.
    :return: A list of tuples containing the page number and the extracted text.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with pdfplumber.open(file_path) as pdf:
        pages = []
        text = ""
        for page_num, page in enumerate(pdf.pages):
            text += page.extract_text()
        if text.strip():  # Check if extracted text is not empty
            pages.append(text)
    return pages

def extract_text_from_doc(file_path: str) -> List[str]:
    """
    Extracts the text from each page of the PDF.

    :param file_path: The path to the PDF file.
    :return: A list of tuples containing the page number and the extracted text.
    """
    ##  TODO: Implement this function
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # with pdfplumber.open(file_path) as pdf:
    #     pages = []
    #     text = ""
    #     for page_num, page in enumerate(pdf.pages):
    #         text += page.extract_text()
    #     if text.strip():  # Check if extracted text is not empty
    #         pages.append(text)
    # return pages
    pass

# Without pages
def clean_text_without_pages(
    pages: List[str], cleaning_functions: List[Callable[[str], str]]
) -> List[str]:
    cleaned_pages = []
    for text in pages:
        for cleaning_function in cleaning_functions:
            text = cleaning_function(text)
        cleaned_pages.append(text)
    return cleaned_pages

