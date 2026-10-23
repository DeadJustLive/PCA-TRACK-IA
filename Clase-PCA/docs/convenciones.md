<!-- @pca:start
@id(docs.convenciones)
@kind(doc)
@relates(docs.sistema_anotaciones)
@desc(Convenciones generales del proyecto)
@pca:end -->
# Convenciones Generales del Proyecto

> **Instrucción para la IA:** Aplica estas reglas en todo código que generes. Cada regla tiene un **ID**. Cuando un ticket indique convenciones aplicables (por ejemplo "Aplicar `CONV-NAM-01`"), respétalas de forma obligatoria.

> **Cómo se usan:** El *Definition of Done* de un ticket no está completo si las convenciones referenciadas no se cumplen. Estas reglas son agnósticas del stack: si el stack define algo más específico, ese detalle vive en `docs/reglas_ui.md` o `docs/reglas_backend.md`.

---

## CONV-GEN — Generales

- **CONV-GEN-01 — Idioma:** El código (variables, funciones, archivos, commits) se escribe en **inglés**. Los comentarios de valor, la documentación y los mensajes al usuario van en **español**.
- **CONV-GEN-02 — Sin código muerto:** No dejes código comentado, funciones sin usar ni `console.log`/`print` de depuración en la entrega.
- **CONV-GEN-03 — Una responsabilidad por archivo:** Cada archivo hace una sola cosa. Si describirlo requiere un "y", probablemente debe dividirse.
- **CONV-GEN-04 — Legibilidad antes que astucia:** Prioriza nombres claros y código simple. Nada de "one-liners" imposibles de leer.
- **CONV-GEN-05 — Documentación viva:** Si cambias una regla de comportamiento, actualiza el doc correspondiente en la misma tarea.

---

## CONV-NAM — Nomenclatura

- **CONV-NAM-01 — Variables y funciones:** `camelCase` → `getUserById`, `isAuthenticated`.
- **CONV-NAM-02 — Componentes y clases:** `PascalCase` → `UserCard`, `AuthService`.
- **CONV-NAM-03 — Constantes globales:** `SCREAMING_SNAKE_CASE` → `MAX_RETRY_COUNT`.
- **CONV-NAM-04 — Archivos y carpetas:** `kebab-case` para archivos sueltos; una carpeta por componente cuando aplique. Sé consistente con la convención del framework elegido.
- **CONV-NAM-05 — Base de datos:** tablas y columnas en `snake_case` y plural para tablas → `user_profiles`, `created_at`.
- **CONV-NAM-06 — Booleanos:** prefijo `is`, `has`, `can` → `isActive`, `hasPermission`.
- **CONV-NAM-07 — Prohibido abreviar por ahorrar letras:** `usr`, `btn`, `cfg` ✗ → `user`, `button`, `config` ✓. (Excepción: abreviaturas universales como `id`, `url`.)

---

## CONV-EST — Estructura del proyecto

- **CONV-EST-01 — Separación por capas:** mantén separado el acceso a datos, la lógica de negocio y la presentación.
- **CONV-EST-02 — Carpetas predecibles:** agrupa por dominio/característica, no por tipo de archivo suelto. La estructura se documenta en `docs/estado_proyecto.md` una vez definida la F0.
- **CONV-EST-03 — Archivos de configuración en la raíz:** `.env`, configuración de linting y build viven en la raíz, nunca dentro del código fuente.

---

## CONV-TIP — Tipado y reglas duras

- **CONV-TIP-01 — Sin tipos implícitos peligrosos:** si el stack permite tipos, prohíbe el escape `any` (o equivalente). Todo dato debe tener tipo claro.
- **CONV-TIP-02 — Contratos primero:** define interfaces/contratos antes de implementar. Si cambia el contrato, se actualiza explícitamente.
- **CONV-TIP-03 — Funciones puras cuando se pueda:** recibe datos por parámetros y devuelve un resultado. Evita depender del estado global dentro de la lógica.
- **CONV-TIP-04 — Límite de líneas:** respeta `@limit(lines: X)`. Si un archivo lo supera, refactoriza antes de seguir.

---

## CONV-ERR — Manejo de errores

- **CONV-ERR-01 — Nunca fallar en silencio:** todo error se captura y se comunica con un mensaje descriptivo.
- **CONV-ERR-02 — Errores esperados vs. inesperados:** valida entradas del usuario (esperados) y captura excepciones de infraestructura (inesperados) por separado.
- **CONV-ERR-03 — Fallar temprano:** valida los datos al inicio de la función, no a mitad de la lógica.
- **CONV-ERR-04 — Mensajes útiles:** un mensaje de error debe decir **qué** falló y **dónde**, sin exponer datos sensibles.

---

## CONV-SEG — Seguridad

- **CONV-SEG-01 — Sin secretos en el código:** claves, tokens y contraseñas van en variables de entorno (`.env`), nunca en el repositorio.
- **CONV-SEG-02 — `.env` fuera del control de versiones:** asegúrate de que `.env` esté en `.gitignore`. Ver `docs/git.md`.
- **CONV-SEG-03 — Validar toda entrada externa:** lo que viene del usuario o de una API se valida antes de usarse.
- **CONV-SEG-04 — Mínimo privilegio:** accede solo a los datos/recursos necesarios para la tarea.

---

## CONV-UI — Interfaz (si aplica)

- **CONV-UI-01 — Componentes desacoplados:** un componente de UI recibe datos por propiedades (props) y no contiene lógica de negocio.
- **CONV-UI-02 — Estados explícitos:** toda vista contempla sus estados: cargando, vacío, error y con datos.
- **CONV-UI-03 — Accesibilidad básica:** etiquetas en campos, contraste legible y navegación por teclado.
- **CONV-UI-04 — Estilos consistentes:** usa las variables/tokens de diseño del proyecto; no inventes colores ni tamaños sueltos.

---

## CONV-DOC — Documentación y anotaciones

- **CONV-DOC-01 — Bloque de anotación:** todo archivo crítico declara su cabecera con el bloque canónico (`@id`, `@kind`, `@limit`, `@contract`, `@relates`, `@desc`). El diccionario está en `docs/sistema_anotaciones.md` y el formato se aplica con `python tools/pca_annotator.py annotate`.
- **CONV-DOC-02 — Contratos declarados:** los servicios declaran su contrato → `@contract(auth)`.
- **CONV-DOC-03 — Comentarios con valor:** explica el *por qué*, no el *qué* (el código ya dice el qué).
- **CONV-DOC-04 — README por módulo:** cada carpeta relevante puede tener un README breve que explique su propósito.
- **CONV-DOC-05 — Grafo actualizado:** tras anotar archivos, regenera el grafo con `python tools/pca_annotator.py graph` y revisa el impacto con `impact <id>`.
- **CONV-DOC-06 — Reglas específicas:** si el cambio afecta UI, DB, API, Flow o performance, actualiza también `docs/reglas_ui.md` o `docs/reglas_backend.md` en la misma tarea.

---

## CONV-STACK — Reglas específicas del stack

> Estas reglas complementan las anteriores. El detalle operativo vive en `docs/reglas_ui.md` y `docs/reglas_backend.md`; aquí quedan los IDs que los tickets deben citar.

### Monorepo y tipado

- **CONV-EST-04 — Límites del monorepo:** `apps/*` pueden depender de `packages/*`; `packages/ui` no importa `features` ni clientes de datos; `packages/domain` no importa React ni Supabase; `packages/flow` y secretos solo se importan en Edge.
- **CONV-EST-05 — Una pantalla, una llamada:** cada pantalla consume un endpoint de composición. Prohibido hacer fan-out a varios endpoints para pintar una vista.
- **CONV-TIP-05 — TypeScript estricto:** `strict: true`, sin `any`, sin `@ts-ignore` sin justificación, sin non-null assertion abusiva. Los contratos se validan con Zod.
- **CONV-TIP-06 — Contratos compartidos:** requests/responses viven en `packages/contracts`; no se duplican tipos entre `web` y `admin`.

### Errores y seguridad

- **CONV-ERR-05 — `AppError` + Problem Details:** todo error de API se serializa como `application/problem+json` con `code`, `status`, `detail`, `traceId` y `errors[]`. Ver `docs/reglas_backend.md`.
- **CONV-ERR-06 — Sin errores crudos del proveedor:** Flow, Postgres y Supabase se mapean a códigos de dominio; no se filtran stack traces ni SQL.
- **CONV-SEG-05 — `service_role` solo servidor:** prohibido en el navegador, en `VITE_*` o en código compartido con UI.
- **CONV-SEG-06 — RLS obligatoria:** toda tabla del esquema público tiene RLS activa y tests por rol.
- **CONV-SEG-07 — Flow server-to-server:** el navegador nunca ve `secretKey`; el webhook valida firma y es idempotente.

### UI

- **CONV-UI-05 — CVA + tokens:** todo componente con variantes usa `cva` + `cn`; prohibido hardcodear colores, tamaños o sombras.
- **CONV-UI-06 — Estados completos:** loading, empty, error, success y partial; los formularios muestran errores por campo.
- **CONV-UI-07 — Componentes agnósticos:** `packages/ui` no conoce dominio, API ni router.
- **CONV-UI-08 — Accesibilidad AA:** foco visible, teclado, labels, contraste y `prefers-reduced-motion`.

### Backend y performance

- **CONV-PERF-01 — Presupuesto de llamadas:** máximo 2 round trips a DB por lectura y 1 llamada externa por checkout.
- **CONV-PERF-02 — Sin N+1:** listas se resuelven con RPC/vista, no con consultas por ítem.
- **CONV-PERF-03 — Caché con invalidación:** CDN para público, TanStack Query para cliente, vistas materializadas para admin. No cachear datos privados en CDN.
- **CONV-DB-01 — Migraciones forward-only:** no se edita una migración aplicada; cambios destructivos en dos pasos.
- **CONV-DB-02 — Dinero en centavos:** `*_cents` + `currency`; nunca `float`.
- **CONV-DB-03 — Snapshots en pedidos:** el historial no depende del catálogo actual.
- **CONV-DB-04 — Idempotencia:** escrituras críticas aceptan `Idempotency-Key` o clave natural única.
