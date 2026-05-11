# CONTEXT.md — Plantilla de Contexto para IA

> **Instrucciones:** Llena este archivo con el contexto de tu proyecto. GitHub Copilot lo usará para generar código consistente con tu arquitectura. Referéncialo con `@workspace` o `#CONTEXT.md` en Copilot Chat.

---

## Nombre del Proyecto
Food Inventory API

## Descripción
API REST para la gestión de productos comestibles, permitiendo registrar, consultar, actualizar y eliminar ítems de un inventario de alimentos. Resuelve la necesidad de llevar un control sobre productos con atributos como nombre, categoría, cantidad, fecha de vencimiento y precio.

## Público Objetivo
Desarrolladores que necesiten integrar funcionalidades de gestión de inventario 
de productos en sus aplicaciones.

## Stack Tecnológico
- **Lenguaje:** Python 3.12
- **Framework:** FastAPI 0.115
- **Base de datos:** Supabase
- **Librerías principales:**
    - fastapi
    - uvicorn
    - supabase

## Estructura del Proyecto
```
<!-- Muestra tu estructura de carpetas aquí -->
mi-proyecto/
├── src/
│   ├── routes/
│   ├── models/
│   └── utils/
├── tests/
├── .env.example
├── CONTEXT.md
├── REGLAS.md
└── README.md
```

## Funcionalidades Principales
1. Registro de usuarios con validación de email y hash de contraseña
2. Inicio de sesión que retorna un token JWT
3. Listar todos los productos del usuario autenticado
4. Crear un nuevo producto con validación de campos (nombre, categoría, cantidad, precio, fecha de vencimiento)
5. Actualizar un producto existente, solo si es del usuario autenticado
6. Eliminar un producto, solo si es del usuario autenticado
7. Manejo centralizado de errores con respuestas consistentes (400, 401, 403, 404, 500)

## Variables de Entorno
- SUPABASE_URL=
- SUPABASE_KEY=
- JWT_SECRET=
- JWT_ALGORITHM=
- ACCESS_TOKEN_EXPIRE_MINUTES=

## Decisiones de Diseño
Se eligió FastAPI porque permite documentar y probar los endpoints directamente desde 
el navegador sin una configuración adicional, además valida automáticamente los datos que llegan 
a la API y su código es limpio y fácil de entender, lo que lo hace una buena opción 
para usar en este tipo de proyectos.

Posteriormente, se eligió Supabase porque al ser una base de datos en la nube no requiere instalación 
ni configuración local, lo que hace más sencillo el proceso de desarrollo y despliegue. 
Además, al estar basada en PostgreSQL, ofrece todas las ventajas de una base de datos 
relacional sin la complejidad de administrarla manualmente.

---
