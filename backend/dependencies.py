from fastapi import Depends
from sqlmodel import Session

from database import get_session
from repositories import IItemsRepository, ItemsRepository
from services import ItemsService


def get_items_repository(
    session: Session = Depends(get_session),
) -> IItemsRepository:
    """Dependency provider for the ItemsRepository."""
    return ItemsRepository(session=session)


def get_items_service(
    repo: IItemsRepository = Depends(get_items_repository),
) -> ItemsService:
    """Dependency provider for the ItemsService."""
    return ItemsService(items_repository=repo)
