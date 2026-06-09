from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- ESQUEMAS CATEGORÍAS ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS PRODUCTOS (GALLOS) ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    unit_price: float
    units_in_stock: int
    age_months: Optional[int] = None
    category_id: int
    image_url: Optional[str] = None  # <-- NUEVO CAMPO OPCIONAL

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS ÓRDENES (VENTAS) ---
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    ship_city: Optional[str] = None
    items: List[OrderItemCreate]  

class OrderDetailResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    order_date: datetime
    ship_city: Optional[str] = None
    details: List[OrderDetailResponse]
    class Config:
        from_attributes = True