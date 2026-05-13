"""SQLAlchemy models for database tables.

Este módulo define las clases de modelo que representan las tablas en PostgreSQL.
Usa SQLAlchemy ORM para mapear objetos Python a registros de base de datos.
"""

from enum import Enum

from sqlalchemy import Column, Date, Enum as SQLEnum, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

# Base: clase base para todos los modelos SQLAlchemy
Base = declarative_base()


class UserRoleEnum(str, Enum):
    """Enumeración de roles de usuario para autorización.
    
    Define dos roles posibles:
    - ADMIN: puede crear, leer, actualizar y eliminar productos
    - CLIENT: solo puede leer productos
    """
    
    ADMIN = "admin"
    CLIENT = "client"


class ProductCategoryEnum(str, Enum):
    """Enumeración de categorías de productos.
    
    Limita los valores permitidos en la columna 'categoria' de la tabla products.
    Asegura que solo se usen categorías válidas.
    """

    FRUTAS = "frutas"
    VERDURAS = "verduras"
    LACTEOS = "lacteos"
    CARNES = "carnes"
    BEBIDAS = "bebidas"
    GRANOS = "granos"
    CONDIMENTOS = "condimentos"
    OTROS = "otros"


class User(Base):
    """Tabla 'users' en PostgreSQL.
    
    Almacena información de usuarios registrados en el sistema.
    Campos:
    - id: identificador único (primary key)
    - nombre: nombre completo del usuario (máx 100 caracteres)
    - email: dirección de correo única y validada
    - password_hash: contraseña hasheada con bcrypt (nunca la contraseña en texto plano)
    - rol: rol del usuario (admin o client, por defecto client)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    rol = Column(SQLEnum(UserRoleEnum), nullable=False, default=UserRoleEnum.CLIENT)


class Product(Base):
    """Tabla 'products' en PostgreSQL.
    
    Almacena información de productos en el inventario.
    Los productos son globales (no pertenecen a un usuario específico).
    Solo los admin pueden crear, actualizar o eliminar.
    
    Campos:
    - id: identificador único (primary key)
    - nombre: nombre del producto (máx 100 caracteres)
    - categoria: categoría (enum con valores predefinidos)
    - cantidad: cantidad disponible en stock (entero no negativo)
    - precio: precio del producto (debe ser > 0)
    - fecha_vencimiento: fecha en la que vence el producto (debe ser futura)
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(SQLEnum(ProductCategoryEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
