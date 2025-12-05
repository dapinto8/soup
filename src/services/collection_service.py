from core import VectorStoreAbstract, Collection

class CollectionService:
    """
    A service for managing collections.
    """

    def __init__(self, store: VectorStoreAbstract):
        self._store = store

    def get_collections(self) -> list[Collection]:
        return self._store.get_collections()

    def collection_exists(self, name: str) -> bool:
        return self._store.collection_exists(collection_name=name)

    def create_collection(self, name: str) -> Collection:
        if self.collection_exists(name):
            raise ValueError(f"Collection {name} already exists")
        if not name:
            raise ValueError("Collection name cannot be empty")

        return self._store.create_collection(collection_name=name)

    def delete_collection(self, name: str) -> None:
        self._store.delete_collection(collection_name=name)

