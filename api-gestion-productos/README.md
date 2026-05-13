# Food Inventory API - Guía de Instalación y Ejecución

Este documento proporciona instrucciones detalladas para instalar, configurar y ejecutar la API REST de Gestión de Inventario de Productos.

## Requisitos del Sistema

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:

- Python 3.10 o superior
- PostgreSQL 12 o superior
- pgAdmin 4 (para gestión de la base de datos)
- pip (gestor de paquetes de Python)

## Paso 1: Clonar el Proyecto

Clona el proyecto en tu máquina local:

```
https://github.com/SebasEE77/TEC_PROJECT.git

```

## Paso 2: Instalar Dependencias de Python

Abre una terminal (PowerShell o CMD) y navega a la carpeta del proyecto. Luego, instala las dependencias requeridas:

```
python -m pip install -r requirements.txt

```

Este comando instalará todos los paquetes necesarios incluyendo:
- FastAPI: Framework web
- SQLAlchemy: ORM para base de datos
- Pydantic: Validación de datos
- psycopg2: Conector de PostgreSQL
- bcrypt: Hash de contraseñas
- python-jose: Tokens JWT

## Paso 3: Configurar PostgreSQL en pgAdmin

### 3.1 Acceder a pgAdmin

Crear una Nueva Base de Datos en pgAdmin:

1. En el panel izquierdo, expande "Servers" y selecciona tu servidor PostgreSQL
2. Haz clic derecho en "Databases" y selecciona "Create" -> "Database"
3. En el campo "Database" escribe: `food_inventory`
4. Haz clic en "Save"

### 3.2 Obtener la Cadena de Conexión

Necesitarás los siguientes datos de tu servidor PostgreSQL:

- Nombre de usuario: (ej. postgres)
- Contraseña: (tu contraseña de PostgreSQL)
- Host: localhost (por defecto)
- Puerto: 5432 (por defecto)
- Nombre de la BD: food_inventory

Si estos valores son diferentes, adáptalos según tu configuración.

## Paso 4: Configurar Variables de Entorno

En la carpeta del proyecto, abre el archivo `.env` (si no existe, cópialo de `.env.example`):

```
.env
```

Edita el archivo y actualiza los siguientes valores según tu configuración:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432 food_inventory
JWT_SECRET=tu-clave-secreta
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Reemplaza:
- `usuario`: nombre de usuario de PostgreSQL (ej. postgres)
- `contraseña`: contraseña de PostgreSQL
- `localhost`: dirección del servidor (localhost si está local)
- `5432`: puerto de PostgreSQL (Dejalo así)
- `food_inventory`: nombre de la base de datos

Ejemplo completo:

```env
DATABASE_URL=postgresql://postgres:mi_contraseña@localhost:5432/food_inventory
JWT_SECRET=aR3@llyC0mpl3xS3cr3tK3y!2024Pr0j3ct
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Guarda el archivo.

## Paso 5: Ejecutar la API

Ejecuta la aplicación con:

```powershell
python run.py
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

```powershell
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
api-gestion-productos/
├── src/
│   ├── main.py                 # Aplicación FastAPI principal
│   ├── models/
│   │   ├── database.py         # Definición de tablas (SQLAlchemy)
│   │   ├── schemas.py          # Esquemas de validación (Pydantic)
│   │   └── db.py               # Conexión a PostgreSQL
│   ├── routes/
│   │   ├── users.py            # Endpoints de usuarios
│   │   └── products.py         # Endpoints de productos
│   └── utils/
│       ├── security.py         # Funciones de seguridad (hashing, JWT)
│       └── auth.py             # Autenticación y autorización
├── run.py                      # Script para ejecutar la API
├── populate_db.py              # Script para datos de ejemplo
├── requirements.txt            # Dependencias de Python
├── .env                        # Variables de entorno (no commitear)
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Archivos a ignorar en Git
└── README.md                   # Este archivo
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
