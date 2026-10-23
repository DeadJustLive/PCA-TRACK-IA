<!-- @pca:start
@id(tools.readme)
@kind(doc)
@relates(tools.pca_annotator)
@desc(Guía de uso del anotador PCA y cómo agregar lenguajes)
@pca:end -->
# pca_annotator — Anotador y grafo de impacto

Herramienta de línea de comandos (Python 3.9+, **solo biblioteca estándar**) que:

1. **Inyecta anotaciones** en los archivos declarados en el manifiesto.
2. **Construye un grafo** con la información relevante de cada archivo y sus relaciones.
3. **Calcula el impacto** de un cambio a partir de las relaciones tipo clave foránea (`@relates`).

El vocabulario de anotaciones se documenta en [`docs/sistema_anotaciones.md`](../docs/sistema_anotaciones.md).

---

## Uso rápido

```bash
# 1. Ver qué se anotaría (sin escribir nada)
python tools/pca_annotator.py annotate --dry-run

# 2. Inyectar/actualizar las anotaciones
python tools/pca_annotator.py annotate --backup

# 3. Generar el grafo (grafo.json + grafo.mmd)
python tools/pca_annotator.py graph

# 4. Validar límites y relaciones (--strict sale con 1 ante problemas de integridad)
python tools/pca_annotator.py check
python tools/pca_annotator.py check --strict

# 5. Ver el impacto de cambiar un archivo
python tools/pca_annotator.py impact auth.login --transitive

# 6. Detectar deriva entre pca.config.json y los bloques (solo lectura; sale con 1 si hay deriva)
python tools/pca_annotator.py annotate --check-drift

# 7. Autoevaluación: pruebas doradas de la herramienta (regresión KB-004 incluida)
python tools/pca_annotator.py selftest
```

Todos los comandos aceptan `--json` (antes del subcomando) para consumo por la IA:

```bash
python tools/pca_annotator.py --json check
```

### Hook de integridad en Git

`tools/hooks/pre-commit` ejecuta `check --strict` antes de cada commit y **bloquea** si hay
FK huérfana, ID duplicado o archivo del manifiesto sin anotar (el sobre-límite es solo
advertencia). Activación, una sola vez por clon:

```bash
git config core.hooksPath tools/hooks
```

Escape puntual para un commit ya revisado: `git commit --no-verify`. Si `python3` no está
disponible, el hook no bloquea.

### Estructura de módulos

| Archivo | Responsabilidad |
| :--- | :--- |
| `pca_annotator.py` | CLI: argumentos, comandos, códigos de salida y `--json`. |
| `pca_core.py` | Núcleo puro: manifiesto, bloques, grafo, impacto y deriva (sin CLI). |
| `pca_selftest.py` | Pruebas doradas de todo lo anterior, con directorios temporales. |
| `hooks/pre-commit` | Hook versionado que cablea `check --strict` a Git. |

---

## El manifiesto `pca.config.json`

```json
{
  "base_dir": "..",
  "roots": ["docs", "tools"],
  "include": ["**/*.py", "**/*.md"],
  "exclude": ["**/grafo.*"],
  "files": [
    {
      "path": "tools/pca_annotator.py",
      "id": "tools.pca_annotator",
      "kind": "service",
      "limit": 500,
      "contract": "cli: annotate|graph|impact|check|selftest",
      "desc": "CLI para inyectar anotaciones PCA y generar el grafo de impacto",
      "relates": ["docs.sistema_anotaciones"]
    }
  ],
  "options": { "output_dir": "." },
  "languages": {}
}
```

| Clave | Descripción |
| :--- | :--- |
| `base_dir` | Carpeta base (relativa al manifiesto) para resolver `path` y `roots`. |
| `files` | **Fuente de verdad.** Lista de archivos a anotar y graficar. |
| `roots` / `include` / `exclude` | Solo se usan si `files` está vacío (modo escaneo libre). |
| `options.output_dir` | Dónde se escriben `grafo.json` y `grafo.mmd`. |
| `languages` | Extensiones o sobreescrituras de sintaxis (ver abajo). |

---

## Comandos

| Comando | Descripción |
| :--- | :--- |
| `annotate [--dry-run] [--backup] [--check-drift]` | Inyecta/actualiza el bloque de anotación (idempotente) o, con `--check-drift`, solo reporta bloques desfazados sin escribir (sale con 1). |
| `graph [--out NOMBRE]` | Genera `NOMBRE.json` y `NOMBRE.mmd`. |
| `impact <id> [--transitive]` | Archivos que dependen de ese `id` (sale con 1 si el `id` no existe). |
| `check [--strict]` | Reporta sobre-límite, FK huérfanas, sin anotación y duplicados; `--strict` sale con 1 ante problemas de integridad. |
| `selftest` | Ejecuta las pruebas doradas de la herramienta; sale con 1 si alguna falla. |

**Semántica del `@limit`:** cuenta solo **líneas de código** (el bloque de anotación no se
suma); es un freno al bloat del archivo, no a su cabecera.

---

## Cómo agregar soporte para más lenguajes

El mapa de lenguajes asocia una **extensión** con su sintaxis de comentario. Hay dos vías:

### Vía 1 — Sin tocar código (recomendada)

Agrega la extensión a la clave `"languages"` de `pca.config.json`:

```json
"languages": {
  ".go": { "line_prefix": "//" },
  ".sql": { "line_prefix": "--" },
  ".vue": { "block_open": "<!--", "block_close": "-->" }
}
```

- `line_prefix`: comenta cada línea (ej. `#`, `//`, `--`).
- `block_open` / `block_close`: comentario de bloque (ej. `/* */`, `<!-- -->`).

### Vía 2 — En el código

Agrega la entrada en el diccionario `LANGUAGES` de `pca_annotator.py` (misma estructura). Útil si quieres que venga de fábrica.

### Reglas de inserción

- **Python/Shell**: salta el `shebang` y la línea `coding`.
- **HTML/XML**: inserta después de `<!DOCTYPE>`.
- **Markdown**: inserta después del *front-matter* (`--- ... ---`).

Si tu lenguaje necesita otra regla especial, edita `insertion_index()` en el código.

### Validar

```bash
python tools/pca_annotator.py annotate --dry-run
python tools/pca_annotator.py check
```

---

## Agregar una anotación nueva

Para una **etiqueta nueva** (no un lenguaje), sigue la sección "Cómo extender el vocabulario" de [`docs/sistema_anotaciones.md`](../docs/sistema_anotaciones.md): documéntala en el diccionario y enséñale a leerla al parser (`parse_annotations` / `_assign`, hoy en `tools/pca_core.py`). Después de tocar el parser o el grafo, ejecuta `python tools/pca_annotator.py selftest` para confirmar que nada se rompió (ver cicatriz KB-004).
