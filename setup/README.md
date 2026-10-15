# Setup PCA — Configura tu proyecto

Este es el **kit de configuración** para trabajar tu proyecto con la metodología PCA (Por qué, Cómo, A qué). Cópialo a la raíz de tu proyecto antes de empezar a programar.

---

## Qué contiene

```
setup/
├── AGENTS.md                 → Reglas + flujo de fases (el archivo que lee tu IA)
├── README.md                 → Este archivo
├── docs/
│   ├── estado_proyecto.md    → Tablero anti-amnesia (fase, sprints, tickets)
│   ├── convenciones.md       → Reglas de código asignables a tickets
│   ├── sistema_anotaciones.md → Diccionario de anotaciones y cómo usarlas
│   ├── git.md                → Ramas, commits y flujo de versionado
│   ├── plantilla_ticket.md   → Formato estándar de tickets
│   └── cicatrices_guerra.md  → Registro de errores y soluciones
├── prompts/
│   ├── workflow_01_levantamiento_ia.md      → Inicia la F1 (levantamiento + sprints)
│   └── workflow_02_extraccion_componentes.md → Inicia la F5 (extracción de componentes)
└── tools/
    ├── pca_annotator.py      → Inyecta anotaciones y genera el grafo de impacto
    ├── pca.config.json       → Manifiesto de archivos + lenguajes soportados
    └── README.md             → Guía del anotador y cómo agregar lenguajes
```

---

## Cómo usarlo

1. **Copia** el contenido de `setup/` a la raíz de tu proyecto.
   Para que tu IA lo encuentre, `AGENTS.md` y la carpeta `docs/` deben quedar en la raíz.

2. **Completa la Fase 0 (Setup):** define tu stack tecnológico y anótalo en `docs/estado_proyecto.md` y en `AGENTS.md`.

3. **Arranca la IA** con este mensaje:

   > "Lee el archivo `AGENTS.md` completo y el estado actual en `docs/estado_proyecto.md`. Dime en qué fase estamos y cuál es el siguiente paso."

4. **Inicia la Fase 1 (Levantamiento):** pega el contenido de `prompts/workflow_01_levantamiento_ia.md` en tu IA y descríbele tu idea.

5. **Sigue el flujo:** F0 Setup → F1 Levantamiento → F2 Sprints → F3 Ejecución → F4 Validación → F5 Cierre. La IA **no avanza de fase sin tu aprobación**.

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

- **Nada de Vibe Coding.** Método PCA antes de programar.
- **Una micro-tarea a la vez.** Sin código "por si acaso".
- **Sin secretos en el código.** Usa `.env` (ver `docs/git.md`).
- **Todo con ticket.** No se programa nada sin ticket.
- **Anota y consulta impacto.** Antes de tocar un archivo, `impact <id>`; al crearlo, agrégalo al manifiesto.
- **Actualiza tu estado.** Al cerrar cada sesión, actualiza `docs/estado_proyecto.md`.
