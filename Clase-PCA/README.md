# Setup PCA — Configura tu proyecto

Este es el **kit de configuración** para trabajar tu proyecto con la metodología PCA (Por qué, Cómo, A qué). Cópialo a la raíz de tu proyecto antes de empezar a programar.

> **Regla de oro:** primero se analiza y diseña; después se programa. El comando `/pca-inicio` te guía por las puertas G1–G4 y bloquea la implementación hasta que la autorices explícitamente.

---

## Qué contiene

```
setup/
├── AGENTS.md                 → Reglas + flujo de fases (la IA lo lee automáticamente)
├── README.md                 → Este archivo
├── .opencode/
│   ├── agents/pca-analista.md      → Agente de solo documentación (no edita código)
│   └── commands/pca-inicio.md      → Comando /pca-inicio
├── docs/
│   ├── estado_proyecto.md    → Tablero anti-amnesia (fase, puertas, tickets)
│   ├── backlog_requisitos.md → Visión, requisitos, edge cases y trazabilidad
│   ├── modelo_datos.md       → Entidades, relaciones, validaciones y ERD
│   ├── arquitectura.md       → Componentes, contratos, ADRs y riesgos
│   ├── plan_sprints.md       → Sprints, tickets, DoR y DoD
│   ├── tickets/README.md     → Convención y ciclo de vida de tickets
│   ├── convenciones.md       → Reglas de código asignables a tickets
│   ├── sistema_anotaciones.md → Diccionario de anotaciones y cómo usarlas
│   ├── git.md                → Ramas, commits y flujo de versionado
│   ├── plantilla_ticket.md   → Formato estándar de tickets
│   └── cicatrices_guerra.md  → Registro de errores y soluciones
├── prompts/
│   ├── 00_inicio_analisis_diseno.md      → Entrevista de análisis y diseño (F0–F2)
│   ├── workflow_01_levantamiento_ia.md   → Apoyo para F1 (levantamiento + sprints)
│   └── workflow_02_extraccion_componentes.md → Apoyo para F5 (extracción)
└── tools/
    ├── pca_annotator.py      → Inyecta anotaciones y genera el grafo de impacto
    ├── pca.config.json       → Manifiesto de archivos + lenguajes soportados
    └── README.md             → Guía del anotador y cómo agregar lenguajes
```

---

## Cómo usarlo

1. **Copia el contenido** de `setup/` a la raíz de tu proyecto. No copies la carpeta `setup/`: `AGENTS.md`, `docs/`, `prompts/` y `.opencode/` deben quedar en la raíz. Si tu proyecto ya tiene una carpeta `.opencode/`, **fusiona** el contenido; no la reemplaces.
2. **Abre OpenCode** en la raíz del proyecto.
3. **Inicia el análisis** con:

   > `/pca-inicio`

   El comando activa el agente `pca-analista`, que **solo puede escribir en `docs/`**. No puede crear código.
4. **Responde la entrevista.** El agente elige modo express o completo, hace una pregunta a la vez y genera:
   - `docs/backlog_requisitos.md`
   - `docs/modelo_datos.md`
   - `docs/arquitectura.md`
   - `docs/plan_sprints.md`
   - `docs/tickets/` (T01, T02, …)
5. **Aprueba las puertas.** Al terminar G4, el agente se detiene y te entrega el handoff. Para implementar, cambia al agente **Build** y escribe:

   > `AUTORIZO IMPLEMENTACIÓN`

6. **Sigue el flujo:** F0 Setup → F1 Levantamiento → F2 Sprints → F3 Ejecución → F4 Validación → F5 Cierre.

---

## El flujo de análisis y diseño

| Puerta | Qué se aprueba | Documento | La IA no puede... |
| :--- | :--- | :--- | :--- |
| **G1** | Problema, usuarios, MVP y fuera de alcance | `backlog_requisitos.md` | Programar |
| **G2** | Requisitos, RNF, edge cases y criterios | `backlog_requisitos.md` | Crear tickets |
| **G3** | Modelo de datos, arquitectura y riesgos | `modelo_datos.md` + `arquitectura.md` | Saltar la defensa del diseño |
| **G4** | Sprints, tickets y DoR | `plan_sprints.md` + `tickets/` | Implementar |
| **G5** | Implementación | Autorización explícita | Empezar sin `AUTORIZO IMPLEMENTACIÓN` |

Si el alumno pide código antes de G5, el agente responde con un bloqueo y registra la petición como requisito.

---

## Si no usas OpenCode

El prompt es portable. Pega `prompts/00_inicio_analisis_diseno.md` en ChatGPT, Claude o Gemini y adjunta:

- `AGENTS.md`
- `docs/estado_proyecto.md`

El agente de chat no podrá escribir archivos, pero puede hacer la entrevista y darte el contenido de cada documento para que lo guardes.

---

## Herramientas

El kit incluye un anotador de código que genera un **grafo de impacto** (relevante para no romper nada al cambiar un archivo). Requiere solo Python 3.9+.

```bash
python tools/pca_annotator.py annotate --dry-run   # previsualiza
python tools/pca_annotator.py annotate             # inyecta anotaciones
python tools/pca_annotator.py graph                # genera grafo.json + grafo.mmd
python tools/pca_annotator.py check                # valida límites y relaciones
python tools/pca_annotator.py impact auth.login --transitive   # ¿qué depende de este archivo?
```

- El vocabulario de etiquetas está en `docs/sistema_anotaciones.md`.
- Cómo soportar más lenguajes, en `tools/README.md`.

---

## Reglas rápidas

- **Sin G1–G4 no hay código.** El análisis y el diseño se aprueban antes de implementar.
- **G5 se autoriza explícitamente.** La frase `AUTORIZO IMPLEMENTACIÓN` abre la fase de código.
- **Una pregunta a la vez.** No se avanza con respuestas ambiguas.
- **No se inventan requisitos.** Si falta información, se pregunta.
- **Nada de Vibe Coding.** Método PCA antes de programar.
- **Una micro-tarea a la vez.** Sin código "por si acaso".
- **Sin secretos en el código.** Usa `.env` (ver `docs/git.md`).
- **Todo con ticket.** No se programa nada sin ticket.
- **Anota y consulta impacto.** Antes de tocar un archivo, `impact <id>`; al crearlo, agrégalo al manifiesto.
- **Actualiza tu estado.** Al cerrar cada sesión, actualiza `docs/estado_proyecto.md`.

---

## Problemas comunes

| Síntoma | Causa probable | Solución |
| :--- | :--- | :--- |
| No aparece `/pca-inicio` | `.opencode/commands/pca-inicio.md` no está en la raíz | Copia el contenido de `setup/` en la raíz y vuelve a abrir OpenCode. |
| La IA intenta programar | Estás en el agente Build | Ejecuta `/pca-inicio` para usar `pca-analista`. |
| La IA no ve el estado | Falta `docs/estado_proyecto.md` | Cópialo a `docs/` y vuelve a ejecutar `/pca-inicio`. |
| Copiaste la carpeta `setup/` | Las rutas quedaron dentro de `setup/` | Mueve el contenido a la raíz del proyecto. |
| Quieres cambiar de modo | Express o completo | Pídeselo al agente; puede cambiar si el proyecto crece. |
| El agente se niega a escribir código | Es correcto: está en F0–F2 | Termina G4 y cambia al agente Build. |
