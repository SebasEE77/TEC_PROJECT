# Food Inventory API - Guía de Instalación y Ejecución

Este documento proporciona instrucciones detalladas para instalar, configurar y ejecutar la API REST de Gestión de Inventario de Productos.

## Requisitos del Sistema

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- Python 3.10 o superior
- Docker Desktop o Docker Compose
- pip (gestor de paquetes de Python)

## Paso 1: Clonar el Proyecto

Clona el proyecto en tu máquina local:

```
https://github.com/SebasEE77/TEC_PROJECT.git
```

## Paso 2: Crear un entorno virtual e instala las dependencias

Abre una terminal y navega a la carpeta de la API. Crea un entorno virtual local para no instalar dependencias globalmente en tu sistema:

```
python -m venv .venv
```

Activa el entorno virtual:

```
.\.venv\Scripts\Activate
```

Luego actualiza pip e instala las dependencias:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Este comando instalará todos los paquetes necesarios incluyendo:
- FastAPI: Framework web
- SQLAlchemy: ORM para base de datos
- Pydantic: Validación de datos
- psycopg2: Conector de PostgreSQL
- bcrypt: Hash de contraseñas
- python-jose: Tokens JWT

## Paso 3: Iniciar PostgreSQL con Docker Compose

El proyecto incluye un `docker-compose.yml` en la raíz que crea un contenedor PostgreSQL listo para usarse.

Desde la raíz del proyecto ejecuta:

```
docker compose up -d
```

Esto levantará un servicio PostgreSQL con los siguientes valores por defecto:

- Usuario: `user`
- Contraseña: `user`
- Base de datos: `products_db`
- Puerto local: `5433`

Verifica que el servicio esté corriendo con:

```
docker compose ps
```

## Paso 4: Configurar Variables de Entorno

En la carpeta `api-gestion-productos`, abre el archivo `.env` (si no existe, cópialo de `.env.example`). Edita el archivo y actualiza los siguientes valores según tu configuración:

```
DATABASE_URL=postgresql://user:user@localhost:5433/products_db
JWT_SECRET=tu-clave-secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Si cambias los valores de `docker compose`, ajusta también la URL de conexión en este archivo.

Ejemplo completo:

```env
DATABASE_URL=postgresql://user:user@localhost:5433/products_db
JWT_SECRET=aR3@llyC0mpl3xS3cr3tK3y!2024Pr0j3ct
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Guarda el archivo.

## Paso 5: Ejecutar la API

Asegúrate de haber iniciado primero el servicio de PostgreSQL con Docker Compose y de estar dentro de la carpeta src. Ejecuta la aplicación con:

```
python main.py
```

Deberías ver un mensaje similar a:

```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

La API estará disponible en:

- Interfaz de Swagger: http://localhost:8000/docs

## Paso 6: Poblar con Datos de Ejemplo (Opcional)

Para crear usuarios y productos de prueba, ejecuta:

```
python populate_db.py
```

Se crearán:
- Usuario administrador: admin@example.com / Admin123!
- Usuario cliente: client@example.com / Client123!
- 5 productos de ejemplo

## Paso 7: Probar la API

Puedes probar los endpoints:

1. Abre http://localhost:8000/docs en tu navegador
2. Haz clic en cualquier endpoint para expandirlo
3. Haz clic en "Try it out" para probar
4. Completa los datos y haz clic en "Execute"

## Estructura del Proyecto

```
.
├── api-gestion-productos/
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── database.py
│   │   │   ├── schemas.py
│   │   │   └── db.py
│   │   ├── routes/
│   │   │   ├── users.py
│   │   │   └── products.py
│   │   └── utils/
│   │       ├── security.py
│   │       └── auth.py
│   ├── populate_db.py
│   ├── requirements.txt
│   ├── .env
│   ├── .env.example
│   └── .gitignore
├── docker-compose.yml
├── README.md
├── ARQUITECTURA.md
├── CONTEXT.md
├── REGLAS.md
└── .gitignore
```

## Descripción de Funcionalidades

### Autenticación y Usuarios

- POST /users/register: Registrar nuevo usuario
- POST /users/login: Iniciar sesión y obtener token JWT
- GET /users/me: Obtener información del usuario actual

### Gestión de Productos

- GET /products/: Listar todos los productos (requiere autenticación)
- GET /products/{id}: Obtener un producto específico
- POST /products/: Crear nuevo producto (solo admin)
- PUT /products/{id}: Actualizar producto (solo admin)
- DELETE /products/{id}: Eliminar producto (solo admin)

## Detener la API

Para detener la API, presiona `Ctrl + C` en la terminal donde se ejecuta.
