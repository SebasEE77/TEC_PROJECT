"""Rutas de autenticación y gestión de usuarios."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from models.database import User
from utils.auth import get_current_user
from models.schemas import UserLogin
from models.db import get_db
from models.schemas import TokenResponse, UserRegister, UserResponse
from utils.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)) -> UserResponse:
    """Registra un nuevo usuario en el sistema.

    Valida que el email no esté registrado, hashea la contraseña y crea el usuario.
    Por defecto, los usuarios nuevos tienen rol CLIENT.

    Args:
        user_data: Datos del usuario a registrar (email, contraseña, nombre, rol)
        db: Sesión de base de datos

    Returns:
        Información del usuario creado sin la contraseña

    Raises:
        HTTPException: Si el email ya está registrado
    """
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Hashear contraseña y crear usuario
    hashed_password = hash_password(user_data.contraseña)

    new_user = User(
        nombre=user_data.nombre,
        email=user_data.email,
        password_hash=hashed_password,
        rol=user_data.rol
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponse.model_validate(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear usuario"
        )


@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """Autentica a un usuario y genera un token JWT.

    Valida email y contraseña, retorna token de acceso si son válidos.

    Args:
        user_data: Datos de inicio de sesión (email y contraseña)
        db: Sesión de base de datos

    Returns:
        Token JWT de acceso

    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    # Buscar usuario por email
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.contraseña, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token de acceso
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Obtiene la información del usuario actualmente autenticado.

    Args:
        current_user: Usuario obtenido del token JWT

    Returns:
        Datos del usuario actual
    """
    return UserResponse.model_validate(current_user)
