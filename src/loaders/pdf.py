from core import LoaderAbstract
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from shared import logger

class PDFLoader(LoaderAbstract):
    """
    A loader for PDF files using langchain.
    """
    @staticmethod
    def load(source: str) -> list[Document]:
        logger.info(f"Loading PDF file: {source}")
        return PyPDFLoader(source).load()