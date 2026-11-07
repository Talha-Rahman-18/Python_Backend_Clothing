from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProductImage(BaseModel):
    url: str
    public_id: str | None = None


class ProductDocument(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    pName: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=500)

    mImage: str
    sImage: list[str] = Field(default_factory=list)

    price: float = Field(ge=0)
    color: str = Field(min_length=1)

    sizes: list[Literal["S", "M", "L", "XL", "XXL"]]
    stock: int = Field(ge=0)

    category: str = Field(min_length=1)
    subCategory: str = ""

    gender: Literal["Men", "Women", "Unisex", "Kids"] | None = None

    isPublished: bool = True

    createdAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updatedAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )