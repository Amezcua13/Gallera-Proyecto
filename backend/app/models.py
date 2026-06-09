from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)

    products = relationship("Product", back_populates="category")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Opcional: si quieres navegar desde el proveedor a sus productos
    products = relationship("Product", back_populates="supplier")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), index=True, nullable=False)
    description = Column(String(255), nullable=True)
    unit_price = Column(Float, default=0.0)         
    units_in_stock = Column(Integer, default=0)     
    age_months = Column(Integer, nullable=True)     
    image_url = Column(String(255), nullable=True)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True, default=1)
    
    # RELACIONES COMPLETAS
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)  
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    ship_city = Column(String(100), nullable=True)        

    details = relationship("OrderDetail", back_populates="order")

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)                
    unit_price = Column(Float, nullable=False)          

    order = relationship("Order", back_populates="details")
    product = relationship("Product")