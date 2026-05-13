"""Utilidades de seguridad para hash de contraseñas y tokens JWT."""

import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from dotenv import load_dotenv
from jose import JWTError, jwt

from models.schemas import TokenResponse

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt.

    Genera un salt aleatorio y aplica el algoritmo bcrypt para crear
    un hash seguro de la contraseña.

    Args:
        password: Contraseña en texto plano a hashear

    Returns:
        Contraseña hasheada como string (incluye salt)
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash.

    Compara una contraseña en texto plano con su versión hasheada
    para determinar si coinciden.

    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Contraseña hasheada almacenada en BD

    Returns:
        True si la contraseña coincide, False en caso contrario
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT de acceso.

    Genera un token JWT con la información del usuario y tiempo de expiración.
    Incluye el campo 'sub' (subject) con el ID del usuario.

    Args:
        data: Diccionario con datos del usuario (debe incluir 'sub' para user ID)
        expires_delta: Tiempo de expiración personalizado (opcional)

    Returns:
        Token JWT como string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verifica y decodifica un token JWT.

    Valida la firma del token y extrae la información contenida.
    Si el token es inválido o expiró, retorna None.

    Args:
        token: Token JWT a verificar

    Returns:
        Datos decodificados del token si es válido, None si es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
