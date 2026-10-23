<!-- @pca:start
@id(docs.estado_proyecto)
@kind(doc)
@relates(docs.convenciones)
@relates(docs.backlog_requisitos)
@relates(docs.modelo_datos)
@relates(docs.arquitectura)
@relates(docs.plan_sprints)
@desc(Tablero de control y memoria del proyecto Anti-Amnesia)
@pca:end -->
# Estado del Proyecto (Anti-Amnesia)

> **Instrucción para la IA:** Lee este archivo al iniciar **cada** sesión, antes de proponer cualquier cambio. Al cerrar la sesión, actualízalo. Este documento es la memoria del proyecto: si no está actualizado, el alumno pierde el contexto y aparece la **amnesia de contexto**.

**Última actualización:** 2026-10-22

---

## 1. Fase actual del flujo

| Campo | Valor |
| :--- | :--- |
| **Fase actual** | F1 — Levantamiento (con borrador de F2) |
| **Siguiente fase** | Aprobación de G1–G4 |
| **Estado** | Documentación F0–F2 redactada; puertas pendientes de revisión |
| **Modo de análisis** | Completo |

> Fases: F0 Setup → F1 Levantamiento → F2 Sprints → F3 Ejecución → F4 Validación → F5 Cierre. Ver `AGENTS.md`.

---

## 2. Puertas de análisis

| Puerta | Qué se aprueba | Estado | Fecha |
| :--- | :--- | :--- | :--- |
| **G1** | Problema, usuarios, MVP y fuera de alcance | Pendiente de aprobación | — |
| **G2** | Requisitos, RNF, edge cases y criterios | Pendiente de aprobación | — |
| **G3** | Modelo de datos, arquitectura y riesgos | Pendiente de aprobación | — |
| **G4** | Plan de sprints, tickets y DoR | Pendiente de aprobación | — |
| **G5** | Implementación | Bloqueada | — |

> **Regla de oro:** sin G1–G4 aprobadas no se escribe código. G5 solo se abre con la frase `AUTORIZO IMPLEMENTACIÓN`.

---

## 3. Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| **Frontend** | React + Vite + TypeScript estricto |
| **UI** | Tailwind CSS + CVA + `tailwind-merge` + Radix UI + Storybook |
| **Monorepo** | pnpm workspaces + Turborepo |
| **Backend / BFF** | Supabase Edge Functions (Deno) + Hono; PostgREST + RPC |
| **Base de Datos** | PostgreSQL en Supabase + RLS |
| **Autenticación** | Supabase Auth (email/contraseña + Google) |
| **Archivos** | Supabase Storage + CDN |
| **Pagos** | Flow (server-to-server) |
| **Jobs** | `pg_cron` + `pg_net` / cola de trabajos |
| **Testing** | Vitest + Testing Library + MSW + Playwright |
| **Despliegue** | Vercel o Cloudflare para apps; Supabase para API y DB |
| **Observabilidad** | Logs estructurados + sentry opcional |

> El navegador **no accede directamente a la base de datos**. Solo habla con la API BFF; Supabase Auth puede invocarse directamente para login/OAuth.

---

## 4. Resumen del proyecto

**Enchanted Botanicals** es una tienda online de plantas de colección con una narrativa de fantasía botánica. El cliente puede descubrir especies, filtrar el catálogo, comprar con Flow, consultar sus pedidos y gestionar el cuidado de las plantas que ha adoptado. El administrador dispone de un backoffice para catálogo, inventario, pedidos, contenido y métricas.

El proyecto resuelve la fragmentación entre catálogo, compra y seguimiento de cuidados. La propuesta técnica separa claramente presentación, API y datos: la base de datos resuelve conjuntos, integridad y atomicidad; la API orquesta, autoriza e integra Flow; el cliente presenta y cachea. El objetivo es evitar llamadas innecesarias y procesos duplicados.

---

## 5. Entrevista actual

| Campo | Valor |
| :--- | :--- |
| **Bloque** | B5 — Requisitos no funcionales y stack |
| **Pregunta actual** | OPEN-01 — País, moneda y condiciones de Flow |
| **Preguntas respondidas** | B0–B5 documentadas en borrador |
| **Preguntas abiertas** | OPEN-01 a OPEN-09 |
| **Modo** | Completo |

---

## 6. Sprints

> Borrador para G4. No se crean tickets ejecutables hasta aprobar G4.

| Sprint | Objetivo | Estado |
| :--- | :--- | :--- |
| S0 | Fundaciones: monorepo, tokens, UI base, errores y contratos | Borrador |
| S1 | Supabase local, esquema, RLS, auth y cliente API | Borrador |
| S2 | Catálogo público y detalle de producto | Borrador |
| S3 | Carrito, checkout y Flow en sandbox | Borrador |
| S4 | Cuenta, pedidos, wishlist y Mi Invernadero | Borrador |
| S5 | Admin: dashboard, productos, inventario y pedidos | Borrador |
| S6 | Journal, newsletter y contenido | Borrador |
| S7 | Hardening: E2E, accesibilidad, SEO y observabilidad | Borrador |

---

## 7. Tablero de Tickets

> Estados: Borrador · Pendiente · En curso · En revisión · Hecho.

| ID | Título | Fase/Sprint | Estado | Convenciones |
| :--- | :--- | :--- | :--- | :--- |
| T01 | Base del monorepo | S0 | Borrador | CONV-EST, CONV-GIT |
| T02 | Tokens, Tailwind y Storybook | S0 | Borrador | CONV-UI |
| T03 | Primitivas UI con CVA | S0 | Borrador | CONV-UI, CONV-TIP |
| T04 | Infraestructura de errores y Problem Details | S0 | Borrador | CONV-ERR, CONV-PERF |
| T05 | Supabase local y migraciones | S1 | Borrador | CONV-DB |
| T06 | Esquema inicial y RLS | S1 | Borrador | CONV-DB, CONV-SEG |
| T07 | Auth y guards de ruta | S1 | Borrador | CONV-SEG, CONV-BE |
| T08 | Contratos, OpenAPI y cliente tipado | S1 | Borrador | CONV-API |
| T09 | API de catálogo con búsqueda y facetas | S2 | Borrador | CONV-PERF, CONV-API |
| T10 | UI de catálogo y filtros | S2 | Borrador | CONV-UI |
| T11 | Detalle de producto y SEO | S2 | Borrador | CONV-UI, CONV-API |
| T12 | Carrito y merge de invitado | S3 | Borrador | CONV-BE, CONV-API |
| T13 | Checkout y orden transaccional | S3 | Borrador | CONV-DB, CONV-BE |
| T14 | Flow: pago, retorno y webhook | S3 | Borrador | CONV-BE, CONV-SEG |
| T15 | Confirmación y estado de pedido | S3 | Borrador | CONV-API, CONV-PERF |
| T16 | Cuenta: pedidos y direcciones | S4 | Borrador | CONV-UI, CONV-BE |
| T17 | Wishlist | S4 | Borrador | CONV-BE |
| T18 | Mi Invernadero y bitácora de cuidados | S4 | Borrador | CONV-DB, CONV-UI |
| T19 | Admin: shell y dashboard | S5 | Borrador | CONV-UI, CONV-PERF |
| T20 | Admin: productos, inventario y bulk | S5 | Borrador | CONV-DB, CONV-BE |
| T21 | Admin: pedidos y envíos | S5 | Borrador | CONV-BE, CONV-API |
| T22 | Journal y newsletter | S6 | Borrador | CONV-UI, CONV-DB |
| T23 | Hardening y validación final | S7 | Borrador | Todas |

---

## 8. Próximo paso

1. Resolver **OPEN-01** (país/moneda de Flow) y **OPEN-02** (inventario por SKU o espécimen).
2. Revisar y aprobar **G1**; después **G2**, **G3** y **G4**.
3. No implementar hasta que exista `AUTORIZO IMPLEMENTACIÓN` (G5).

---

## 9. Bloqueos y preguntas abiertas

| ID | Pregunta o bloqueo | Impacto | Responsable | Estado |
| :--- | :--- | :--- | :--- | :--- |
| OPEN-01 | ¿Flow operará en Chile con CLP o la tienda usará EUR? | Modelo de pagos, precios, impuestos y checkout | Alumno | Abierta |
| OPEN-02 | ¿El inventario se gestiona por SKU o por espécimen único? | Modelo de productos, stock, admin y Mi Invernadero | Alumno | Abierta |
| OPEN-03 | ¿El formulario del vlog será IA real o FAQ estático? | Alcance de S6 e integraciones | Alumno | Abierta |
| OPEN-04 | ¿Se incluye Apple OAuth en el MVP? | Auth y requisitos de cuenta Apple | Alumno | Abierta |
| OPEN-05 | Reglas de envío, impuestos y umbral de envío gratis | Total del pedido y Flow | Alumno | Abierta |
| OPEN-06 | ¿Qué paleta es la canónica: la del front matter o la narrativa de `DESIGN.md`? | Tokens y consistencia visual | Alumno | Abierta |
| OPEN-07 | ¿Email transaccional con Supabase o proveedor externo? | Confirmaciones y recuperación | Alumno | Abierta |
| OPEN-08 | ¿Se necesitan roles de admin granulares? | RLS, admin y auditoría | Alumno | Abierta |
| OPEN-09 | ¿Tailwind CSS v3.4 con preset o v4 CSS-first? | Tokens, build y configuración de UI | Alumno | Abierta |

> Una pregunta abierta bloquea una puerta si impide definir un requisito, un dato o una decisión.

---

## 10. Decisiones y notas

| ID | Decisión | Alternativas | Motivo | Consecuencias |
| :--- | :--- | :--- | :--- | :--- |
| DEC-01 | Monorepo con pnpm + Turborepo | npm workspaces, Nx | Dos apps y paquetes compartidos con caché | Requiere disciplina de dependencias |
| DEC-02 | React + Vite + TypeScript estricto | Next.js, Astro | Lo pedido; SPA simple | SEO requiere trabajo extra |
| DEC-03 | Tailwind + CVA + tokens | CSS Modules, styled-components | Variantes legibles y diseño consistente | Hay que mantener el paquete de tokens |
| DEC-04 | Supabase para Auth, DB, Storage y RLS | Backend propio desde cero | Menos infraestructura y seguridad por fila | Dependencia del ecosistema Supabase |
| DEC-05 | API BFF en Edge Functions + PostgREST/RPC | Backend Node propio, cliente directo a DB | Server-to-server y menos infraestructura | Una capa extra entre cliente y DB |
| DEC-06 | Flow solo server-to-server | Integración desde el navegador | Los secretos no se exponen | Dependencia de webhooks y conciliación |
| DEC-07 | Error model `AppError` + Problem Details | Mensajes ad hoc | Contrato estable y trazable | Requiere mapear cada proveedor |
| DEC-08 | DB para conjuntos y atomicidad; API para orquestación | Lógica en API o en el cliente | Menos llamadas y procesos innecesarios | RPC debe mantenerse y probarse |
| DEC-09 | Caché en CDN, TanStack Query y vistas materializadas | Sin caché o solo cliente | Reduce carga y latencia | Hay que invalidar correctamente |
| DEC-10 | Testing con Vitest, MSW y Playwright | Solo pruebas manuales | Calidad y regresión | Más tiempo en F4 |
| DEC-11 | Reglas específicas en `reglas_ui.md` y `reglas_backend.md` | Todo en `convenciones.md` | Documentos enfocados y mantenibles | Hay que mantener referencias cruzadas |
| DEC-12 | Carrito de invitado local y merge al iniciar sesión | Carrito solo autenticado | Mejor conversión | Complejidad de merge y conflictos |

> Registra aquí las decisiones que no quieres volver a discutir.

---

## 11. Última sesión

| Fecha | Bloque o ticket | Avance | Próximo paso |
| :--- | :--- | :--- | :--- |
| 2026-10-22 | Análisis de docs y mockups | Stack, arquitectura, DB, API y reglas redactadas | Revisar OPEN-01/OPEN-02 y aprobar G1 |

---

## 12. Checklist de primer arranque

- [x] Copié el contenido de `setup/` en la raíz del proyecto.
- [x] Abrí OpenCode en la raíz del proyecto.
- [x] Verifiqué que existe `.opencode/commands/pca-inicio.md`.
- [x] Ejecuté `/pca-inicio`.
- [x] Elegí modo completo.
- [ ] Completé G1 (alcance).
- [ ] Completé G2 (requisitos).
- [ ] Completé G3 (diseño).
- [ ] Completé G4 (plan y tickets).
- [ ] Leí el handoff y cambié al agente Build para implementar.
