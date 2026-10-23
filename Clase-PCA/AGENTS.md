# AGENTS.md — Enrutador de Contexto y Flujo PCA

> **Instrucción para la IA:** Lee obligatoriamente este archivo cada vez que inicies una nueva sesión o chat. Este documento define las reglas arquitectónicas y el flujo de trabajo del proyecto.

---

## 0. Cómo usar este archivo (guía rápida para el alumno)

1. Copia **el contenido** de `setup/` a la raíz de tu proyecto (no copies la carpeta `setup/`). `AGENTS.md`, `docs/`, `prompts/` y `.opencode/` deben quedar en la raíz.
2. Abre OpenCode en la raíz del proyecto.
3. Para iniciar el análisis y diseño, escribe:

   > `/pca-inicio`

   El comando activa el agente `pca-analista`, que **solo puede editar documentación en `docs/`**. No puede tocar código.
4. Cuando el análisis termine con G4 aprobado, cambia al agente **Build** y escribe `AUTORIZO IMPLEMENTACIÓN` para empezar F3.
5. Si usas ChatGPT, Claude o Gemini en lugar de OpenCode, pega el contenido de `prompts/00_inicio_analisis_diseno.md` y adjunta `AGENTS.md` y `docs/estado_proyecto.md`.
6. A partir de ahí, sigue el **Flujo de Fases** (sección 1) y el **Protocolo de Sesión** (sección 2). La IA no debe adelantarse de fase sin tu aprobación.

---

## 1. Flujo de Fases PCA (control de avance)

El proyecto avanza por fases secuenciales. **Regla de oro:** la IA debe declarar siempre en qué fase está y **NO puede avanzar a la siguiente sin tu aprobación explícita**.

| Fase | Nombre | Objetivo | Entregable | Criterio de salida |
| :--- | :--- | :--- | :--- | :--- |
| **F0** | Setup | Definir stack y dejar lista la configuración | `docs/estado_proyecto.md` con stack definido | Stack confirmado y registrado |
| **F1** | Levantamiento | Aterrizar la idea, encontrar edge cases | `backlog_requisitos.md` + `modelo_datos.md` + `arquitectura.md` | Puertas G1–G3 aprobadas |
| **F2** | Plan de Sprints | Dividir el backlog en sprints manejables | `plan_sprints.md` | G4 aprobada y tickets con DoR |
| **F3** | Ejecución por tickets | Programar con micro-tareas controladas | Tickets completados + código | Ticket con Definition of Done cumplido |
| **F4** | Validación / Testing | Verificar calidad y casos límite | Tests y evidencia de pruebas | Todo ticket validado |
| **F5** | Cierre / Extracción | Extraer componentes reutilizables y registrar aprendizajes | Biblioteca de componentes + `docs/cicatrices_guerra.md` | Aprendizajes registrados |

### Reglas de transición
- **F1 → F2 → F3:** la IA solo pasa de fase cuando tú dices "aprobado" en cada puerta (G1–G4).
- **F3 no empieza sin G5:** la implementación requiere la frase `AUTORIZO IMPLEMENTACIÓN`.
- **F3 → F4:** ningún ticket se considera terminado sin su *Definition of Done*.
- **F5:** obligatorio registrar las cicatrices (errores y soluciones) antes de cerrar.

### Puertas de análisis (F0–F2)

Antes de programar, el proyecto pasa por cuatro puertas. No se abre la siguiente sin la palabra `aprobado`:

| Puerta | Qué se aprueba | Documento |
| :--- | :--- | :--- |
| **G1** | Problema, usuarios, MVP y fuera de alcance | `docs/backlog_requisitos.md` |
| **G2** | Requisitos, RNF, edge cases y criterios | `docs/backlog_requisitos.md` |
| **G3** | Modelo de datos, arquitectura y riesgos | `docs/modelo_datos.md` + `docs/arquitectura.md` |
| **G4** | Sprints, tickets y Definition of Ready | `docs/plan_sprints.md` + `docs/tickets/` |
| **G5** | Implementación | Se autoriza con `AUTORIZO IMPLEMENTACIÓN` |

**Regla de oro:** sin G1–G4 aprobadas no se escribe código. G5 se abre fuera del análisis, ya en F3.

### Herramientas por fase
- **F0–F2:** usa `/pca-inicio` (o `prompts/00_inicio_analisis_diseno.md`). Genera backlog, modelo de datos, arquitectura y plan de sprints. No escribe código.
- **F1–F2 (detalle):** `prompts/workflow_01_levantamiento_ia.md` sigue disponible como guía de entrevista y sprints.
- **F5:** usa el prompt `prompts/workflow_02_extraccion_componentes.md`.

---

## 2. Protocolo de Sesión (checklist guiado)

### Al INICIAR cada sesión
1. Leer `AGENTS.md` (este archivo) y `docs/estado_proyecto.md`.
2. Si estás en **F0–F2**, ejecutar `/pca-inicio` y continuar desde el bloque pendiente.
3. Declarar la fase actual, la puerta pendiente y el próximo paso.
4. Si estás en **F3–F4**, elegir **un solo** ticket del tablero (`docs/plantilla_ticket.md` como formato).
5. Revisar las **convenciones aplicables** del ticket en `docs/convenciones.md`.

### Durante el trabajo
1. En **F0–F2** solo se escribe documentación dentro de `docs/`. No se programa.
2. Trabajar en **micro-tareas** (una unidad verificable a la vez).
3. Respetar `docs/convenciones.md` y las anotaciones `@kind/@limit/@contract`.
4. Si hay ambigüedad o falta un caso límite, la IA debe **detenerse y preguntar**.
5. Crear una rama de trabajo según `docs/git.md` antes de programar.

### Al CERRAR cada sesión
1. Verificar el ticket contra su *Definition of Done*.
2. Actualizar `docs/estado_proyecto.md` (fase, puerta, ticket, próximo paso).
3. En **F0–F2**, registrar la pregunta actual, las decisiones y los bloqueos.
4. Registrar en `docs/cicatrices_guerra.md` cualquier error resuelto.
5. Proponer el mensaje de commit (la IA **no** hace commit sola). Ver `docs/git.md`.

---

## 3. Reglas Inquebrantables de la Sesión
- **Puertas de análisis:** Tienes PROHIBIDO escribir código hasta que G1–G4 estén aprobadas y el alumno haya escrito `AUTORIZO IMPLEMENTACIÓN`. En F0–F2 solo se produce documentación en `docs/`.
- **Bloqueo de Build:** si `docs/estado_proyecto.md` no existe o muestra G1–G4 pendientes/G5 bloqueada, el agente Build debe negarse a escribir código y pedir `/pca-inicio`.
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
| Vas a iniciar o continuar el análisis y diseño (F0–F2) | `prompts/00_inicio_analisis_diseno.md` + `docs/estado_proyecto.md` |
| Vas a definir requisitos, alcance o casos límite | `docs/backlog_requisitos.md` |
| Vas a definir entidades, relaciones o validaciones | `docs/modelo_datos.md` |
| Vas a definir componentes, contratos, stack o riesgos | `docs/arquitectura.md` |
| Vas a planificar sprints o crear tickets | `docs/plan_sprints.md` + `docs/tickets/README.md` |
| Vas a modificar el diseño visual o CSS | `docs/reglas_ui.md` (si existe) |
| Vas a interactuar con la Base de Datos | `docs/reglas_backend.md` (si existe) |
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

> **Instrucción de Inicialización:** Cuando el análisis llegue al bloque **B5** (requisitos no funcionales y stack) y el Stack Tecnológico aún diga "Por Definir", tu primera acción es preguntar: "¿Qué stack tecnológico vamos a utilizar (Frontend, Backend, Base de Datos, Estilos)?" y registrarlo en `docs/estado_proyecto.md` y `docs/arquitectura.md`.

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
| `docs/estado_proyecto.md` | Tablero de control: fase, puertas, pregunta actual, sprints y tickets. Motor anti-amnesia. |
| `docs/backlog_requisitos.md` | Visión, usuarios, alcance, historias, requisitos, edge cases y trazabilidad. |
| `docs/modelo_datos.md` | Entidades, atributos, relaciones, validaciones y ERD. |
| `docs/arquitectura.md` | Componentes, contratos, flujos, stack, ADRs, riesgos y pruebas. |
| `docs/plan_sprints.md` | Sprints, tickets, dependencias, Definition of Ready y Definition of Done. |
| `docs/tickets/README.md` | Convención y ciclo de vida de los tickets. |
| `docs/convenciones.md` | Reglas de nomenclatura, estilo y buenas prácticas (asignables a tickets). |
| `docs/git.md` | Estrategia de ramas, commits y flujo de versionado. |
| `docs/plantilla_ticket.md` | Formato estándar para definir y ejecutar tickets. |
| `docs/cicatrices_guerra.md` | Registro de errores y soluciones (Learning Loop). |
| `docs/sistema_anotaciones.md` | Diccionario de anotaciones PCA y cómo usarlas. |
| `tools/pca_annotator.py` | CLI: inyecta anotaciones y genera el grafo de impacto. |
| `tools/README.md` | Guía del anotador y cómo agregar lenguajes. |
| `prompts/00_inicio_analisis_diseno.md` | Prompt de análisis y diseño F0–F2. No escribe código. |
| `prompts/workflow_01_levantamiento_ia.md` | Prompt para iniciar F1 (levantamiento + sprints). |
| `prompts/workflow_02_extraccion_componentes.md` | Prompt para iniciar F5 (extracción de componentes). |
| `.opencode/commands/pca-inicio.md` | Comando `/pca-inicio` para iniciar el análisis. |
| `.opencode/agents/pca-analista.md` | Agente de solo documentación: no puede editar código. |
