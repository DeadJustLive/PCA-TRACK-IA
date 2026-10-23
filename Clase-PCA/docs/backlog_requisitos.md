<!-- @pca:start
@id(docs.backlog_requisitos)
@kind(doc)
@relates(docs.convenciones)
@relates(docs.reglas_backend)
@relates(docs.reglas_ui)
@desc(Backlog oficial de requisitos del sistema, historias de usuario y casos límite)
@pca:end -->
# Backlog de Requisitos

> **Instrucción para la IA:** Este documento responde **qué** se construye y **para quién**. No escribas código desde aquí. Si un requisito no tiene criterio de aceptación o caso límite, detente y pregunta.

> **Estado:** Borrador para G1 y G2. Las puertas siguen pendientes de aprobación.

---

## 1. Visión

**Enchanted Botanicals** es una tienda online de plantas de colección con una narrativa de fantasía botánica. El cliente descubre especies, compra con Flow, sigue sus pedidos y registra el cuidado de las plantas que adopta. El negocio administra catálogo, inventario, pedidos y contenido desde un backoffice.

La propuesta une tres mundos que suelen estar separados:

1. **Catálogo y compra:** explorar, filtrar y pagar sin fricción.
2. **Pertenencia:** cada planta comprada puede convertirse en una planta adoptada con bitácora de cuidados.
3. **Operación:** el administrador ve stock, pedidos y métricas sin planillas paralelas.

---

## 2. Objetivo y métricas

| Campo | Valor |
| :--- | :--- |
| **Objetivo del MVP** | Permitir una compra completa con Flow y operar el catálogo y los pedidos desde el admin |
| **Métrica principal** | Tasa de conversión de visita a pedido pagado |
| **Métricas secundarias** | Tiempo de checkout, pedidos con incidencia, stock agotado, uso de Mi Invernadero |
| **Criterio de éxito** | Un cliente puede registrarse, comprar, pagar y ver su pedido; un admin puede gestionar catálogo, stock y pedidos sin tocar la base de datos |

> Las metas numéricas son propuestas para validar en G1. No son compromisos de negocio todavía.

---

## 3. Usuarios y roles

| Rol | Descripción | Permisos principales |
| :--- | :--- | :--- |
| **Visitante** | Persona sin sesión | Ver landing, catálogo, detalle, journal; buscar; carrito local; newsletter |
| **Cliente** | Usuario autenticado | Comprar, ver pedidos, direcciones, wishlist, plantas y bitácora |
| **Administrador** | Dueño o responsable de la tienda | Dashboard, productos, inventario, pedidos, contenido y auditoría |
| **Editor** (futuro) | Redactor de contenido | Journal y newsletter, sin acceso a pedidos ni dinero |

> Para el MVP se implementan `customer` y `admin`. El rol `editor` queda fuera hasta que exista una necesidad real (OPEN-08).

---

## 4. Alcance del MVP

### 4.1 Dentro del MVP

- Landing con identidad visual y secciones de marca.
- Catálogo con búsqueda, filtros, orden y paginación.
- Detalle de producto con imágenes, precio, stock, cuidados y productos relacionados.
- Registro, inicio de sesión, cierre de sesión y recuperación de contraseña.
- Carrito de invitado y carrito autenticado con merge.
- Checkout con dirección y creación de orden.
- Pago con Flow server-to-server y webhook idempotente.
- Confirmación y estado del pedido.
- Cuenta: pedidos, direcciones y wishlist.
- Mi Invernadero: plantas adoptadas y bitácora de cuidados.
- Admin: dashboard, catálogo, inventario, pedidos y envíos.
- Journal público y newsletter.
- Manejo de errores global, por API y por proveedor.
- Tests de flujo crítico y validación de RLS.

### 4.2 Fuera del MVP

- Apple OAuth (OPEN-04).
- Múltiples monedas y conversión automática.
- Suscripciones, membresías o cajas mensuales.
- Reembolsos automáticos y conciliación contable completa.
- Reviews con fotos y moderación.
- Comentarios en el journal.
- Múltiples bodegas o inventario por ubicación.
- Integración con carriers para etiquetas y tracking automático.
- App móvil nativa.
- Programa de puntos, cupones complejos o referidos.
- IA generativa real en el formulario del vlog (OPEN-03).

---

## 5. Restricciones

| ID | Restricción |
| :--- | :--- |
| RES-01 | El navegador no accede directamente a Postgres; toda lectura/escritura pasa por la API BFF. |
| RES-02 | Los secretos de Flow y `service_role` viven solo en el servidor. |
| RES-03 | El pago se confirma por webhook y conciliación, nunca por el query param del retorno. |
| RES-04 | El stack es React + Vite + Tailwind + Supabase + Flow. |
| RES-05 | El proyecto es un monorepo con apps `web` y `admin` y paquetes compartidos. |
| RES-06 | Los componentes compartidos no contienen lógica de dominio. |
| RES-07 | No se escribe código hasta aprobar G1–G4 y recibir `AUTORIZO IMPLEMENTACIÓN`. |
| RES-08 | La tienda opera con una sola moneda por entorno (OPEN-01). |

---

## 6. Historias de usuario

| ID | Historia | Prioridad | Sprint |
| :--- | :--- | :--- | :--- |
| US-01 | Como visitante quiero explorar el catálogo y filtrar por características para encontrar una planta adecuada. | Alta | S2 |
| US-02 | Como visitante quiero ver el detalle de una planta con su precio, stock y cuidados para decidir la compra. | Alta | S2 |
| US-03 | Como visitante quiero crear una cuenta o iniciar sesión para comprar y ver mis pedidos. | Alta | S1 |
| US-04 | Como visitante quiero agregar plantas al carrito sin registrarme para no perder mi selección. | Alta | S3 |
| US-05 | Como cliente quiero pagar con Flow y recibir confirmación para saber que mi pedido existe. | Alta | S3 |
| US-06 | Como cliente quiero ver el estado de mis pedidos para saber cuándo llegan. | Alta | S3/S4 |
| US-07 | Como cliente quiero guardar direcciones para agilizar el checkout. | Media | S4 |
| US-08 | Como cliente quiero guardar plantas favoritas para comprarlas después. | Media | S4 |
| US-09 | Como cliente quiero registrar los cuidados de mis plantas para no olvidar riegos y cambios de luz. | Media | S4 |
| US-10 | Como administrador quiero ver ventas, stock bajo y pedidos recientes en un solo panel. | Alta | S5 |
| US-11 | Como administrador quiero crear y editar productos, imágenes y stock para mantener el catálogo. | Alta | S5 |
| US-12 | Como administrador quiero gestionar pedidos y envíos para operar la tienda. | Alta | S5 |
| US-13 | Como visitante quiero leer el journal para aprender sobre las plantas y la marca. | Baja | S6 |
| US-14 | Como visitante quiero suscribirme al newsletter para recibir novedades. | Baja | S6 |
| US-15 | Como administrador quiero publicar contenido del journal para comunicar la marca. | Baja | S6 |
| US-16 | Como administrador quiero que las acciones sensibles queden auditadas para investigar incidentes. | Media | S5 |

---

## 7. Requisitos funcionales

| ID | Requisito | Criterio de aceptación | Historia |
| :--- | :--- | :--- | :--- |
| **RF-01** | Catálogo público con búsqueda, filtros por categoría, luz, riego y rareza, orden y paginación. | Dado un visitante, cuando aplica filtros y ordena, entonces recibe una página de hasta 24 productos con facetas y cursor; si no hay resultados, ve un estado vacío claro. | US-01 |
| **RF-02** | Detalle de producto por slug. | Dado un producto activo, cuando el visitante abre su slug, entonces ve imágenes, precio, stock, cuidados y relacionados; si está archivado, recibe 404 amable. | US-02 |
| **RF-03** | Registro, login, logout y recuperación de contraseña. | Dado un visitante, cuando se registra con email válido, entonces recibe confirmación y puede iniciar sesión; un email duplicado muestra un error de dominio. | US-03 |
| **RF-04** | Carrito de invitado y carrito autenticado con merge. | Dado un invitado con carrito local, cuando inicia sesión, entonces sus ítems se fusionan sin duplicar productos y se validan cantidades contra stock. | US-04 |
| **RF-05** | Checkout con dirección y creación de orden. | Dado un carrito válido, cuando confirma el checkout, entonces se crea una orden `pending_payment` con snapshot de precios y una reserva de stock; un doble submit no crea dos órdenes. | US-05 |
| **RF-06** | Pago con Flow server-to-server. | Dado un checkout confirmado, cuando se inicia el pago, entonces el navegador recibe la URL de Flow; el webhook valida firma, registra el evento y actualiza el pago de forma idempotente. | US-05 |
| **RF-07** | Confirmación y estado del pedido. | Dado un pago confirmado, cuando el cliente abre la orden, entonces ve estado, ítems, total y timeline; el estado no se actualiza por el retorno del navegador. | US-05/06 |
| **RF-08** | Historial de pedidos del cliente. | Dado un cliente autenticado, cuando abre sus pedidos, entonces ve una lista paginada con estado y total; no puede ver pedidos de otro usuario. | US-06 |
| **RF-09** | Gestión de direcciones. | Dado un cliente, cuando crea, edita o elimina una dirección, entonces los cambios se reflejan en su cuenta y en el checkout; no puede usar direcciones de otro usuario. | US-07 |
| **RF-10** | Wishlist. | Dado un cliente, cuando agrega o quita una planta, entonces la lista persiste y no se duplica; un visitante es redirigido a login. | US-08 |
| **RF-11** | Mi Invernadero y bitácora de cuidados. | Dado un pedido pagado, cuando el cliente abre Mi Invernadero, entonces ve sus plantas adoptadas; puede registrar un cuidado con fecha y próximo recordatorio. | US-09 |
| **RF-12** | Dashboard administrativo. | Dado un admin, cuando abre el dashboard, entonces ve KPIs, ventas por categoría, stock bajo y pedidos recientes en una sola llamada. | US-10 |
| **RF-13** | Admin de productos e inventario. | Dado un admin, cuando crea o edita un producto, entonces puede gestionar datos, imágenes, estado y stock; cada ajuste de stock genera un movimiento. | US-11 |
| **RF-14** | Admin de pedidos y envíos. | Dado un admin, cuando abre un pedido, entonces puede cambiar estados válidos, registrar tracking y ver el historial; no puede borrar pagos. | US-12 |
| **RF-15** | Journal público. | Dado un visitante, cuando abre el journal, entonces ve posts publicados con filtros y detalle; los borradores no son visibles. | US-13 |
| **RF-16** | Newsletter. | Dado un visitante, cuando se suscribe con email válido, entonces queda en estado pendiente y recibe confirmación; un email repetido no duplica la suscripción. | US-14 |
| **RF-17** | Admin de contenido. | Dado un admin, cuando crea un post, entonces puede guardarlo como borrador o publicarlo; al publicar se invalida la caché del journal. | US-15 |
| **RF-18** | Auditoría de acciones sensibles. | Dado un admin, cuando cambia precios, stock, pedidos o roles, entonces se registra actor, acción, entidad y fecha. | US-16 |
| **RF-19** | Webhook y conciliación de Flow. | Dado un evento repetido o fuera de orden, cuando llega al webhook, entonces no duplica pagos y deja el estado consistente; un evento inválido se rechaza y se registra. | US-05 |

---

## 8. Requisitos no funcionales

| ID | Requisito | Criterio verificable |
| :--- | :--- | :--- |
| **RNF-01** | Rendimiento de API | p95 < 300 ms en lecturas; p95 < 800 ms en checkout sin contar Flow. |
| **RNF-02** | Rendimiento de DB | Consultas de pantalla < 100 ms; máximo 2 round trips por request de lectura. |
| **RNF-03** | Presupuesto de llamadas | Una pantalla = una llamada de composición; el cliente no hace N+1. |
| **RNF-04** | Seguridad | RLS en toda tabla; `service_role` solo en servidor; secretos fuera del bundle. |
| **RNF-05** | Accesibilidad | WCAG 2.1 AA: foco visible, teclado, contraste, labels y `aria` cuando corresponda. |
| **RNF-06** | Responsive | Mobile-first; usable desde 360 px hasta 1440 px. |
| **RNF-07** | SEO | Landing, catálogo y journal con metadatos, canonical y sitemap; detalle con datos estructurados. |
| **RNF-08** | Observabilidad | Logs estructurados con `traceId`, errores de API y webhook, alertas de pagos fallidos. |
| **RNF-09** | Disponibilidad | 99,5 % mensual para catálogo y checkout en producción. |
| **RNF-10** | Privacidad | Datos personales minimizados; no se registran tarjetas; retención definida en G3. |
| **RNF-11** | Testing | Unitarios de dominio, integración de API/RPC, RLS y E2E del camino de compra. |
| **RNF-12** | Mantenibilidad | TypeScript estricto, sin `any`, archivos dentro de `@limit`, contratos versionados. |
| **RNF-13** | Respaldos | Backups diarios de Postgres y prueba de restauración antes de producción. |
| **RNF-14** | Abuso | Rate limiting en auth, newsletter, checkout y webhook. |

---

## 9. Edge cases

| ID | Caso límite | Comportamiento esperado |
| :--- | :--- | :--- |
| **EDGE-01** | Dos clientes compran la última unidad a la vez | La RPC reserva stock de forma atómica; uno recibe `OUT_OF_STOCK`. |
| **EDGE-02** | Flow envía el mismo webhook dos veces | `webhook_events` lo deduplica; no se duplica el pago ni la orden. |
| **EDGE-03** | Webhook llega antes que el retorno del navegador | El webhook manda; la UI consulta el estado y no asume éxito por la URL. |
| **EDGE-04** | Pago rechazado | La orden queda `pending_payment` o `cancelled`; se liberan reservas y se muestra reintento. |
| **EDGE-05** | Flow no responde o hay timeout | Se registra el intento, no se marca pagado y se ofrece reintento/conciliación. |
| **EDGE-06** | Usuario manipula el retorno de Flow | El servidor ignora el query param y valida contra Flow/webhook. |
| **EDGE-07** | Reserva de stock expirada | Un job libera la reserva y cancela la orden pendiente. |
| **EDGE-08** | Precio cambió mientras el producto estaba en el carrito | El checkout muestra el precio vigente y pide confirmación si cambió. |
| **EDGE-09** | Sesión expira en checkout | Se conserva el carrito y se redirige a login; al volver se retoma. |
| **EDGE-10** | Usuario sin rol admin intenta abrir el admin | La API responde 403 y la UI no muestra datos. |
| **EDGE-11** | Email ya registrado | Error de dominio claro; no se filtra si la cuenta existe en recuperación. |
| **EDGE-12** | Contraseña débil | Validación en cliente y servidor con mensaje único. |
| **EDGE-13** | Búsqueda sin resultados | Estado vacío con sugerencias y opción de limpiar filtros. |
| **EDGE-14** | Imagen inválida o demasiado grande | Se rechaza antes de subir y se muestra el límite. |
| **EDGE-15** | Admin edita un producto y el CDN sirve versión vieja | Se invalida la clave de caché al publicar. |
| **EDGE-16** | Usuario sin conexión | TanStack Query conserva datos; se muestra estado offline y no se pierde el carrito local. |
| **EDGE-17** | Doble clic en “Pagar” | La idempotency key evita dos órdenes o dos sesiones de pago. |
| **EDGE-18** | Pago confirmado pero falla el email | La orden sigue pagada; el email se reintenta y se registra el fallo. |
| **EDGE-19** | Reembolso solicitado | Se registra como evento manual; el estado de la orden y el pago quedan auditados. |
| **EDGE-20** | Producto archivado aparece en un pedido viejo | El snapshot del ítem se conserva; no se rompe el historial. |
| **EDGE-21** | Exportación grande en admin | Se procesa como job y se entrega un enlace, no se bloquea la request. |
| **EDGE-22** | Rate limit alcanzado | 429 con `Retry-After` y mensaje accionable. |
| **EDGE-23** | Dirección inválida o incompleta | Validación con Zod en cliente y servidor; no se crea la orden. |
| **EDGE-24** | Moneda del producto no coincide con la de Flow | Se bloquea el checkout y se alerta; OPEN-01 debe resolverlo. |
| **EDGE-25** | Firma de webhook inválida | 401/400, no se procesa y se registra el intento. |

---

## 10. Reglas de negocio

| ID | Regla |
| :--- | :--- |
| **RN-01** | El precio se calcula y valida en el servidor; el cliente nunca envía el total. |
| **RN-02** | El stock se reserva al crear la orden y se consume cuando el pago se confirma. |
| **RN-03** | La orden guarda snapshot de nombre, precio y datos de envío; un cambio posterior del producto no altera el historial. |
| **RN-04** | Solo una orden pagada pasa a preparación. |
| **RN-05** | No se borran órdenes, pagos ni movimientos de inventario; se corrigen con estados y auditoría. |
| **RN-06** | Un cliente tiene un carrito activo; el carrito de invitado se fusiona al iniciar sesión. |
| **RN-07** | Wishlist y Mi Invernadero requieren autenticación. |
| **RN-08** | Las plantas adoptadas se crean a partir de órdenes pagadas. |
| **RN-09** | Solo el contenido publicado es visible en el journal. |
| **RN-10** | Flow es la fuente de verdad del pago; la UI solo refleja el estado persistido. |
| **RN-11** | No se almacenan datos de tarjeta. |
| **RN-12** | Toda mutación sensible del admin se audita. |
| **RN-13** | El envío y los impuestos se calculan con reglas configurables; OPEN-05 debe definirlas. |
| **RN-14** | Una tienda/entorno usa una sola moneda; OPEN-01 debe definirla. |
| **RN-15** | Los endpoints de escritura aceptan `Idempotency-Key`. |

---

## 11. Trazabilidad

| Requisito | Historia | Edge cases | Ticket |
| :--- | :--- | :--- | :--- |
| RF-01 | US-01 | EDGE-13, EDGE-15 | T09, T10 |
| RF-02 | US-02 | EDGE-20 | T11 |
| RF-03 | US-03 | EDGE-09, EDGE-11, EDGE-12 | T07 |
| RF-04 | US-04 | EDGE-08, EDGE-09 | T12 |
| RF-05 | US-05 | EDGE-01, EDGE-17, EDGE-23 | T13 |
| RF-06 | US-05 | EDGE-02, EDGE-03, EDGE-05, EDGE-06, EDGE-25 | T14 |
| RF-07 | US-05/06 | EDGE-03, EDGE-04 | T15 |
| RF-08 | US-06 | EDGE-10 | T16 |
| RF-09 | US-07 | EDGE-23 | T16 |
| RF-10 | US-08 | — | T17 |
| RF-11 | US-09 | EDGE-18 | T18 |
| RF-12 | US-10 | — | T19 |
| RF-13 | US-11 | EDGE-14, EDGE-15 | T20 |
| RF-14 | US-12 | EDGE-19, EDGE-21 | T21 |
| RF-15 | US-13 | — | T22 |
| RF-16 | US-14 | EDGE-11 | T22 |
| RF-17 | US-15 | EDGE-15 | T22 |
| RF-18 | US-16 | EDGE-10 | T20/T21 |
| RF-19 | US-05 | EDGE-02, EDGE-03, EDGE-05 | T14 |

---

## 12. Preguntas abiertas

| ID | Pregunta | Por qué bloquea |
| :--- | :--- | :--- |
| **OPEN-01** | ¿Flow opera en Chile con CLP o la tienda vende en EUR? | Define precios, impuestos, checkout, datos y textos. |
| **OPEN-02** | ¿Inventario por SKU o por espécimen único? | Cambia el modelo de stock, el admin y Mi Invernadero. |
| **OPEN-03** | ¿El formulario del vlog usa IA real o FAQ/contacto? | Cambia el alcance de S6 y las integraciones. |
| **OPEN-04** | ¿Apple OAuth entra en el MVP? | Cambia auth, cuenta y pruebas. |
| **OPEN-05** | ¿Envío plano, por zona o gratis desde un umbral? ¿IVA incluido? | Afecta total, Flow y contratos. |
| **OPEN-06** | ¿Qué paleta es la canónica? | Afecta tokens y consistencia visual. |
| **OPEN-07** | ¿Email transaccional con Supabase o proveedor externo? | Afecta confirmaciones y recuperación. |
| **OPEN-08** | ¿Se necesitan roles admin granulares? | Afecta RLS, auditoría y UI. |
| **OPEN-09** | ¿Tailwind CSS v3.4 con preset o v4 CSS-first? | Afecta tokens, build y configuración de UI. |

---

## 13. Historial de cambios

| Fecha | Cambio |
| :--- | :--- |
| 2026-10-22 | Borrador inicial de alcance, requisitos, RNF, edge cases y trazabilidad. |
