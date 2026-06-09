from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app import models, schemas  

# --- OPERACIONES PARA CATEGORÍAS ---
def get_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# --- OPERACIONES PARA PRODUCTOS (GALLOS) ACTUALIZADAS ---
def get_products(db: Session):
    # Uso de joinedload para cargar relaciones de forma segura y evitar que la consulta falle
    # si faltan datos en alguna tabla relacionada.
    return db.query(models.Product).options(
        joinedload(models.Product.category), 
        joinedload(models.Product.supplier)
    ).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# --- OPERACIONES TRANSACCIONALES DE ÓRDENES (VENTAS) ---
def create_order(db: Session, order_data: schemas.OrderCreate):
    db_order = models.Order(
        customer_name=order_data.customer_name,
        ship_city=order_data.ship_city
    )
    db.add(db_order)
    db.flush() 

    for item in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail=f"El gallo con ID {item.product_id} no existe.")
        
        if product.units_in_stock < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para '{product.name}'. Disponibles en corrales: {product.units_in_stock}"
            )
        
        product.units_in_stock -= item.quantity
        
        db_detail = models.OrderDetail(
            order_id=db_order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.unit_price
        )
        db.add(db_detail)

    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session):
    return db.query(models.Order).all()

# --- MÉTODOS DE ACTUALIZACIÓN (UPDATE) ---

def update_category(db: Session, category_id: int, category_data: schemas.CategoryCreate):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db_category.name = category_data.name
        db_category.description = category_data.description
        db.commit()
        db.refresh(db_category)
    return db_category

def update_product(db: Session, product_id: int, product_data: schemas.ProductCreate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db_product.name = product_data.name
        db_product.description = product_data.description
        db_product.unit_price = product_data.unit_price
        db_product.units_in_stock = product_data.units_in_stock
        db_product.age_months = product_data.age_months
        db_product.category_id = product_data.category_id
        db.commit()
        db.refresh(db_product)
    return db_product


# --- MÉTODOS DE ELIMINACIÓN (DELETE) ---

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False

# --- CARGA MASIVA DE INVENTARIO (SEED) ---
def import_massive_inventory(db: Session, inventory_data: dict):
    for cat_data in inventory_data.get("categories", []):
        db_cat = db.query(models.Category).filter(models.Category.name == cat_data["name"]).first()
        if not db_cat:
            db_cat = models.Category(name=cat_data["name"], description=cat_data.get("description"))
            db.add(db_cat)
            db.flush() 
        
        for prod_data in cat_data.get("products", []):
            db_prod = db.query(models.Product).filter(models.Product.name == prod_data["name"]).first()
            if not db_prod:
                new_prod = models.Product(
                    name=prod_data["name"],
                    description=prod_data.get("description"),
                    unit_price=prod_data.get("unit_price", 0.0),
                    units_in_stock=prod_data.get("units_in_stock", 0),
                    age_months=prod_data.get("age_months"),
                    category_id=db_cat.id
                )
                db.add(new_prod)
                
    db.commit()
    return {"status": "success", "message": "¡Líneas y gallos cargados en MySQL exitosamente!"}

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()