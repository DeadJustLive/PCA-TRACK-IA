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
