from abc import ABC, abstractmethod

from sqlmodel import Session, select

from models import Item, ItemCreate, ItemUpdate


class IItemsRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Item]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Item | None:
        pass

    @abstractmethod
    def create(self, item: ItemCreate) -> Item:
        pass

    @abstractmethod
    def update(self, item: Item, changes: ItemUpdate) -> Item:
        pass

    @abstractmethod
    def delete(self, item: Item) -> None:
        pass


class ItemsRepository(IItemsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[Item]:
        return list(
            self.session.exec(select(Item).order_by(Item.created_at.desc()))
        )

    def get_by_id(self, id: int) -> Item | None:
        return self.session.get(Item, id)

    def create(self, item: ItemCreate) -> Item:
        db_item = Item.model_validate(item)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def update(self, item: Item, changes: ItemUpdate) -> Item:
        item.sqlmodel_update(changes.model_dump(exclude_unset=True))
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, item: Item) -> None:
        self.session.delete(item)
        self.session.commit()
