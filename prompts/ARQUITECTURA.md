# ARQUITECTURA.md — Documento de Arquitectura

> **Instrucciones:** Describe la arquitectura de tu solución. Este documento ayuda tanto a tu equipo como a Copilot a entender cómo se conectan las piezas.

---

## Diagrama de Arquitectura

```
 [Cliente / Swagger UI]
         │
         ▼
    [FastAPI App]
         │
    ┌────┴────┐
    ▼         ▼
 [Auth]    [CRUD]
    │         │
    └────┬────┘
         ▼
   [PostgreSQL]
```

## Capas del Sistema

### Capa de Presentación / Rutas
Los datos entran por endpoints REST definidos en `routes/`. Hay dos routers:
- `users.py` → registro (`POST /users/register`), login (`POST /users/login`) y perfil (`GET /users/me`)
- `products.py` → CRUD completo sobre `/products` (listar, obtener, crear, actualizar, eliminar)

La validación de entrada la hace Pydantic automáticamente a través de los esquemas definidos en `schemas.py`.

### Capa de Lógica / Servicios
La lógica de negocio vive directamente en las rutas (no hay carpeta `services/` separada). Incluye:
- Verificación de email duplicado al registrar
- Hasheo de contraseñas con bcrypt
- Generación y validación de tokens JWT
- Control de acceso por rol: `admin` puede todo, `client` solo lectura

### Capa de Datos / Modelos
- `database.py` → modelos ORM (SQLAlchemy): tablas `users` y `products` con sus enums (`UserRoleEnum`, `ProductCategoryEnum`)
- `schemas.py` → esquemas Pydantic separados para entrada (`UserRegister`, `ProductCreate`, etc.) y salida (`UserResponse`, `ProductResponse`), para nunca exponer campos sensibles como `password_hash`
- `db.py` → conexión a PostgreSQL (engine único, `SessionLocal`, dependency `get_db()`, y `create_tables()` al iniciar)

### Capa de Utilidades
- `security.py` → funciones de hashing (`bcrypt`) y JWT (`python-jose`): crear token, verificar token, hashear y comparar contraseñas
- `auth.py` → dependencias de FastAPI para inyectar el usuario autenticado (`get_current_user`) y verificar rol admin (`get_current_admin_user`)

## Flujo Principal
1. El cliente envía un request HTTP con body JSON (y token JWT en el header si requiere autenticación)
2. FastAPI valida los datos de entrada con Pydantic y resuelve las dependencias (autenticación, sesión de BD)
3. La ruta ejecuta la lógica de negocio: consulta o modifica la BD a través de SQLAlchemy ORM
4. Se retorna una respuesta JSON validada con el esquema de salida correspondiente

## Decisiones Técnicas
| Decisión | Justificación |
|----------|---------------|
| PostgreSQL | Robusto, soporta enums nativos y es estándar en producción. Se levanta con Docker Compose. |
| JWT (stateless) | Autenticación sin estado en el servidor, ideal para APIs REST escalables. |
| FastAPI | Validación automática con Pydantic, docs interactivas (Swagger) incluidas, tipado estricto. |
| bcrypt | Hashing seguro de contraseñas con salt automático y resistencia a fuerza bruta. |
| SQLAlchemy ORM | Evita SQL raw (previene inyecciones), facilita mantenimiento del código. |
| Esquemas entrada/salida separados | Nunca se expone `password_hash` ni campos internos en las respuestas. |

## Dependencias
| Librería | Versión | Para qué |
|----------|---------|----------|
| `fastapi` | 0.115.0 | Framework web REST |
| `uvicorn` | 0.30.0 | Servidor ASGI |
| `sqlalchemy` | 2.0.23 | ORM para PostgreSQL |
| `psycopg2-binary` | 2.9.9 | Driver de PostgreSQL |
| `pydantic[email]` | 2.5.0 | Validación de datos y emails |
| `bcrypt` | 4.1.2 | Hashing de contraseñas |
| `python-jose` | 3.3.0 | Tokens JWT |
| `python-dotenv` | 1.0.0 | Variables de entorno desde `.env` |
| `pytest` | 7.4.3 | Testing |
| `httpx` | 0.25.2 | Cliente HTTP para tests |

---

*Mantén este documento actualizado conforme evoluciona tu proyecto.*
