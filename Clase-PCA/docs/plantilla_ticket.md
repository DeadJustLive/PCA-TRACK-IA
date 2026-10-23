# Plantilla de Ticket

> **Instrucción para la IA:** Cada tarea se ejecuta desde un ticket. No programes sin un ticket asociado. Si falta información, detente y pregunta antes de avanzar.

> Copia este bloque por cada nueva tarea y guárdalo (por ejemplo en `docs/tickets/T01.md` o directamente en tu herramienta de tickets).

---

```markdown
# Ticket <ID> — <Título breve>

## Metadatos
- **Tipo:** feat | fix | refactor | docs | test | chore
- **Fase / Sprint:** F3 · Sprint 1
- **Rama sugerida:** feature/<ID>-<descripcion>
- **Prioridad:** alta | media | baja

## Contexto
<Qué se necesita y por qué. Enlaces al backlog o al sprint.>

## Convenciones aplicables
<Lista de IDs de `docs/convenciones.md` que rigen esta tarea.>
- CONV-NAM-01
- CONV-ERR-01

## Alcance (Qué SÍ / Qué NO)
- **SÍ:** <qué se debe hacer>
- **NO:** <qué queda fuera de esta tarea>

## Criterios de aceptación
- [ ] <resultado verificable 1>
- [ ] <resultado verificable 2>
- [ ] <resultado verificable 3>

## Archivos afectados (previstos)
| Archivo | @kind | @limit |
| :--- | :--- | :--- |
| `ruta/archivo` | component | 100 |

## Casos límite (Edge Cases)
- <qué pasa si el usuario hace algo inesperado>

## Definition of Done
- [ ] La tarea cumple todos los criterios de aceptación.
- [ ] Se respetan las convenciones listadas.
- [ ] Se respetan los `@limit` de los archivos tocados.
- [ ] Pruebas pasadas (ver F4 — Validación).
- [ ] `docs/estado_proyecto.md` actualizado.
- [ ] Si hubo un bug resuelto, está registrado en `docs/cicatrices_guerra.md`.
- [ ] Commit propuesto (la IA no commitea sola — ver `docs/git.md`).
```

---

## Ejemplo rellenado

```markdown
# Ticket T05 — Inicio de sesión con email

## Metadatos
- **Tipo:** feat
- **Fase / Sprint:** F3 · Sprint 1
- **Rama sugerida:** feature/T05-login-usuario
- **Prioridad:** alta

## Contexto
Necesitamos que el usuario pueda autenticarse con email y contraseña
para acceder a las funciones privadas definidas en el backlog.

## Convenciones aplicables
- CONV-NAM-01
- CONV-ERR-01
- CONV-SEG-01

## Alcance
- **SÍ:** formulario de login, validación de credenciales, sesión activa.
- **NO:** registro de nuevos usuarios (va en otro ticket).

## Criterios de aceptación
- [ ] Un usuario válido puede iniciar sesión.
- [ ] Credenciales incorrectas muestran un error claro.
- [ ] La sesión persiste al recargar la página.

## Casos límite (Edge Cases)
- Email con formato inválido.
- Usuario inexistente.
- Base de datos no disponible.

## Definition of Done
- [ ] Criterios de aceptación cumplidos.
- [ ] Convenciones respetadas.
- [ ] Pruebas pasadas.
- [ ] `docs/estado_proyecto.md` actualizado.
- [ ] Commit propuesto.
```
