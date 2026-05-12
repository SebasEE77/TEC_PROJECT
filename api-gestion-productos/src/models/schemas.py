"""Pydantic schemas for request/response validation.

Este módulo define esquemas Pydantic para validar datos de entrada y salida.
- Esquemas de ENTRADA (Request): UserRegister, UserLogin, ProductCreate, ProductUpdate
- Esquemas de SALIDA (Response): UserResponse, ProductResponse
Esto asegura que nunca exponemos campos sensibles como password_hash.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRoleEnum(str, Enum):
    """Roles de usuario para el sistema de autorización."""

    ADMIN = "admin"
    CLIENT = "client"


class ProductCategoryEnum(str, Enum):
    """Categorías válidas para productos en el inventario."""

    FRUTAS = "frutas"
    VERDURAS = "verduras"
    LACTEOS = "lacteos"
    CARNES = "carnes"
    BEBIDAS = "bebidas"
    GRANOS = "granos"
    CONDIMENTOS = "condimentos"
    OTROS = "otros"


# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    """Base compartido para esquemas de usuario.
    
    Contiene campos comunes que se usan en esquemas de registro y respuesta.
    Configurado con extra="forbid" para rechazar campos no definidos.
    """

    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email único del usuario")

    model_config = ConfigDict(extra="forbid")


class UserRegister(UserBase):
    """Schema para REGISTRO de nuevo usuario.
    
    Usado cuando un usuario intenta registrarse.
    Incluye validación de contraseña:
    - Mínimo 8 caracteres
    - Debe tener al menos 1 letra, 1 número y 1 carácter especial
    """

    contraseña: str = Field(..., min_length=8, description="Contraseña del usuario (mín. 8 caracteres)")

    @field_validator("contraseña")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Valida que la contraseña cumpla con requisitos de seguridad.
        
        Requisitos:
        - Al menos una letra (mayúscula o minúscula)
        - Al menos un número (0-9)
        - Al menos un carácter especial (!@#$%^&*...)
        
        Raises:
            ValueError: si no cumple los requisitos
        """
        has_letter = any(char.isalpha() for char in value)
        has_number = any(char.isdigit() for char in value)
        has_special = any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?" for char in value)

        if not (has_letter and has_number and has_special):
            raise ValueError(
                "La contraseña debe contener al menos una letra, un número y un carácter especial"
            )
        return value


class UserLogin(BaseModel):
    """Schema para LOGIN de usuario.
    
    Usado cuando un usuario intenta iniciar sesión.
    Solo requiere email y contraseña (sin validación compleja).
    """

    email: EmailStr = Field(..., description="Email del usuario")
    contraseña: str = Field(..., description="Contraseña del usuario")

    model_config = ConfigDict(extra="forbid")


class UserResponse(UserBase):
    """Schema para RESPUESTA cuando se retorna datos de usuario.
    
    Usado en endpoints que devuelven información de usuario.
    NUNCA expone password_hash (campo sensible).
    Incluye id y rol para saber quién es el usuario y qué permisos tiene.
    """

    id: int = Field(..., description="ID del usuario")
    rol: UserRoleEnum = Field(..., description="Rol del usuario")

    model_config = ConfigDict(from_attributes=True)


# ==================== PRODUCT SCHEMAS ====================


class ProductBase(BaseModel):
    """Base compartido para esquemas de producto.
    
    Contiene campos comunes usados en creación, actualización y respuesta de productos.
    Validaciones incluidas:
    - cantidad: debe ser >= 0
    - precio: debe ser > 0
    - fecha_vencimiento: debe ser una fecha futura
    """

    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    categoria: ProductCategoryEnum = Field(..., description="Categoría del producto")
    cantidad: int = Field(..., ge=0, description="Cantidad en stock")
    precio: float = Field(..., gt=0, description="Precio del producto")
    fecha_vencimiento: datetime = Field(..., description="Fecha de vencimiento")

    model_config = ConfigDict(extra="forbid")

    @field_validator("fecha_vencimiento")
    @classmethod
    def validate_expiration_date(cls, value: datetime) -> datetime:
        """Valida que la fecha de vencimiento sea una fecha futura.
        
        Verifica que el producto no esté vencido al momento de crear/actualizar.
        
        Raises:
            ValueError: si la fecha es en el pasado o igual a la fecha actual
        """
        if value <= datetime.utcnow():
            raise ValueError("La fecha de vencimiento debe ser una fecha futura")
        return value


class ProductCreate(ProductBase):
    """Schema para CREAR un nuevo producto.
    
    Usado cuando un admin intenta crear un producto.
    Hereda todas las validaciones de ProductBase.
    """
    pass


class ProductUpdate(BaseModel):
    """Schema para ACTUALIZAR un producto existente.
    
    Todos los campos son opcionales (Optional).
    Permite actualizar solo los campos que el usuario desea cambiar.
    Si un campo no se envía, su valor es None (se ignora).
    """

    nombre: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del producto")
    categoria: Optional[ProductCategoryEnum] = Field(None, description="Categoría del producto")
    cantidad: Optional[int] = Field(None, ge=0, description="Cantidad en stock")
    precio: Optional[float] = Field(None, gt=0, description="Precio del producto")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento")

    model_config = ConfigDict(extra="forbid")

    @field_validator("fecha_vencimiento")
    @classmethod
    def validate_expiration_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Valida fecha de vencimiento solo si se proporciona un valor.
        
        Si value es None, no hace validación (el campo es opcional).
        Si value es una fecha, verifica que sea futura.
        """
        if value is not None and value <= datetime.utcnow():
            raise ValueError("La fecha de vencimiento debe ser una fecha futura")
        return value


class ProductResponse(ProductBase):
    """Schema para RESPUESTA cuando se retorna datos de producto.
    
    Usado en endpoints que devuelven información de producto.
    Incluye el id del producto para identificarlo.
    No expone campos internos no necesarios.
    """

    id: int = Field(..., description="ID del producto")

    model_config = ConfigDict(from_attributes=True)


# ==================== TOKEN SCHEMA ====================

class TokenResponse(BaseModel):
    """Schema para RESPUESTA de autenticación (token JWT).
    
    Usado cuando un usuario se registra o inicia sesión.
    Contiene el token JWT que el cliente debe enviar en requests posteriores.
    """
    access_token: str = Field(..., description="JWT token para autenticación")
    token_type: str = Field(default="bearer", description="Tipo de token (siempre 'bearer')")

