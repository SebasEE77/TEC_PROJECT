# REGLAS.md — Reglas de Arquitectura y Seguridad

> **Instrucciones:** Define las reglas INEGOCIABLES de tu proyecto. Copilot debe seguirlas siempre. Si hay conflicto entre un prompt y estas reglas, **las reglas ganan**.

---

## Arquitectura
- Patrón: Capas (Routes → Services → Models)
- Separación de responsabilidades: cada archivo tiene UN solo propósito
  - `routes/` → solo definición de endpoints y validación de entrada
  - `models/` → solo definición de esquemas Pydantic y estructuras de datos
  - `utils/` → solo funciones auxiliares reutilizables (hashing, JWT, etc.)
  - La lógica de negocio y acceso a PostgreSQL va en una capa de servicios (`services/`)
- Nombres descriptivos: si necesitas un comentario para explicar qué hace una función, está mal nombrada
- Los endpoints siguen convenciones REST: sustantivos en plural, sin verbos en la URL
  - Permitido: `GET /products`, `POST /products`, `DELETE /products/{id}`
  - Prohibido: `GET /getProducts`, `POST /createProduct`

## Seguridad (OWASP)
- NUNCA hardcodear credenciales, API keys o secretos en el código
- TODOS los inputs del usuario deben ser validados antes de procesarse
- NUNCA exponer stack traces o detalles internos en respuestas de error
- Usar parameterized queries (NUNCA concatenar strings para SQL)
- Contraseñas: siempre hasheadas con bcrypt
- **JWT:** los tokens deben incluir `exp` (expiración), `sub` (user ID) y generarse con el `JWT_SECRET` del entorno
- **Autorización:** validar autenticación y permisos según el rol o alcance permitido para cada endpoint; un 401 es para no autenticado y un 403 para no autorizado
- Los endpoints de productos SIEMPRE requieren token JWT válido; no existe acceso anónimo a datos del inventario

## FastAPI
- Usar status_code explícito en cada endpoint (201 para creación, 204 para eliminación sin cuerpo, etc.)
- Separar esquemas de entrada (ProductCreate, UserLogin) de los de respuesta (ProductResponse) para no exponer campos internos como password_hash

## PostgreSQL
- El cliente de PostgreSQL se instancia una sola vez y se reutiliza (no crear una instancia por request)
- NUNCA exponer la PostgreSQL_URL en respuestas ni logs
- Los errores de PostgreSQL deben capturarse y convertirse en HTTPException con mensajes amigables antes de llegar al cliente

## Clean Code
- Funciones: máximo 20 líneas. Si es más, dividirla.
- Una función hace UNA sola cosa
- Nombres de variables en inglés, descriptivos (no `x`, `data`, `result`)
- Eliminar código comentado (git ya guarda el historial)
- No repetir lógica (DRY)

## Manejo de Errores
- try/catch en TODAS las operaciones que pueden fallar (BD, API, archivos)
- Errores con mensajes claros para el usuario (no técnicos)
- Log del error completo para debugging
- NUNCA ignorar un catch vacío
- Mapa de errores estándar del proyecto:
  | Situación | Código HTTP |
  |---|---|
  | Input inválido / campo faltante | 400 |
  | Token ausente o inválido | 401 |
  | Recurso de otro usuario | 403 |
  | Producto / usuario no encontrado | 404 |
  | Error interno / PostgreSQL caído | 500 |

## Validaciones de negocio
### Producto
- `nombre`: obligatorio, string no vacío, máximo 100 caracteres
- `categoría`: obligatorio, debe pertenecer a un conjunto de valores permitidos (enum)
- `cantidad`: obligatorio, entero ≥ 0
- `precio`: obligatorio, float > 0
- `fecha_vencimiento`: obligatorio, debe ser una fecha futura al momento del registro

### Usuario
- `nombre`: obligatorio, string no vacío, máximo 100 caracteres
- `email`: validado con el tipo `EmailStr` de Pydantic; único por usuario en la BD
- `contraseña`: obligatorio, string no vacío, mínimo 8 caracteres; obligatorio que contenga al menos un número, una letra y un caracter especial.
- NUNCA aceptar campos extra en el body de un request (`model_config = ConfigDict(extra='forbid')`)

## Testing
- Mínimo un test por endpoint principal (registro, login, CRUD de productos)
- Usar `pytest` con `httpx.AsyncClient` para llamadas a la API
- Cubrir los casos de error más críticos: token inválido, producto de otro usuario, campos faltantes

## Git
- Commits atómicos y con mensajes descriptivos
- `.env` SIEMPRE en `.gitignore`
- `node_modules/`, `__pycache__/`, `.venv/` en `.gitignore`

---

## Reglas específicas del proyecto
- **Acceso a datos:** todos los usuarios autenticados pueden ver los productos. Solo los usuarios con rol `admin` pueden crear, actualizar o eliminar productos.
- **Unicidad de email:** al registrar un usuario, verificar antes de insertar que el email no exista; devolver 400 con mensaje claro si ya está registrado
- **Expiración de tokens:** respetar `ACCESS_TOKEN_EXPIRE_MINUTES` del entorno; no hardcodear tiempos de expiración en el código
- **Respuestas consistentes:** toda respuesta de error sigue la misma estructura `{"detail": "<mensaje legible>"}` para facilitar el manejo en el cliente
- **Roles de usuario:** existen dos roles, `admin` y `client`. El rol `admin` puede realizar todas las operaciones sobre los productos (crear, leer, actualizar y eliminar). 
  El rol `client` solo puede realizar operaciones de lectura. Cualquier intento de un `client` de crear, actualizar o eliminar un producto debe retornar 403.


---
