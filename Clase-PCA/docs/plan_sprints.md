<!-- @pca:start
@id(docs.plan_sprints)
@kind(doc)
@relates(docs.estado_proyecto)
@relates(docs.backlog_requisitos)
@relates(docs.convenciones)
@relates(docs.reglas_backend)
@relates(docs.reglas_ui)
@desc(Plan maestro de sprints y tablero de tickets atómicos para el desarrollo del MVP)
@pca:end -->
# Plan de Sprints

> **Instrucción para la IA:** Este documento responde **en qué orden** se construye. No crees tickets ejecutables ni escribas código hasta que G4 esté aprobada. Cada ticket debe cumplir su Definition of Ready (DoR) y su Definition of Done (DoD).

> **Estado:** Borrador para G4. Los tickets T01–T23 son propuestas; todavía no existen como archivos en `docs/tickets/`.

---

## 1. Estrategia

1. **Primero fundaciones, luego pantallas.** Sin tokens, contratos ni errores, cada feature inventa su propio estilo y su propio manejo de fallos.
2. **Un vertical slice por sprint.** Cada sprint termina con algo que se puede probar de punta a punta.
3. **El pago es el corte más delicado.** No se empieza Flow hasta resolver OPEN-01 y probar el webhook en sandbox.
4. **Admin y web comparten UI, pero no lógica de dominio.** El admin no reutiliza hooks de compra.
5. **La DB hace conjuntos; la API compone.** Cada pantalla tiene una llamada principal.
6. **Nada se considera hecho sin tests y sin documentación actualizada.**

---

## 2. Resumen

| Sprint | Duración estimada | Objetivo | Entregable demostrable |
| :--- | :--- | :--- | :--- |
| **S0** | 1 semana | Fundaciones | Monorepo, tokens, UI base, errores y contratos |
| **S1** | 1 semana | Datos y auth | Supabase local, esquema, RLS, login y cliente API |
| **S2** | 1–2 semanas | Catálogo | Catálogo y detalle con datos reales |
| **S3** | 2 semanas | Compra | Carrito, checkout y pago Flow en sandbox |
| **S4** | 1–2 semanas | Cuenta | Pedidos, direcciones, wishlist y Mi Invernadero |
| **S5** | 2 semanas | Admin | Dashboard, productos, inventario y pedidos |
| **S6** | 1 semana | Contenido | Journal, newsletter y admin de contenido |
| **S7** | 1 semana | Hardening | E2E, accesibilidad, SEO y observabilidad |

> Las duraciones son orientativas para un equipo pequeño. Ajustar en G4.

---

## 3. Sprint 0 — Fundaciones

**Objetivo:** dejar el monorepo, el diseño y los contratos listos para que los sprints siguientes no reinicien decisiones.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T01 | Base del monorepo | chore | Alta | — |
| T02 | Tokens, Tailwind y Storybook | feat | Alta | T01 |
| T03 | Primitivas UI con CVA | feat | Alta | T02 |
| T04 | Infraestructura de errores y Problem Details | feat | Alta | T01 |

### T01 — Base del monorepo

**Alcance:** pnpm workspaces, Turborepo, apps `web`/`admin`, paquetes vacíos, TypeScript estricto, ESLint, Prettier, Vitest.
**No incluye:** pantallas, base de datos, Flow.
**Criterios:**
- [ ] `pnpm install`, `pnpm build`, `pnpm lint`, `pnpm test` funcionan desde la raíz.
- [ ] `web` y `admin` levantan en dev.
- [ ] No hay `any` ni imports cruzados no permitidos.
- [ ] `pnpm-workspace.yaml` y `turbo.json` documentados.

### T02 — Tokens, Tailwind y Storybook

**Alcance:** `packages/tokens`, configuración Tailwind, tipografías, colores semánticos, Storybook.
**No incluye:** componentes de dominio.
**Criterios:**
- [ ] Tokens canónicos definidos y documentados.
- [ ] `web` y `admin` consumen el mismo preset.
- [ ] Storybook levanta y muestra tokens.
- [ ] Contraste AA validado en pares texto/fondo.

### T03 — Primitivas UI con CVA

**Alcance:** Button, Input, Select, Card, Badge, Dialog, Table, Skeleton, EmptyState, ErrorState.
**No incluye:** lógica de carrito, auth o datos.
**Criterios:**
- [ ] Cada componente tiene variantes CVA y `className` merge.
- [ ] Estados hover, focus, disabled, loading y error.
- [ ] Accesibilidad por teclado y `aria`.
- [ ] Stories y tests de render.

### T04 — Infraestructura de errores

**Alcance:** `packages/errors`, `AppError`, catálogo de códigos, Problem Details, ErrorBoundary, mapeo SQLSTATE/Flow.
**No incluye:** mensajes finales de todas las pantallas.
**Criterios:**
- [ ] Un error de API se serializa como `application/problem+json`.
- [ ] El cliente distingue error de red, auth, validación y negocio.
- [ ] `traceId` aparece en logs y respuesta.
- [ ] Tests de mapeo.

---

## 4. Sprint 1 — Datos, RLS y Auth

**Objetivo:** tener una base de datos reproducible y un usuario autenticado con roles.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T05 | Supabase local y migraciones | chore | Alta | T01 |
| T06 | Esquema inicial y RLS | feat | Alta | T05, OPEN-02 |
| T07 | Auth y guards de ruta | feat | Alta | T06 |
| T08 | Contratos, OpenAPI y cliente tipado | feat | Alta | T01, T06 |

### T05 — Supabase local y migraciones

**Criterios:**
- [ ] `supabase start` levanta DB, Auth y Storage.
- [ ] Migraciones forward-only y seed reproducible.
- [ ] Scripts documentados en README.
- [ ] CI aplica migraciones en seco.

### T06 — Esquema inicial y RLS

**Alcance:** tablas de `docs/modelo_datos.md` para perfiles, catálogo, carrito, órdenes, pagos y contenido.
**Bloqueo:** OPEN-02 decide si `products.stock` es suficiente o se requiere una tabla de especímenes.
**Criterios:**
- [ ] Constraints, índices y FK según el modelo.
- [ ] RLS activa en todas las tablas.
- [ ] Tests de RLS por rol.
- [ ] Triggers de `updated_at` y `search_vector`.

### T07 — Auth y guards

**Criterios:**
- [ ] Registro, login, logout y recuperación.
- [ ] Google OAuth si G1 lo confirma; Apple según OPEN-04.
- [ ] Perfil sincronizado en `profiles`.
- [ ] Rutas privadas redirigen a login y conservan destino.
- [ ] Ruta admin verifica rol en servidor, no solo en UI.

### T08 — Contratos y cliente API

**Criterios:**
- [ ] Esquemas Zod para cada endpoint del BFF.
- [ ] Cliente tipado con manejo de errores.
- [ ] OpenAPI generado o validado en CI.
- [ ] MSW con fixtures para desarrollo sin backend.

---

## 5. Sprint 2 — Catálogo

**Objetivo:** que un visitante explore y vea producto con datos reales, una llamada por pantalla y buena performance.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T09 | API de catálogo con búsqueda y facetas | feat | Alta | T06, T08 |
| T10 | UI de catálogo y filtros | feat | Alta | T03, T09 |
| T11 | Detalle de producto y SEO | feat | Alta | T09 |

### T09 — API de catálogo

**Criterios:**
- [ ] `GET /v1/catalog` devuelve items, facetas y cursor.
- [ ] Búsqueda con `search_vector` y fallback.
- [ ] Máximo 2 round trips; sin llamadas externas.
- [ ] Caché CDN con invalidación por versión de catálogo.
- [ ] Tests de filtros combinados y página vacía.

### T10 — UI de catálogo

**Criterios:**
- [ ] Grid responsive, filtros en drawer móvil.
- [ ] Estados loading, empty, error y “cargar más”.
- [ ] Filtros reflejados en URL.
- [ ] Imágenes con `alt`, lazy loading y sizes.
- [ ] Accesibilidad de teclado.

### T11 — Detalle de producto

**Criterios:**
- [ ] Galería, precio, stock, cuidados y relacionados.
- [ ] Metadatos, canonical y JSON-LD de producto.
- [ ] 404 amable para slug inexistente/archivado.
- [ ] CTA de carrito deshabilitado si no hay stock.

---

## 6. Sprint 3 — Carrito, checkout y Flow

**Objetivo:** completar una compra real en sandbox y reflejar el estado confirmado por webhook.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T12 | Carrito y merge de invitado | feat | Alta | T10 |
| T13 | Checkout y orden transaccional | feat | Alta | T12, T06, OPEN-01 |
| T14 | Flow: pago, retorno y webhook | feat | Alta | T13, OPEN-01 |
| T15 | Confirmación y estado de pedido | feat | Alta | T14 |

### T12 — Carrito

**Criterios:**
- [ ] Carrito local para invitado; servidor para autenticado.
- [ ] Merge sin duplicados y validación de stock.
- [ ] Cambios de cantidad con debounce.
- [ ] Persistencia y recuperación tras recarga.
- [ ] Tests de merge y stock.

### T13 — Checkout

**Bloqueo:** OPEN-01 (moneda/Flow) y OPEN-05 (envío/impuestos).
**Criterios:**
- [ ] RPC atómica crea orden + items + reservas.
- [ ] Totales calculados en servidor.
- [ ] `Idempotency-Key` evita doble orden.
- [ ] Dirección validada y snapshot.
- [ ] Errores de stock y precio visibles.

### T14 — Flow

**Criterios:**
- [ ] Pago creado server-to-server; secretos fuera del bundle.
- [ ] Webhook valida firma, registra evento y es idempotente.
- [ ] Reintento/conciliación para eventos perdidos.
- [ ] No se confía en el query param de retorno.
- [ ] Tests con fixtures de Flow y firma inválida.

### T15 — Confirmación

**Criterios:**
- [ ] Página de pedido con timeline y estados.
- [ ] Polling corto solo si el pago está pendiente.
- [ ] Email de confirmación (OPEN-07).
- [ ] Estado consistente tras recargar.

---

## 7. Sprint 4 — Cuenta y Mi Invernadero

**Objetivo:** que el cliente gestione su cuenta y sus plantas.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T16 | Cuenta: pedidos y direcciones | feat | Alta | T07, T15 |
| T17 | Wishlist | feat | Media | T07 |
| T18 | Mi Invernadero y bitácora | feat | Media | T15, OPEN-02 |

### T16 — Cuenta

**Criterios:**
- [ ] Lista de pedidos paginada y detalle.
- [ ] CRUD de direcciones con default único.
- [ ] No se puede acceder a pedidos/direcciones de otro usuario.
- [ ] Estados vacíos y errores.

### T17 — Wishlist

**Criterios:**
- [ ] Agregar/quitar desde catálogo y detalle.
- [ ] Persistencia y lista en cuenta.
- [ ] Visitante redirigido a login.
- [ ] Sin duplicados.

### T18 — Mi Invernadero

**Criterios:**
- [ ] Plantas creadas desde pedidos pagados.
- [ ] Registro de cuidados con fecha y próximo recordatorio.
- [ ] Vista de pendientes.
- [ ] RLS: solo el dueño ve sus plantas.

---

## 8. Sprint 5 — Admin

**Objetivo:** operar la tienda sin tocar la base de datos.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T19 | Admin: shell y dashboard | feat | Alta | T03, T09 |
| T20 | Admin: productos, inventario y bulk | feat | Alta | T06, T08 |
| T21 | Admin: pedidos y envíos | feat | Alta | T14, T19 |

### T19 — Dashboard

**Criterios:**
- [ ] KPIs, ventas por categoría, stock bajo y pedidos recientes.
- [ ] Una llamada de composición y vista materializada.
- [ ] Rango de fechas y estados de carga.
- [ ] 403 si el rol no es admin.

### T20 — Productos e inventario

**Criterios:**
- [ ] CRUD de producto, imágenes y estado.
- [ ] Ajuste de stock con movimiento y auditoría.
- [ ] Acciones masivas (activar/archivar/categoría).
- [ ] Validación de slug único y precio.
- [ ] Invalidación de caché al publicar.

### T21 — Pedidos y envíos

**Criterios:**
- [ ] Lista filtrable y detalle con timeline.
- [ ] Transiciones válidas; 409 en inválidas.
- [ ] Registro de carrier/tracking.
- [ ] No se borran pagos; auditoría de cambios.
- [ ] Exportación como job si es grande.

---

## 9. Sprint 6 — Contenido

**Objetivo:** publicar journal y captar newsletter sin acoplar contenido al catálogo.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T22 | Journal y newsletter | feat | Media | T03, T06 |

### T22 — Journal y newsletter

**Criterios:**
- [ ] Lista y detalle de posts publicados.
- [ ] Filtros por tag y SEO.
- [ ] Admin crea/edita/publica.
- [ ] Newsletter con doble opt-in si G1 lo confirma.
- [ ] Rate limiting y estados de error.

> OPEN-03 decide si el formulario del vlog es IA real o FAQ/contacto. Si es IA, se abre un ticket separado y se reevalúa el sprint.

---

## 10. Sprint 7 — Hardening

**Objetivo:** cerrar calidad, seguridad y operación antes de producción.

| Ticket | Título | Tipo | Prioridad | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| T23 | Hardening y validación final | test | Alta | Todos |

**Criterios:**
- [ ] E2E del camino completo en staging.
- [ ] Tests de RLS y de webhook fallido.
- [ ] Lighthouse y presupuesto de performance.
- [ ] axe sin errores críticos.
- [ ] Backups y restauración probados.
- [ ] Runbook de incidentes y alertas.
- [ ] `docs/cicatrices_guerra.md` actualizado.

---

## 11. Dependencias

```text
T01 → T02 → T03
T01 → T04
T01 → T05 → T06 → T07
T06 → T08 → T09 → T10 → T11
T10 → T12 → T13 → T14 → T15
T07/T15 → T16
T07 → T17
T15 → T18
T03/T09 → T19
T06/T08 → T20
T14/T19 → T21
T03/T06 → T22
Todo → T23
```

**Bloqueos externos:**
- OPEN-01 bloquea T13 y T14.
- OPEN-02 bloquea T06, T18 y T20.
- OPEN-05 bloquea T13.
- OPEN-07 bloquea T15.
- OPEN-03 bloquea el alcance de T22.

---

## 12. Definition of Ready (DoR)

Un ticket puede empezar cuando:

- [ ] Tiene objetivo, alcance y fuera de alcance.
- [ ] Tiene criterios de aceptación verificables.
- [ ] Tiene edge cases identificados.
- [ ] Tiene contratos de API/datos definidos.
- [ ] Tiene convenciones aplicables listadas.
- [ ] Tiene dependencias resueltas o bloqueo explícito.
- [ ] Tiene archivos previstos y `@limit`.
- [ ] Tiene estrategia de prueba.

---

## 13. Definition of Done (DoD)

Un ticket termina cuando:

- [ ] Criterios de aceptación cumplidos.
- [ ] Tests unitarios/integración/E2E según corresponda.
- [ ] Typecheck y lint sin errores.
- [ ] Sin `any` ni secretos en el código.
- [ ] Accesibilidad y responsive revisados.
- [ ] Errores mapeados a Problem Details.
- [ ] Documentación y anotaciones actualizadas.
- [ ] `docs/estado_proyecto.md` actualizado.
- [ ] Commit propuesto según `docs/git.md`.
- [ ] Revisión de código aprobada.

---

## 14. Hitos

| Hito | Criterio |
| :--- | :--- |
| **M1 — Base lista** | S0 + S1; build, auth y DB local funcionando |
| **M2 — Catálogo** | S2; visitante navega con datos reales |
| **M3 — Compra** | S3; pago sandbox confirmado por webhook |
| **M4 — Operación** | S5; admin gestiona catálogo y pedidos |
| **M5 — Release** | S7; E2E, performance, backups y runbook |

---

## 15. Preguntas abiertas

| ID | Pregunta | Sprint afectado |
| :--- | :--- | :--- |
| **OPEN-01** | Moneda/país de Flow | S3 |
| **OPEN-02** | SKU vs espécimen | S1, S4, S5 |
| **OPEN-03** | IA real o FAQ | S6 |
| **OPEN-04** | Apple OAuth | S1 |
| **OPEN-05** | Envío/impuestos | S3 |
| **OPEN-06** | Paleta canónica | S0 |
| **OPEN-07** | Email transaccional | S3 |
| **OPEN-08** | Roles admin | S1, S5 |
| **OPEN-09** | Tailwind v3.4 vs v4 | S0 |

---

## 16. Historial de cambios

| Fecha | Cambio |
| :--- | :--- |
| 2026-10-22 | Borrador inicial de sprints, tickets, dependencias y DoR/DoD. |
