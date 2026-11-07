from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProductSize = Literal["S", "M", "L", "XL", "XXL"]
ProductGender = Literal["Men", "Women", "Unisex", "Kids"]


class ProductCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)#extra = forbid for strict against unexpected input, and str strip whitespace is for clean up spaces from word.

    pName: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=500)

    mImage: str
    sImage: list[str] = Field(default_factory=list)

    price: float = Field(ge=0)
    color: str = Field(min_length=1)

    sizes: list[ProductSize] = Field(min_length=1)
    stock: int = Field(ge=0)

    category: str = Field(min_length=1)
    subCategory: str = ""

    gender: ProductGender | None = None
    isPublished: bool = True


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    pName: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=500)

    mImage: str | None = None
    sImage: list[str] | None = None

    price: float | None = Field(default=None, ge=0)
    color: str | None = Field(default=None, min_length=1)

    sizes: list[ProductSize] | None = Field(default=None, min_length=1)
    stock: int | None = Field(default=None, ge=0)

    category: str | None = Field(default=None, min_length=1)
    subCategory: str | None = None

    gender: ProductGender | None = None
    isPublished: bool | None = None


class ProductResponse(BaseModel):

    model_config = ConfigDict(extra="ignore")

    id: str

    pName: str
    description: str

    mImage: str
    sImage: list[str]

    price: float
    color: str
    sizes: list[ProductSize]
    stock: int

    category: str
    subCategory: str
    gender: ProductGender | None
    isPublished: bool

    createdAt: datetime
    updatedAt: datetime


class ProductListQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)

    min_price: float | None = Field(default=None, ge=0)
    max_price: float | None = Field(default=None, ge=0)

    sort_by: Literal["pName", "price", "stock"] = "pName"
    sort_order: Literal["asc", "desc"] = "asc"



class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int
    page: int
    limit: int
    total_pages: int
