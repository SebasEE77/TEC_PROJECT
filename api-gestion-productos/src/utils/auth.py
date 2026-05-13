"""Utilidades de autenticación para validación de tokens JWT y dependencias de usuario."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from models.database import User
from models.db import get_db
from models.schemas import UserRoleEnum
from utils.security import verify_token

# Esquema de seguridad para tokens JWT Bearer
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtiene el usuario actual desde el token JWT.

    Extrae y valida el token JWT del header Authorization.
    Busca al usuario en la base de datos usando el ID del token.

    Args:
        credentials: Token JWT del header Authorization
        db: Sesión de base de datos

    Returns:
        Objeto User si el token es válido

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    """
    token = credentials.credentials
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtiene el usuario actual y verifica que tenga rol de administrador.

    Primero obtiene el usuario autenticado, luego verifica que su rol sea ADMIN.

    Args:
        current_user: Usuario de la dependencia get_current_user

    Returns:
        Objeto User si es administrador

    Raises:
        HTTPException: Si el usuario no tiene rol de admin
    """
    if current_user.rol != UserRoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para realizar esta acción",
        )
    return current_user
