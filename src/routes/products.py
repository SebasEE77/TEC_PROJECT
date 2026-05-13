"""Rutas de productos para operaciones CRUD."""

from typing import List

from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from models.database import Product, User
from models.db import get_db
from models.schemas import ProductCreate, ProductResponse, ProductUpdate
from utils.auth import get_current_admin_user, get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> List[ProductResponse]:
    """Lista todos los productos (requiere autenticación).

    Todos los usuarios autenticados pueden ver los productos.
    Soporta paginación con parámetros skip y limit.

    Args:
        skip: Número de productos a saltar (paginación)
        limit: Número máximo de productos a retornar
        current_user: Usuario autenticado (requerido)
        db: Sesión de base de datos

    Returns:
        Lista de productos
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return [ProductResponse.model_validate(product) for product in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """Obtiene un producto específico por ID (requiere autenticación).

    Args:
        product_id: ID del producto a obtener
        current_user: Usuario autenticado (requerido)
        db: Sesión de base de datos

    Returns:
        Datos del producto

    Raises:
        HTTPException: Si el producto no se encuentra
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    return ProductResponse.model_validate(product)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """Crea un nuevo producto (requiere rol de administrador).

    Solo los usuarios administradores pueden crear productos.

    Args:
        product_data: Datos para crear el producto
        current_user: Usuario administrador (requerido)
        db: Sesión de base de datos

    Returns:
        Datos del producto creado
    """
    new_product = Product(**product_data.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return ProductResponse.model_validate(new_product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
) -> ProductResponse:
    """Actualiza un producto existente (requiere rol de administrador).

    Solo los usuarios administradores pueden actualizar productos.
    Solo se actualizan los campos proporcionados.

    Args:
        product_id: ID del producto a actualizar
        product_update: Campos a actualizar (opcionales)
        current_user: Usuario administrador (requerido)
        db: Sesión de base de datos

    Returns:
        Datos del producto actualizado

    Raises:
        HTTPException: Si el producto no se encuentra
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Actualizar solo los campos proporcionados
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return ProductResponse.model_validate(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Elimina un producto (requiere rol de administrador).

    Solo los usuarios administradores pueden eliminar productos.

    Args:
        product_id: ID del producto a eliminar
        current_user: Usuario administrador (requerido)
        db: Sesión de base de datos

    Raises:
        HTTPException: Si el producto no se encuentra
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    db.delete(product)
    db.commit()
