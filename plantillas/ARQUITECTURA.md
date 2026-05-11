# ARQUITECTURA.md — Documento de Arquitectura

> **Instrucciones:** Describe la arquitectura de tu solución. Este documento ayuda tanto a tu equipo como a Copilot a entender cómo se conectan las piezas.

---

## Diagrama de Arquitectura

```
<!-- Dibuja un diagrama textual de tu solución -->
 Ejemplo API REST:

 [Cliente/Frontend]
        │
        ▼
   [API Gateway / Router]
        │
   ┌────┼────┐
   ▼    ▼    ▼
[Auth] [CRUD] [Export]
   │    │    │
   └────┼────┘
        ▼
   [Base de Datos]
```

## Capas del Sistema

### Capa de Presentación / Rutas
<!-- ¿Cómo entran los datos? Endpoints, CLI commands, etc. -->

### Capa de Lógica / Servicios
<!-- ¿Qué procesamiento se hace? Reglas de negocio -->

### Capa de Datos / Modelos
<!-- ¿Cómo se almacena? Modelos, esquemas -->

### Capa de Utilidades
<!-- Funciones helper, middleware, etc. -->

## Flujo Principal
<!-- Describe paso a paso el flujo principal de tu aplicación -->
1. 
2. 
3. 

## Decisiones Técnicas
| Decisión | Justificación |
|----------|---------------|
| <!-- Ej: SQLite vs PostgreSQL --> | <!-- ¿Por qué? --> |
| <!-- Ej: JWT vs Sessions --> | <!-- ¿Por qué? --> |

## Dependencias
| Librería | Versión | Para qué |
|----------|---------|----------|
| | | |

---

*Mantén este documento actualizado conforme evoluciona tu proyecto.*
