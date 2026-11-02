from models import Item, ItemCreate, ItemUpdate
from repositories import IItemsRepository


class ItemsService:
    def __init__(self, items_repository: IItemsRepository):
        self.items_repository = items_repository

    def get_items(self) -> list[Item]:
        return self.items_repository.get_all()

    def get_item_by_id(self, id: int) -> Item | None:
        return self.items_repository.get_by_id(id)

    def create_item(self, item: ItemCreate) -> Item:
        return self.items_repository.create(item)

    def update_item(self, id: int, changes: ItemUpdate) -> Item | None:
        item = self.items_repository.get_by_id(id)
        if not item:
            return None
        return self.items_repository.update(item, changes)

    def delete_item(self, id: int) -> bool:
        item = self.items_repository.get_by_id(id)
        if not item:
            return False
        self.items_repository.delete(item)
        return True
