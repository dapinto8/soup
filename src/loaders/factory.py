from core import LoaderAbstract
from .pdf import PDFLoader

LOADERS: dict[str, type[LoaderAbstract]] = {
    ".pdf": PDFLoader,
}

def get_loader(file_extension: str) -> type[LoaderAbstract]:
    """
    Factory function that returns the appropriate loader class based on content type.
    """
    loader = LOADERS.get(file_extension)
    if loader is None:
        raise ValueError(f"Unsupported file extension: {file_extension}")
    return loader

