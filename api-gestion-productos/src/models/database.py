"""SQLAlchemy models for database tables."""

from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRoleEnum(str, Enum):
    """User roles for authorization."""

    ADMIN = "admin"
    CLIENT = "client"


class ProductCategoryEnum(str, Enum):
    """Product categories for inventory."""

    FRUTAS = "frutas"
    VERDURAS = "verduras"
    LACTEOS = "lacteos"
    CARNES = "carnes"
    BEBIDAS = "bebidas"
    GRANOS = "granos"
    CONDIMENTOS = "condimentos"
    OTROS = "otros"


class User(Base):
    """User table model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    rol = Column(SQLEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.CLIENT)


class Product(Base):
    """Product table model (global, no owner)."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(SQLEnum(ProductCategoryEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
