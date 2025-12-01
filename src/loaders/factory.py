from core.abstracts import LoaderAbstract
from loaders.pdf import PDFLoader

LOADERS: dict[str, type[LoaderAbstract]] = {
    "application/pdf": PDFLoader,
}

def get_loader(content_type: str) -> type[LoaderAbstract]:
    """
    Factory function that returns the appropriate loader class based on content type.
    """
    loader = LOADERS.get(content_type)
    if loader is None:
        raise ValueError(f"Unsupported content type: {content_type}")
    return loader

