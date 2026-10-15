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

# 4. Validar límites y relaciones
python tools/pca_annotator.py check

# 5. Ver el impacto de cambiar un archivo
python tools/pca_annotator.py impact auth.login --transitive
```

Todos los comandos aceptan `--json` (antes del subcomando) para consumo por la IA:

```bash
python tools/pca_annotator.py --json check
```

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
      "contract": "cli: annotate|graph|impact|check",
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
| `annotate [--dry-run] [--backup]` | Inyecta/actualiza el bloque de anotación. Idempotente. |
| `graph [--out NOMBRE]` | Genera `NOMBRE.json` y `NOMBRE.mmd`. |
| `impact <id> [--transitive]` | Archivos que dependen de ese `id`. |
| `check` | Reporta sobre-límite, FK huérfanas, sin anotación y duplicados. |

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

Para una **etiqueta nueva** (no un lenguaje), sigue la sección "Cómo extender el vocabulario" de [`docs/sistema_anotaciones.md`](../docs/sistema_anotaciones.md): documéntala en el diccionario y enséñale a leerla al parser (`parse_annotations` / `_assign`).
