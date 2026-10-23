# Tickets

> Un ticket por archivo. Se crean recién después de aprobar G4 y solo si cumplen el Definition of Ready.

## Convención

- Nombre: `T01.md`, `T02.md`, …
- Formato: copia `docs/plantilla_ticket.md`.
- Estado: se registra en `docs/estado_proyecto.md`.
- Rama: `feature/T01-descripcion` o `fix/T01-descripcion`.
- Un ticket = una unidad verificable. No mezcles varias tareas.

## Definition of Ready

Antes de crear un ticket, verifica:

- [ ] Historia clara y acotada.
- [ ] Criterios de aceptación en formato Dado/Cuando/Entonces.
- [ ] Casos límite identificados.
- [ ] Datos y contratos definidos.
- [ ] Dependencias conocidas.
- [ ] Sin preguntas abiertas bloqueantes.
- [ ] Prioridad y estimación.

## Definition of Done

- [ ] Criterios de aceptación cumplidos.
- [ ] Convenciones respetadas.
- [ ] Límites `@limit` respetados.
- [ ] Pruebas pasadas.
- [ ] Documentación actualizada.
- [ ] Commit propuesto.

## Plantilla

Usa `docs/plantilla_ticket.md`. No inventes un formato nuevo.
