from fastapi import APIRouter, status ,Depends

from app.controllers.product_controller import (
    create_product_controller,
    get_all_products_controller
)
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductListQuery,
    ProductListResponse
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product: ProductCreate):
    return await create_product_controller(product)

# Get all products
@router.get(
    "/",
    response_model=ProductListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_products(query: ProductListQuery = Depends()):
    return await get_all_products_controller(query)