from typing import Optional

from sqlmodel import Field, SQLModel


# Database table model
class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=255)
    price: float = Field(gt=0, description="Price must be greater than 0")
    is_offer: Optional[bool] = Field(default=False)


# Pydantic models for API requests/responses
class ItemBase(SQLModel):
    name: str = Field(max_length=255)
    price: float = Field(gt=0, description="Price must be greater than 0")
    is_offer: Optional[bool] = False


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=255)
    price: Optional[float] = Field(default=None, gt=0)
    is_offer: Optional[bool] = None


class ItemRead(ItemBase):
    id: int
