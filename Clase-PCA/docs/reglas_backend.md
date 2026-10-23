<!-- @pca:start
@id(docs.reglas_backend)
@kind(doc)
@relates(docs.convenciones)
@relates(docs.modelo_datos)
@relates(docs.arquitectura)
@desc(Reglas de base de datos, API BFF, Flow, errores, caché y performance)
@pca:end -->
# Reglas de Backend y Base de Datos

> **Instrucción para la IA:** Este documento responde **cómo se consulta, escribe y protege** el backend. Si una regla entra en conflicto con una idea de implementación, gana este documento. Si falta un caso, detente y pregunta.

> **Alcance:** API BFF, Edge Functions, Postgres, RLS, RPC, Storage, Flow y jobs. Las reglas visuales están en `docs/reglas_ui.md`.

---

## 1. Principios

1. **El navegador no toca la base de datos.** Solo llama al BFF.
2. **La DB hace lo que sabe hacer:** filtrar, ordenar, agregar, validar integridad y ejecutar transacciones atómicas.
3. **La API orquesta:** autentica, autoriza, valida, compone, integra Flow y mapea errores.
4. **El cliente presenta y cachea:** no calcula totales, stock ni permisos.
5. **Una pantalla, una llamada.** Evitar N+1 y llamadas en cascada.
6. **Cero llamadas externas en lecturas.** Flow solo aparece en checkout/webhook/conciliación.
7. **Todo lo que escribe es idempotente o transaccional.**
8. **Los secretos viven en el servidor.** Nunca en `VITE_*`.

---

## 2. Matriz de responsabilidades

| Necesidad | Dónde se resuelve | Por qué |
| :--- | :--- | :--- |
| Filtrar catálogo, facetas, orden, paginación | Postgres/RPC | Una consulta, índice y conjunto |
| Búsqueda full-text | Postgres `tsvector` | Evita servicio externo y llamadas |
| Total de orden, reserva y descuento de stock | RPC transaccional | Atomicidad y concurrencia |
| Permisos por fila | RLS | Seguridad cerca del dato |
| Dashboard agregado | Vista materializada + RPC | Evita N consultas y cálculo repetido |
| Composición de pantalla | API BFF | Una respuesta para el cliente |
| Auth y sesión | Supabase Auth | Estándar y seguro |
| Firma de Flow | Edge `flow-webhook` | Secreto y validación HMAC |
| Expirar reservas | `pg_cron` | No depende de un usuario conectado |
| Imágenes | Storage + CDN | Peso y distribución |
| Email transaccional | Proveedor/Supabase | Fuera de la request crítica |

---

## 3. Presupuesto de llamadas

| Operación | Cliente → BFF | BFF → DB | BFF → externo |
| :--- | :--- | :--- | :--- |
| Landing | 1 | 1 RPC | 0 |
| Catálogo | 1 | 1 RPC | 0 |
| Detalle | 1 | 1 RPC | 0 |
| Cuenta | 1 | 1 RPC | 0 |
| Checkout | 1 | 1 RPC + 1 update | 1 Flow |
| Confirmación | 1 | 1 RPC | 0 |
| Admin dashboard | 1 | 1 RPC/vista | 0 |

**Reglas duras:**
- Máximo **2 round trips** a DB por request de lectura.
- Máximo **1 llamada externa** por request de checkout.
- Prohibido resolver listas con `for` + query por ítem.
- Prohibido llamar a Flow desde GET.
- Prohibido que el cliente haga fan-out a varios endpoints para pintar una pantalla.

---

## 4. Base de datos

### 4.1 Nomenclatura

| Elemento | Convención | Ejemplo |
| :--- | :--- | :--- |
| Tablas | plural, `snake_case` | `order_items` |
| Columnas | `snake_case` | `created_at` |
| PK | `id` | `id uuid` |
| FK | `<entidad>_id` | `order_id` |
| Booleanos | prefijo `is_`/`has_` | `is_active` |
| Timestamps | `*_at` | `paid_at` |
| Dinero | `*_cents` | `total_cents` |
| Enums | singular, `snake_case` | `order_status` |
| Índices | `idx_<tabla>_<columnas>` | `idx_orders_user_created` |
| Funciones | verbo + entidad | `create_order`, `confirm_payment` |

### 4.2 Tipos y constraints

- PK `uuid` con `gen_random_uuid()`.
- `timestamptz` para fechas; `date` solo para fechas sin hora.
- `numeric` solo si se justifica; dinero en `integer` de centavos.
- `citext` para email.
- Enums para estados finitos; `text + check` si el enum cambia mucho.
- `not null` por defecto; nullable solo con motivo.
- `check` para `stock >= 0`, `quantity > 0`, `price_cents >= 0`.
- FK con índice y `on delete` explícito.
- Unique para slug, email, provider IDs e idempotencia.

### 4.3 Migraciones

- Una migración por cambio lógico; nombre `YYYYMMDDHHMMSS_descripcion.sql`.
- Forward-only: no se edita una migración aplicada.
- Cambios destructivos en dos pasos: agregar → migrar datos → eliminar.
- Toda migración se prueba en local y staging.
- CI aplica migraciones en seco y falla si hay drift.
- Backup antes de producción.

### 4.4 RLS

- RLS **activa** en todas las tablas del esquema público.
- Políticas por operación (`select`, `insert`, `update`, `delete`), no una genérica.
- `auth.uid()` para dueño; `exists` con `user_roles` para admin.
- `service_role` solo en Edge/jobs; nunca en el cliente.
- Tests de RLS por rol y por recurso.
- Las vistas exponen solo columnas necesarias; `security_invoker` cuando aplique.

### 4.5 Consultas

- Seleccionar columnas explícitas; nunca `select *` en producción.
- Paginación por cursor (`created_at`, `id`), no `offset` alto.
- Índices para filtros y orden; revisar `explain analyze`.
- Evitar funciones en `where` que rompan índices.
- Usar `exists` en lugar de `count` para “hay más”.
- Para agregados de admin, vista materializada + refresh por job.
- Para búsqueda, `websearch_to_tsquery` + índice GIN; fallback `ILIKE` solo en datasets pequeños.
- Las RPC reciben parámetros tipados y devuelven JSON estable.

### 4.6 Transacciones

- Checkout: crear orden + items + reservas + pago en una sola transacción.
- Confirmación: actualizar pago + orden + stock + reserva en una sola transacción.
- Si falla cualquier paso, rollback completo.
- No hacer llamadas HTTP dentro de una transacción.
- Usar `select ... for update` solo donde haya contención real de stock.

### 4.7 Borrado y retención

- Catálogo: `archived_at`, no `delete`.
- Órdenes, pagos y auditoría: no se borran.
- Datos personales: anonimizar por solicitud, conservando integridad referencial.
- Webhooks: retención corta y `payload` minimizado.
- Jobs de limpieza documentados.

---

## 5. API BFF

### 5.1 Estructura

- Una Edge Function `api` con router modular (`/v1/...`).
- Una Edge Function `flow-webhook` separada:
  - JWT verification **desactivado**.
  - Firma HMAC **obligatoria**.
  - Idempotencia y respuesta rápida.
- `flow-webhook` no comparte middleware de usuario.
- `api` valida JWT de Supabase y roles.
- CORS restringido a los dominios de `web` y `admin`.

### 5.2 Contratos

- Cada endpoint tiene schema Zod de entrada y salida en `packages/contracts`.
- El contrato se versiona (`/v1`).
- Respuestas estables; no exponer filas crudas de DB.
- Errores con `application/problem+json`.
- OpenAPI generado o validado en CI.
- Cambios incompatibles requieren nueva versión.

### 5.3 Validación

- Validar body, query, params y headers.
- Normalizar email, slugs y strings.
- Rechazar campos desconocidos en escrituras.
- Límites de tamaño y cantidad (ej. 20 ítems de carrito).
- Sanitizar contenido del journal si acepta HTML.
- No confiar en el cliente para precios, stock, roles ni totales.

### 5.4 Autenticación y autorización

- `Authorization: Bearer <jwt>` en rutas privadas.
- El BFF verifica JWT y obtiene `sub`.
- El rol se consulta en `user_roles`; no se confía en un claim editable.
- Admin: 403 si no tiene rol.
- Recurso ajeno: 404 o 403 según no filtrar existencia.
- Rate limit por IP/usuario en auth, newsletter, checkout y webhook.

### 5.5 Idempotencia

- `POST /checkout/sessions` requiere `Idempotency-Key`.
- Guardar hash del request + respuesta.
- Si la key se repite con el mismo hash, devolver la misma respuesta.
- Si el hash cambia, 409.
- Expiración de keys: 24 h.
- El webhook usa `(provider, event_id)` como clave natural.

### 5.6 Paginación

- Cursor opaco (base64 de `created_at|id`).
- `limit` por defecto 20, máximo 50.
- Respuesta: `items`, `nextCursor`, `hasMore`.
- No usar `offset` para listas grandes.
- Admin puede usar páginas si el volumen es bajo, pero el contrato debe ser explícito.

### 5.7 Caché

| Capa | Qué se cachea | Invalidación |
| :--- | :--- | :--- |
| CDN | Landing, catálogo, imágenes, journal | Por tag/versión al publicar |
| TanStack Query | Respuestas de API | `queryKey` + invalidación por mutación |
| Postgres | Vistas materializadas | Job programado |
| Edge | Respuestas públicas cortas | `Cache-Control`/`s-maxage` |

**Reglas:**
- No cachear datos privados en CDN.
- No cachear checkout, pagos ni admin.
- `stale-while-revalidate` para catálogo.
- Invalidar catálogo al cambiar producto, precio, stock o estado.
- El cliente no inventa caché para permisos.

---

## 6. Manejo de errores

### 6.1 Taxonomía

| Tipo | HTTP | Cuándo |
| :--- | :--- | :--- |
| `VALIDATION` | 400 | Input inválido |
| `UNAUTHENTICATED` | 401 | Sin token o token inválido |
| `FORBIDDEN` | 403 | Sin permiso |
| `NOT_FOUND` | 404 | Recurso inexistente |
| `CONFLICT` | 409 | Estado incompatible, stock, duplicado |
| `RATE_LIMITED` | 429 | Demasiadas solicitudes |
| `UPSTREAM` | 502 | Flow u otro proveedor falla |
| `INTERNAL` | 500 | Error inesperado |

### 6.2 Formato

```json
{
  "type": "https://api.enchanted-botanicals.com/problems/out-of-stock",
  "title": "Stock insuficiente",
  "status": 409,
  "detail": "La planta Monstera Variegata ya no tiene unidades disponibles.",
  "code": "OUT_OF_STOCK",
  "traceId": "01J...",
  "errors": [
    { "field": "items[0].quantity", "message": "Solicitaste 2, quedan 0." }
  ]
}
```

**Reglas:**
- `AppError` en `packages/errors` con `code`, `status`, `detail`, `cause`.
- Mapear SQLSTATE (`23505`, `23503`, `23514`, `P0001`) a códigos de dominio.
- Mapear Flow a `PAYMENT_REJECTED`, `PAYMENT_PENDING`, `FLOW_UNAVAILABLE`.
- No filtrar stack traces, SQL ni secretos.
- Loguear con `traceId`, ruta, usuario (ID, no email), código y latencia.
- El cliente muestra `detail` si es seguro; si no, un mensaje genérico + `traceId`.

### 6.3 Reintentos

- Reintentar solo errores transitorios (`UPSTREAM`, timeout, 5xx).
- Backoff exponencial con jitter; máximo 3.
- No reintentar validación, permisos ni conflictos.
- Los webhooks se reintentan desde Flow; el endpoint debe ser idempotente.
- Los emails fallidos van a cola con reintento.

---

## 7. Flow server-to-server

### 7.1 Flujo

1. El cliente confirma checkout.
2. La API crea la orden y reserva stock.
3. La API crea el pago en Flow con `apiKey` y `secretKey`.
4. Flow devuelve `url` y `token`/ID.
5. La API guarda `payments.pending`.
6. El cliente redirige a Flow.
7. Flow llama al webhook.
8. La API valida firma, deduplica y confirma pago.
9. La orden pasa a `paid` y se consume stock.
10. La UI consulta el estado real.

### 7.2 Reglas

- Secretos solo en Edge.
- Nunca confiar en el retorno del navegador.
- Validar firma HMAC del webhook.
- Responder 2xx rápido; procesar lo pesado después si hace falta.
- Guardar `provider_order_id` y `provider_payment_id`.
- Comparar monto y moneda; si no coinciden, no confirmar.
- Estados desconocidos → `pending` + alerta, no `paid`.
- Conciliación programada para pagos pendientes.
- Reembolsos manuales con auditoría.

### 7.3 Idempotencia

- `webhook_events` unique `(provider, event_id)`.
- Si el evento ya fue procesado, responder 200 sin repetir efectos.
- Si llega fuera de orden, aplicar la transición solo si es válida.
- Un pago `paid` no vuelve a `pending`.
- Tests con evento duplicado, inválido, tardío y monto incorrecto.

---

## 8. Rendimiento y jobs

### 8.1 Presupuestos

| Métrica | Objetivo |
| :--- | :--- |
| p95 API lectura | < 300 ms |
| p95 DB | < 100 ms |
| p95 checkout sin Flow | < 800 ms |
| Payload de lista | < 100 KB |
| Consultas por request | ≤ 2 |
| Llamadas externas en lectura | 0 |

### 8.2 Jobs

| Job | Frecuencia | Acción |
| :--- | :--- | :--- |
| Expirar reservas | Cada 1–5 min | Liberar stock y cancelar órdenes vencidas |
| Refrescar dashboard | Cada 5–15 min | `refresh materialized view` |
| Conciliar pagos | Cada 15 min | Consultar Flow pendientes |
| Reintentar emails | Cada 5 min | Cola con backoff |
| Limpiar idempotencia | Diario | Borrar keys expiradas |
| Limpiar webhooks | Diario/semanal | Retención definida |

**Reglas:**
- Jobs idempotentes.
- Lock para evitar ejecuciones concurrentes.
- Logs con duración y filas afectadas.
- Alertas si un job falla repetidamente.

---

## 9. Seguridad

- RLS en todas las tablas.
- `service_role` solo servidor.
- Secretos en variables de entorno; nunca en git.
- CORS restringido.
- Rate limiting.
- Validación de tamaño y tipo de archivos.
- Buckets privados por defecto; público solo para catálogo/journal.
- URLs firmadas para subidas.
- No loggear PII ni tokens.
- Dependencias auditadas.
- Cabeceras de seguridad en el hosting.
- Protección CSRF no aplica a bearer tokens, pero sí a cookies si se usan.
- Revisar `security definer` en funciones; preferir `security invoker` salvo RPC controladas.

---

## 10. Testing

| Nivel | Qué se prueba |
| :--- | :--- |
| Unitario | Reglas de dominio, cálculo de totales, mapeos |
| Integración | RPC, constraints, transacciones |
| RLS | Cada rol y cada tabla |
| Contrato | Zod/OpenAPI |
| E2E | Compra completa y admin |
| Webhook | Firma, duplicado, fuera de orden, monto |
| Performance | p95, payload, consultas |
| Carga | Checkout concurrente y stock |

**Regla:** un bug de producción se convierte en test de regresión.

---

## 11. Anti-patrones prohibidos

| Anti-patrón | Por qué |
| :--- | :--- |
| Cliente directo a PostgREST con `service_role` | Expone todo |
| `select *` en endpoints públicos | Datos de más y payload grande |
| N+1 en listas | Satura DB y API |
| Llamar Flow en GET o en render | Efectos secundarios y latencia |
| Confiar en el total del cliente | Fraude y errores |
| Confirmar pago por query param | Fraude |
| Guardar tarjetas | PCI y riesgo |
| `any` en TypeScript | Pierde contratos |
| Migraciones editadas | Drift |
| RLS desactivada “temporalmente” | Brecha |
| Webhook sin firma | Suplantación |
| Reintentar sin idempotencia | Duplicados |
| Cachear datos privados en CDN | Fuga de datos |
| Borrar órdenes/pagos | Pérdida de historial |

---

## 12. Checklist de PR backend

- [ ] ¿El navegador sigue sin acceso directo a DB?
- [ ] ¿Hay una sola llamada de pantalla y ≤2 round trips?
- [ ] ¿La escritura es transaccional o idempotente?
- [ ] ¿Los permisos se validan en servidor?
- [ ] ¿RLS está activa y probada?
- [ ] ¿Los errores usan Problem Details?
- [ ] ¿No se filtran secretos ni PII?
- [ ] ¿Flow solo se llama server-to-server?
- [ ] ¿El webhook valida firma y deduplica?
- [ ] ¿Hay tests del camino feliz y de un edge case?
- [ ] ¿La caché se invalida correctamente?
- [ ] ¿La migración es forward-only?

---

## 13. Decisiones abiertas

| ID | Pregunta | Impacto |
| :--- | :--- | :--- |
| **OPEN-01** | País/moneda de Flow | Contratos, totales, impuestos |
| **OPEN-02** | SKU vs espécimen | Stock, RPC, admin |
| **OPEN-05** | Envío/impuestos | Cálculo del total |
| **OPEN-07** | Email transaccional | Cola y confirmaciones |
| **OPEN-08** | Roles admin | RLS y autorización |

---

## 14. Historial de cambios

| Fecha | Cambio |
| :--- | :--- |
| 2026-10-22 | Borrador inicial de reglas de DB, API, Flow, errores y performance. |
