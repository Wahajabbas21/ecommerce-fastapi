from pydantic import BaseModel

class InventoryResponse(BaseModel):
    id: int
    name: str
    sku: str | None = "N/A"
    stock: int = 0
    price: float

    class Config:
        from_attributes = True