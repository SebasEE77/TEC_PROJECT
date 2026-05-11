# REGLAS.md — Reglas de Arquitectura y Seguridad

> **Instrucciones:** Define las reglas INEGOCIABLES de tu proyecto. Copilot debe seguirlas siempre. Si hay conflicto entre un prompt y estas reglas, **las reglas ganan**.

---

## Arquitectura
<!-- Define tu patrón arquitectónico -->
- Patrón: <!-- MVC / Hexagonal / Capas / etc. -->
- Separación de responsabilidades: cada archivo tiene UN solo propósito
- Nombres descriptivos: si necesitas un comentario para explicar qué hace una función, está mal nombrada

## Seguridad (OWASP)
- NUNCA hardcodear credenciales, API keys o secretos en el código
- TODOS los inputs del usuario deben ser validados antes de procesarse
- NUNCA exponer stack traces o detalles internos en respuestas de error
- Usar parameterized queries (NUNCA concatenar strings para SQL)
- Contraseñas: siempre hasheadas con bcrypt o equivalente

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

## Testing
- Mínimo tests para los endpoints/functions principales
- Usar el framework de testing del stack elegido

## Git
- Commits atómicos y con mensajes descriptivos
- `.env` SIEMPRE en `.gitignore`
- `node_modules/`, `__pycache__/`, `.venv/` en `.gitignore`

---

## Tu regla personalizada
<!-- Agrega al menos 1 regla que sea específica de TU proyecto -->


---

*Referencia este archivo en Copilot Chat: "Lee REGLAS.md antes de generar código. Las reglas tienen prioridad sobre mis prompts."*
