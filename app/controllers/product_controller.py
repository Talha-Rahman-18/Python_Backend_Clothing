from datetime import datetime, timezone
import math

from app.db import db
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductListQuery,
    ProductListResponse
)


async def create_product_controller(
    product: ProductCreate,
) -> ProductResponse:

    product_data = product.model_dump()

    now = datetime.now(timezone.utc)

    product_data["createdAt"] = now
    product_data["updatedAt"] = now

    result = await db.products.insert_one(product_data)

    product_data["id"] = str(result.inserted_id)

    return ProductResponse(**product_data)

# get all products

async def get_all_products_controller(
    query: ProductListQuery,
) -> ProductListResponse:
    # 1. Build the MongoDB filter
    filters = {}

    if query.min_price is not None or query.max_price is not None:
        filters["price"] = {}

        if query.min_price is not None:
            filters["price"]["$gte"] = query.min_price

        if query.max_price is not None:
            filters["price"]["$lte"] = query.max_price

    # 2. Calculate pagination
    skip = (query.page - 1) * query.limit

    # 3. Fetch products and count matching documents
    total = await db.products.count_documents(filters)

    cursor = (
        db.products.find(filters)
        .sort(query.sort_by, 1 if query.sort_order == "asc" else -1)
        .skip(skip)
        .limit(query.limit)
    )

    documents = await cursor.to_list(length=query.limit)

    # 4. Convert MongoDB documents to API response objects
    products = []

    for document in documents:
        document["id"] = str(document.pop("_id"))
        products.append(ProductResponse(**document))

    # 5. Calculate total pages
    total_pages = math.ceil(total / query.limit)

    return ProductListResponse(
        products=products,
        total=total,
        page=query.page,
        limit=query.limit,
        total_pages=total_pages,
    )



