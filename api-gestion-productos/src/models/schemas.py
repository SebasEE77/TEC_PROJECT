"""Pydantic schemas for request/response validation."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRoleEnum(str, Enum):
    """User roles."""

    ADMIN = "admin"
    CLIENT = "client"


class ProductCategoryEnum(str, Enum):
    """Product categories."""

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
    """Base user schema."""

    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email único del usuario")

    model_config = ConfigDict(extra="forbid")


class UserRegister(UserBase):
    """Schema for user registration."""

    contraseña: str = Field(..., min_length=8, description="Contraseña del usuario (mín. 8 caracteres)")

    @field_validator("contraseña")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Validate password complexity: at least 1 letter, 1 number, 1 special character."""
        has_letter = any(char.isalpha() for char in value)
        has_number = any(char.isdigit() for char in value)
        has_special = any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?" for char in value)

        if not (has_letter and has_number and has_special):
            raise ValueError(
                "La contraseña debe contener al menos una letra, un número y un carácter especial"
            )
        return value


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="Email del usuario")
    contraseña: str = Field(..., description="Contraseña del usuario")

    model_config = ConfigDict(extra="forbid")


class UserResponse(UserBase):
    """Schema for user response (no password exposed)."""

    id: int = Field(..., description="ID del usuario")
    rol: UserRoleEnum = Field(..., description="Rol del usuario")

    model_config = ConfigDict(from_attributes=True)


# ==================== PRODUCT SCHEMAS ====================


class ProductBase(BaseModel):
    """Base product schema."""

    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    categoria: ProductCategoryEnum = Field(..., description="Categoría del producto")
    cantidad: int = Field(..., ge=0, description="Cantidad en stock")
    precio: float = Field(..., gt=0, description="Precio del producto")
    fecha_vencimiento: datetime = Field(..., description="Fecha de vencimiento")

    model_config = ConfigDict(extra="forbid")

    @field_validator("fecha_vencimiento")
    @classmethod
    def validate_expiration_date(cls, value: datetime) -> datetime:
        """Validate that expiration date is in the future."""
        if value <= datetime.utcnow():
            raise ValueError("La fecha de vencimiento debe ser una fecha futura")
        return value


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)."""

    nombre: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del producto")
    categoria: Optional[ProductCategoryEnum] = Field(None, description="Categoría del producto")
    cantidad: Optional[int] = Field(None, ge=0, description="Cantidad en stock")
    precio: Optional[float] = Field(None, gt=0, description="Precio del producto")
    fecha_vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento")

    model_config = ConfigDict(extra="forbid")

    @field_validator("fecha_vencimiento")
    @classmethod
    def validate_expiration_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Validate that expiration date is in the future."""
        if value is not None and value <= datetime.utcnow():
            raise ValueError("La fecha de vencimiento debe ser una fecha futura")
        return value


class ProductResponse(ProductBase):
    """Schema for product response."""

    id: int = Field(..., description="ID del producto")

    model_config = ConfigDict(from_attributes=True)

# ==================== TOKEN SCHEMA ====================

class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str = Field(..., description="JWT token")
    token_type: str = Field(default="bearer", description="Tipo de token")

