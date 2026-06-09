from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.staticfiles import StaticFiles  # Importante para servir imágenes
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gallera Amezcua", 
    description="Sistema de Ventas e Inventario de Aves de Combate - Modelo Northwind de 5 Tablas",
    version="1.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CREACIÓN Y CONFIGURACIÓN DE CARPETA ESTÁTICA PARA IMÁGENES ---
UPLOAD_DIR = os.path.join("static", "images")
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Crea las carpetas static/images si no existen

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido al Sistema de Ventas de la Gallera Northwind"}


# --- ENDPOINTS CATEGORÍAS (LÍNEAS) ---
@app.get("/categories", response_model=List[schemas.CategoryResponse], tags=["Categorías"])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/categories", response_model=schemas.CategoryResponse, tags=["Categorías"])
def crear_categoria(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.put("/categories/{category_id}", response_model=schemas.CategoryResponse, tags=["Categorías"])
def editar_categoria(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.update_category(db, category_id, category)
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_category

@app.delete("/categories/{category_id}", tags=["Categorías"])
def eliminar_categoria(category_id: int, db: Session = Depends(get_db)):
    if not crud.delete_category(db, category_id):
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": f"La categoría con ID {category_id} fue eliminada correctamente"}


# --- ENDPOINTS PRODUCTOS (GALLOS) ---
@app.get("/products", response_model=List[schemas.ProductResponse], tags=["Productos (Gallos)"])
def listar_productos(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.post("/products", response_model=schemas.ProductResponse, tags=["Productos (Gallos)"])
def crear_producto(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.ProductResponse, tags=["Productos (Gallos)"])
def editar_producto(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id, product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Gallo no encontrado")
    return db_product

@app.delete("/products/{product_id}", tags=["Productos (Gallos)"])
def eliminar_gallo(product_id: int, db: Session = Depends(get_db)):
    if not crud.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Gallo no encontrado")
    return {"mensaje": f"El gallo con ID {product_id} fue eliminado correctamente"}


# --- ENDPOINT: SUBIR FOTO DEL EJEMPLAR ---
@app.post("/products/{product_id}/upload-image", tags=["Productos (Gallos)"])
def subir_foto_gallo(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Gallo no encontrado")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo cargado debe ser una imagen")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"gallo_{product_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_product.image_url = f"/static/images/{unique_filename}"
    db.commit()
    db.refresh(db_product)

    return {"mensaje": "Foto del ejemplar guardada con éxito", "image_url": db_product.image_url}


# --- ENDPOINTS ÓRDENES (VENTAS) ---
@app.get("/orders", response_model=List[schemas.OrderResponse], tags=["Órdenes (Ventas)"])
def listar_ordenes(db: Session = Depends(get_db)):
    return crud.get_orders(db)

@app.post("/orders", response_model=schemas.OrderResponse, tags=["Órdenes (Ventas)"])
def generar_venta(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


# --- ENDPOINTS PROVEEDORES (5TA TABLA EXIGIDA) ---
@app.get("/suppliers", tags=["Proveedores (Criaderos)"])
def listar_proveedores(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


# --- CARGA MASIVA DE INVENTARIO CON PRE-POBLADO DE 5 TABLAS (SEED) ---
@app.post("/seed-inventory", tags=["Utilidades / Inicialización"])
def cargar_inventario_masivo(data: dict, db: Session = Depends(get_db)):
    # A) Validar e inyectar la 5ta Tabla si está vacía (Suppliers)
    if not db.query(models.Supplier).first():
        prov1 = models.Supplier(name="Criadero Los Azules", contact_name="Don Chon", phone="3511234567")
        prov2 = models.Supplier(name="Rancho El Retinto", contact_name="Ing. Amezcua", phone="3517654321")
        db.add_all([prov1, prov2])
        db.flush()    

    # B) Validar e inyectar Categorías base si está vacía
    if not db.query(models.Category).first():
        cat1 = models.Category(name="Hatch", description="Línea de combate tradicional")
        cat2 = models.Category(name="Kelso", description="Aves de gran inteligencia y corte")
        cat3 = models.Category(name="Warhorse", description="Línea agresiva y de poder")
        db.add_all([cat1, cat2, cat3])
        db.flush()

    # C) Ejecutar la rutina masiva para los productos amarrados a las llaves foráneas
    return crud.import_massive_inventory(db, data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)