# AGENTS.md — Enrutador de Contexto y Flujo PCA

> **Instrucción para la IA:** Lee obligatoriamente este archivo cada vez que inicies una nueva sesión o chat. Este documento define las reglas arquitectónicas y el flujo de trabajo del proyecto.

---

## 0. Cómo usar este archivo (guía rápida para el alumno)

1. Copia la carpeta `setup/` a la raíz de tu proyecto antes de empezar.
2. Abre tu IA (ChatGPT, Claude, Cursor, etc.) y pega este mensaje de arranque:

   > "Lee el archivo `AGENTS.md` completo y el estado actual en `docs/estado_proyecto.md`. Dime en qué fase estamos y cuál es el siguiente paso."

3. A partir de ahí, sigue el **Flujo de Fases** (sección 1) y el **Protocolo de Sesión** (sección 2). La IA no debe adelantarse de fase sin tu aprobación.

---

## 1. Flujo de Fases PCA (control de avance)

El proyecto avanza por fases secuenciales. **Regla de oro:** la IA debe declarar siempre en qué fase está y **NO puede avanzar a la siguiente sin tu aprobación explícita**.

| Fase | Nombre | Objetivo | Entregable | Criterio de salida |
| :--- | :--- | :--- | :--- | :--- |
| **F0** | Setup | Definir stack y dejar lista la configuración | `docs/estado_proyecto.md` con stack definido | Stack confirmado y `AGENTS.md` adaptado |
| **F1** | Levantamiento | Aterrizar la idea, encontrar edge cases | `backlog_requisitos.md` | Backlog revisado y aprobado |
| **F2** | Plan de Sprints | Dividir el backlog en sprints manejables | `plan_sprints.md` | Sprints aprobados y priorizados |
| **F3** | Ejecución por tickets | Programar con micro-tareas controladas | Tickets completados + código | Ticket con Definition of Done cumplido |
| **F4** | Validación / Testing | Verificar calidad y casos límite | Tests y evidencia de pruebas | Todo ticket validado |
| **F5** | Cierre / Extracción | Extraer componentes reutilizables y registrar aprendizajes | Biblioteca de componentes + `docs/cicatrices_guerra.md` | Aprendizajes registrados |

### Reglas de transición
- **F1 → F2 → F3:** la IA solo pasa de fase cuando tú dices "aprobado".
- **F3 → F4:** ningún ticket se considera terminado sin su *Definition of Done*.
- **F5:** obligatorio registrar las cicatrices (errores y soluciones) antes de cerrar.

### Herramientas por fase
- **F1:** usa el prompt `prompts/workflow_01_levantamiento_ia.md`.
- **F5:** usa el prompt `prompts/workflow_02_extraccion_componentes.md`.

---

## 2. Protocolo de Sesión (checklist guiado)

### Al INICIAR cada sesión
1. Leer `AGENTS.md` (este archivo) y `docs/estado_proyecto.md`.
2. Declarar la fase actual y el próximo paso pendiente.
3. Elegir **un solo** ticket del tablero (`docs/plantilla_ticket.md` como formato).
4. Revisar las **convenciones aplicables** del ticket en `docs/convenciones.md`.

### Durante el trabajo
1. Trabajar en **micro-tareas** (una unidad verificable a la vez).
2. Respetar `docs/convenciones.md` y las anotaciones `@kind/@limit/@contract`.
3. Si hay ambigüedad o falta un caso límite, la IA debe **detenerse y preguntar**.
4. Crear una rama de trabajo según `docs/git.md` antes de programar.

### Al CERRAR cada sesión
1. Verificar el ticket contra su *Definition of Done*.
2. Actualizar `docs/estado_proyecto.md` (fase, ticket, próximo paso).
3. Registrar en `docs/cicatrices_guerra.md` cualquier error resuelto.
4. Proponer el mensaje de commit (la IA **no** hace commit sola). Ver `docs/git.md`.

---

## 3. Reglas Inquebrantables de la Sesión
- **Regla 0 (Curiosidad Obligatoria):** Tienes PROHIBIDO programar si el prompt tiene alta ambigüedad técnica o no contempla casos límite (*Edge Cases*). Estás obligado a detenerte y hacer preguntas hasta que la incertidumbre baje a cero.
- **NO hagas "Vibe Coding".** Sigue el método PCA (Por qué, Cómo, A qué) antes de programar.
- **Respeta los Límites (Enforcement):** Si un archivo tiene la anotación `@limit(lines: X)`, detente y refactoriza si vas a sobrepasar ese número.
- **Tipado Estricto (si el stack lo permite):** Prohibido usar `any` en TypeScript.
- **Contratos Duros:** Respeta las interfaces. Si olvidas un método, el compilador fallará.
- **Sin secretos en el código:** Nunca escribas claves, tokens o contraseñas dentro del código. Usa variables de entorno.
- **Una micro-tarea a la vez:** No generes archivos enteros "por si acaso". Programa solo lo que el ticket pide.

---

## 4. Gestión de Contexto bajo Demanda

Para evitar la Amnesia de Contexto, no leas todo el proyecto de golpe. Lee los siguientes documentos solo si tu tarea cumple la condición (Trigger):

| Condición de la Tarea (Trigger) | Archivo a Leer |
| :--- | :--- |
| Vas a modificar el diseño visual o CSS | `docs/reglas_ui.md` |
| Vas a interactuar con la Base de Datos | `docs/reglas_backend.md` |
| Vas a programar cualquier tarea (nomenclatura, estilo, errores) | `docs/convenciones.md` |
| Vas a hacer ramas, commits o merge | `docs/git.md` |
| Encontramos un error y vamos a debugear | `docs/cicatrices_guerra.md` (Registro de errores) |
| Necesitas saber dónde estamos parados | `docs/estado_proyecto.md` |
| Vas a anotar archivos o generar el grafo de impacto | `docs/sistema_anotaciones.md` + `tools/README.md` |

> Los archivos `docs/reglas_ui.md` y `docs/reglas_backend.md` los genera el proyecto cuando defina su stack. Si aún no existen y tu tarea los requiere, la IA debe avisarte.

---

## 5. Sistema de Anotaciones (Frenos de Emergencia)

Todo archivo crítico que generes debe incluir en su cabecera un **bloque de anotación**. El diccionario completo de etiquetas está en `docs/sistema_anotaciones.md`. Formato canónico (una etiqueta por línea):

```
@pca:start
@id(auth.login)
@kind(component)
@limit(lines: 120)
@contract(props: email, password)
@relates(auth.session, user.model)
@desc(Formulario de inicio de sesión)
@pca:end
```

Reglas asociadas:
- **Antes de editar un archivo**, ejecuta `python tools/pca_annotator.py impact <id>` para conocer qué depende de él (análisis de impacto).
- Al **crear un archivo**, agrégalo al manifiesto `tools/pca.config.json` y ejecuta `python tools/pca_annotator.py annotate`.
- El programa (`tools/pca_annotator.py`) **inyecta el bloque** y genera el grafo; no edites el bloque a mano si usas `annotate`.
- `@id` = clave primaria del nodo · `@relates` = clave foránea. `check` detecta relaciones rotas.

---

## 6. Bucle de Aprendizaje (Learning Loop)

Si cometes un error lógico, no lo olvidaremos. Lo documentaremos en `docs/cicatrices_guerra.md` con el siguiente formato:

```
// @learn-error id=1 input="x" expected="y" actual="z" fix="solución"
```

Antes de proponer soluciones complejas, revisa si ya cometiste ese error en el pasado.

---

## 7. Stack Tecnológico (Por Definir)

> **Instrucción de Inicialización:** Si este es el primer mensaje de nuestro proyecto y el Stack Tecnológico aún dice "Por Definir", tu primera acción obligatoria es preguntarme: "¿Qué stack tecnológico vamos a utilizar (Frontend, Backend, Base de Datos, Estilos)?"

> Una vez que te responda, deberás usar esas tecnologías como contexto obligatorio para cualquier Workflow que apliquemos, y me sugerirás actualizar este archivo reemplazando el "Por Definir" con el listado definitivo de nuestro stack. Registra también el stack en `docs/estado_proyecto.md`.

- **Frontend:** Por Definir
- **Backend:** Por Definir
- **Base de Datos:** Por Definir
- **Estilos:** Por Definir

---

## 8. Mapa de Documentos

| Archivo | Para qué sirve |
| :--- | :--- |
| `AGENTS.md` | Este archivo. Enrutador de contexto y flujo de fases. |
| `docs/estado_proyecto.md` | Tablero de control: fase, sprints, tickets. Motor anti-amnesia. |
| `docs/convenciones.md` | Reglas de nomenclatura, estilo y buenas prácticas (asignables a tickets). |
| `docs/git.md` | Estrategia de ramas, commits y flujo de versionado. |
| `docs/plantilla_ticket.md` | Formato estándar para definir y ejecutar tickets. |
| `docs/cicatrices_guerra.md` | Registro de errores y soluciones (Learning Loop). |
| `docs/sistema_anotaciones.md` | Diccionario de anotaciones PCA y cómo usarlas. |
| `tools/pca_annotator.py` | CLI: inyecta anotaciones y genera el grafo de impacto. |
| `tools/README.md` | Guía del anotador y cómo agregar lenguajes. |
| `prompts/workflow_01_levantamiento_ia.md` | Prompt para iniciar F1 (levantamiento + sprints). |
| `prompts/workflow_02_extraccion_componentes.md` | Prompt para iniciar F5 (extracción de componentes). |
