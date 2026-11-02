from fastapi import APIRouter, Depends, HTTPException, Path

from dependencies import get_items_service
from models import ItemCreate, ItemPublic, ItemUpdate
from services import ItemsService

router = APIRouter()


@router.get("/items", tags=["items"], response_model=list[ItemPublic])
def get_items(service: ItemsService = Depends(get_items_service)):
    return service.get_items()


@router.get("/items/{id}", tags=["items"], response_model=ItemPublic)
def get_item(
    id: int = Path(..., description="Item ID"),
    service: ItemsService = Depends(get_items_service),
):
    item = service.get_item_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post(
    "/items", tags=["items"], response_model=ItemPublic, status_code=201
)
def create_item(
    item: ItemCreate,
    service: ItemsService = Depends(get_items_service),
):
    return service.create_item(item)


@router.patch("/items/{id}", tags=["items"], response_model=ItemPublic)
def update_item(
    changes: ItemUpdate,
    id: int = Path(..., description="Item ID"),
    service: ItemsService = Depends(get_items_service),
):
    item = service.update_item(id, changes)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/items/{id}", tags=["items"], status_code=204)
def delete_item(
    id: int = Path(..., description="Item ID"),
    service: ItemsService = Depends(get_items_service),
):
    if not service.delete_item(id):
        raise HTTPException(status_code=404, detail="Item not found")
