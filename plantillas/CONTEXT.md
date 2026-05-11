# CONTEXT.md — Plantilla de Contexto para IA

> **Instrucciones:** Llena este archivo con el contexto de tu proyecto. GitHub Copilot lo usará para generar código consistente con tu arquitectura. Referéncialo con `@workspace` o `#CONTEXT.md` en Copilot Chat.

---

## Nombre del Proyecto
<!-- Ej: Task Manager API, Climate Dashboard, CSV Processor -->

## Descripción
<!-- ¿Qué hace tu aplicación? ¿Qué problema resuelve? 2-3 líneas -->

## Público Objetivo
<!-- ¿Quién va a usar esto? -->

## Stack Tecnológico
<!-- Sé específico con versiones -->
- **Lenguaje:** <!-- Ej: Python 3.12 / Node.js 20 -->
- **Framework:** <!-- Ej: FastAPI 0.110 / Express 4.18 -->
- **Base de datos:** <!-- Ej: SQLite / PostgreSQL 16 -->
- **Librerías principales:** <!-- Lista las principales -->

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
<!-- Lista las features que debe tener -->
1. 
2. 
3. 

## Variables de Entorno
<!-- Lista las variables necesarias (SIN valores reales) -->
- `DATABASE_URL=` 
- `JWT_SECRET=`
- `PORT=`

## Decisiones de Diseño
<!-- ¿Por qué elegiste este stack? ¿Qué trade-offs consideraste? -->

---

*Completa este archivo ANTES de empezar a pedir código a Copilot.*
