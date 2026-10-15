<!-- @pca:start
@id(docs.sistema_anotaciones)
@kind(doc)
@relates(tools.pca_annotator)
@desc(Diccionario de anotaciones PCA y cómo usarlas)
@pca:end -->
# Sistema de Anotaciones PCA

> **Instrucción para la IA:** Usa estas etiquetas al crear o modificar archivos. El programa `tools/pca_annotator.py` las lee para construir el grafo de impacto. Cada anotación tiene un **objetivo** claro; no inventes etiquetas nuevas sin registrarlas aquí.

Este documento es el **diccionario** de las anotaciones del método PCA: qué significa cada una, cómo se escribe y quién la consume. El sistema cumple tres funciones:

1. **Documentar** cada archivo crítico (qué es y para qué sirve).
2. **Relacionar** archivos entre sí mediante etiquetas tipo **clave foránea (FK)**.
3. **Calcular impacto**: al cambiar un archivo, saber qué otros dependen de él.

---

## 1. Formato del bloque

Un bloque de anotación va en la **cabecera** del archivo, delimitado por marcadores y con **una etiqueta por línea** (formato canónico):

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

En cada lenguaje se comenta según su sintaxis:

| Archivo | Sintaxis | Ejemplo |
| :--- | :--- | :--- |
| `.py` `.sh` `.yml` | `#` | `# @id(auth.login)` |
| `.js` `.ts` `.tsx` | `//` | `// @id(auth.login)` |
| `.css` `.scss` | `/* ... */` | `/* @pca:start ... @pca:end */` |
| `.html` `.xml` `.md` | `<!-- ... -->` | `<!-- @pca:start ... @pca:end -->` |
| `.sql` | `--` | `-- @id(auth.login)` |

El programa inserta y ordena las etiquetas automáticamente con `annotate`. También acepta la forma compacta `@file(id=..., kind=..., limit=..., contract=..., relates=..., desc=...)` por compatibilidad.

---

## 2. Diccionario de anotaciones

### `@pca:start` / `@pca:end`
- **Objetivo:** delimitar el bloque de anotaciones para que el programa lo detecte y lo reemplace sin duplicar.
- **Sintaxis:** marcadores sin valor.
- **Dónde va:** abren y cierran el bloque, en la cabecera del archivo.
- **Consume:** el programa (`pca_annotator.py`).
- **Regla:** nunca editar el bloque a mano si usas `annotate`; el programa lo regenera.

### `@id(...)`
- **Objetivo:** identificar de forma única el nodo (equivalente a la **clave primaria / PK**).
- **Sintaxis:** `@id(dominio.accion)`, sin espacios. Ej: `auth.login`, `user.model`.
- **Dónde va:** dentro del bloque, una sola vez por archivo.
- **Consume:** el programa (nodo del grafo) y la IA (para `impact`).
- **Regla:** debe ser único en todo el proyecto. Convención sugerida: `carpeta.archivo`.

### `@kind(...)`
- **Objetivo:** declarar el tipo de archivo para entender su rol.
- **Sintaxis:** `@kind(component)` — valores típicos: `component`, `service`, `hook`, `util`, `model`, `view`, `doc`, `config`, `prompt`.
- **Dónde va:** dentro del bloque.
- **Consume:** humanos, la IA y el programa (etiqueta del nodo).
- **Regla:** si ningún valor calza, inventa uno consistente y regístralo aquí.

### `@limit(lines: X)`
- **Objetivo:** fijar el máximo de líneas permitido (freno anti-bloat).
- **Sintaxis:** `@limit(lines: 120)`.
- **Dónde va:** dentro del bloque.
- **Consume:** el programa (`check` avisa si se supera) y la IA.
- **Regla (CONV-TIP-04):** si el archivo supera su límite, refactoriza antes de seguir.

### `@contract(...)`
- **Objetivo:** declarar el contrato público del archivo (interfaz, props, endpoints).
- **Sintaxis:** `@contract(props: email, password)` o `@contract(cli: annotate|graph)`.
- **Dónde va:** dentro del bloque.
- **Consume:** humanos y la IA (para respetar interfaces).
- **Regla:** si cambia el contrato, actualízalo en la misma tarea.

### `@relates(...)`
- **Objetivo:** declarar relaciones con otros nodos por su `@id` (equivalente a **clave foránea / FK**). Genera las aristas del grafo.
- **Sintaxis:** `@relates(id1, id2)` — varios separados por coma.
- **Dónde va:** dentro del bloque; puede repetirse una vez por relación o agruparse separando por comas.
- **Consume:** el programa (aristas + `impact`) y la IA (impacto).
- **Regla:** el destino debe existir (un `@id` real); si no, `check` lo reporta como **FK huérfana**.

### `@desc(...)`
- **Objetivo:** descripción legible en una línea de qué hace el archivo.
- **Sintaxis:** `@desc(Formulario de inicio de sesión)`.
- **Dónde va:** dentro del bloque.
- **Consume:** humanos y la IA.
- **Regla:** una sola línea, en español, sin punto final.

### `@learn-error ...` (Learning Loop)
- **Objetivo:** registrar errores resueltos para no repetirlos. Vive en `docs/cicatrices_guerra.md`, no en el bloque de cabecera.
- **Sintaxis:** `// @learn-error id=1 input="x" expected="y" actual="z" fix="solución"`.
- **Dónde va:** en el registro de cicatrices.
- **Consume:** la IA antes de proponer soluciones.
- **Regla:** cada bug complejo resuelto deja una cicatriz.

---

## 3. Cómo se relaciona con el grafo (lo "tipo SQL")

| Concepto SQL | Anotación PCA | Efecto |
| :--- | :--- | :--- |
| Clave primaria (PK) | `@id(...)` | Nodo del grafo |
| Clave foránea (FK) | `@relates(...)` | Arista entre nodos |
| `JOIN` / consulta | `pca_annotator.py impact <id>` | Lista de dependientes |
| Integridad referencial | `check` → FK huérfanas | Detecta relaciones rotas |

Flujo típico antes de tocar un archivo:

```
python tools/pca_annotator.py impact auth.login --transitive
```

Devuelve todos los archivos que dependen (directa o indirectamente) de ese `id`.

---

## 4. Cómo extender el vocabulario

Para agregar una anotación nueva:

1. **Defínela aquí** con su objetivo, sintaxis, dónde va, quién la consume y regla (copia el formato de arriba).
2. **Enséñale a leerla al programa:** agrega su caso en `parse_annotations` / `_assign` de `tools/pca_annotator.py`.
3. **Úsala** en los bloques y valida con `python tools/pca_annotator.py check`.

> Si solo necesitas **soportar otro lenguaje** (no una etiqueta nueva), agrega su extensión al mapa `LANGUAGES` del código o a la clave `"languages"` de `pca.config.json`. Ver `tools/README.md`.
