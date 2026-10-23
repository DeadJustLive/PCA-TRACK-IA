#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @pca:start
# @id(tools.pca_core)
# @kind(service)
# @limit(lines: 430)
# @contract(core: load_config, annotate_file, build_graph, compute_impact, find_drift)
# @relates(tools.pca_annotator)
# @relates(tools.pca_selftest)
# @desc(Núcleo puro del anotador PCA: manifiesto, bloques, grafo e impacto sin CLI)
# @pca:end

"""pca_core.py — Núcleo de la herramienta PCA (sin dependencias de la CLI).

Funciones puras para cargar el manifiesto, inyectar bloques de anotación,
construir el grafo de impacto y detectar deriva entre `pca.config.json` y los
archivos. La CLI vive en `pca_annotator.py` y las pruebas doradas en
`pca_selftest.py`. Solo biblioteca estándar.

Ver `tools/README.md` y `docs/sistema_anotaciones.md`.
"""

import fnmatch
import json
import os
import re
from datetime import datetime
from pathlib import Path

MARKER_START = "@pca:start"
MARKER_END = "@pca:end"

DEFAULT_LANGUAGES = {
    ".py": {"line_prefix": "#"},
    ".sh": {"line_prefix": "#"},
    ".rb": {"line_prefix": "#"},
    ".yml": {"line_prefix": "#"},
    ".yaml": {"line_prefix": "#"},
    ".toml": {"line_prefix": "#"},
    ".js": {"line_prefix": "//"},
    ".jsx": {"line_prefix": "//"},
    ".ts": {"line_prefix": "//"},
    ".tsx": {"line_prefix": "//"},
    ".java": {"line_prefix": "//"},
    ".c": {"line_prefix": "//"},
    ".cpp": {"line_prefix": "//"},
    ".h": {"line_prefix": "//"},
    ".cs": {"line_prefix": "//"},
    ".go": {"line_prefix": "//"},
    ".rs": {"line_prefix": "//"},
    ".kt": {"line_prefix": "//"},
    ".kts": {"line_prefix": "//"},
    ".swift": {"line_prefix": "//"},
    ".css": {"block_open": "/*", "block_close": "*/"},
    ".scss": {"block_open": "/*", "block_close": "*/"},
    ".less": {"block_open": "/*", "block_close": "*/"},
    ".html": {"block_open": "<!--", "block_close": "-->"},
    ".htm": {"block_open": "<!--", "block_close": "-->"},
    ".xml": {"block_open": "<!--", "block_close": "-->"},
    ".svg": {"block_open": "<!--", "block_close": "-->"},
    ".md": {"block_open": "<!--", "block_close": "-->"},
    ".markdown": {"block_open": "<!--", "block_close": "-->"},
    ".sql": {"line_prefix": "--"},
}

TAG_RE = re.compile(r"@([a-zA-Z][\w-]*)\(([^)]*)\)")


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    config_dir = Path(config_path).resolve().parent
    base_dir = (config_dir / config.get("base_dir", ".")).resolve()
    config["_config_dir"] = config_dir
    config["_base_dir"] = base_dir
    return config


def build_languages(config):
    languages = dict(DEFAULT_LANGUAGES)
    for ext, spec in (config.get("languages") or {}).items():
        key = ext if ext.startswith(".") else "." + ext
        languages[key.lower()] = spec
    return languages


def rel_posix(path, base):
    try:
        return Path(path).resolve().relative_to(base).as_posix()
    except ValueError:
        return Path(os.path.relpath(path, base)).as_posix()


def match_any(rel, patterns):
    rel = rel.replace(os.sep, "/")
    name = rel.rsplit("/", 1)[-1]
    for pattern in patterns:
        clean = pattern[3:] if pattern.startswith("**/") else pattern
        if fnmatch.fnmatch(rel, clean) or fnmatch.fnmatch(name, clean):
            return True
    return False


def collect_files(config, languages):
    base = config["_base_dir"]
    manifest = config.get("files") or []

    # El manifiesto es la fuente de verdad. Solo se escanean roots si no hay files.
    if manifest:
        found = {}
        for entry in manifest:
            path = (base / entry["path"]).resolve()
            if path.exists():
                found[str(path)] = path
        return [found[key] for key in sorted(found)]

    include = config.get("include") or ["**/*"]
    exclude = config.get("exclude") or []
    found = {}

    for root in config.get("roots", []):
        root_path = (base / root).resolve()
        if not root_path.exists():
            continue
        for path in root_path.rglob("*"):
            if not path.is_file():
                continue
            rel = rel_posix(path, base)
            if match_any(rel, exclude):
                continue
            if path.suffix.lower() not in languages:
                continue
            if include and not match_any(rel, include):
                continue
            found[str(path)] = path

    return [found[key] for key in sorted(found)]


def render_block(entry, languages):
    ext = Path(entry["path"]).suffix.lower()
    lang = languages.get(ext)
    if not lang:
        raise ValueError(f"Lenguaje no soportado para {entry['path']}")

    lines = [MARKER_START, f"@id({entry['id']})", f"@kind({entry.get('kind', 'unknown')})"]
    if entry.get("limit"):
        lines.append(f"@limit(lines: {entry['limit']})")
    if entry.get("contract"):
        lines.append(f"@contract({entry['contract']})")
    for related in entry.get("relates", []):
        lines.append(f"@relates({related})")
    if entry.get("desc"):
        lines.append(f"@desc({entry['desc']})")
    lines.append(MARKER_END)

    if "line_prefix" in lang:
        prefix = lang["line_prefix"]
        return [f"{prefix} {line}" for line in lines]

    inner = " * " if lang["block_open"] == "/*" else ""
    rendered = [f"{lang['block_open']} {MARKER_START}"]
    rendered += [f"{inner}{line}" for line in lines[1:-1]]
    rendered.append(f"{inner}{MARKER_END} {lang['block_close']}")
    return rendered


def find_block_span(lines):
    start = end = None
    for index, line in enumerate(lines):
        if MARKER_START in line and start is None:
            start = index
        if MARKER_END in line and start is not None:
            end = index
            break
    return (start, end) if start is not None and end is not None else None


def insertion_index(lines, ext):
    index = 0
    if ext in (".py", ".sh", ".rb"):
        while index < len(lines) and (
            lines[index].startswith("#!") or "coding" in lines[index][:40]
        ):
            index += 1
    elif ext in (".md", ".markdown"):
        if lines and lines[0].strip() == "---":
            index = 1
            while index < len(lines) and lines[index].strip() != "---":
                index += 1
            index += 1
    elif ext in (".html", ".htm", ".xml", ".svg"):
        if lines and "<!DOCTYPE" in lines[0].upper():
            index = 1
    return index


def detect_eol(text):
    return "\r\n" if "\r\n" in text else "\n"


def annotate_file(path, entry, languages, dry_run=False, backup=False):
    ext = Path(path).suffix.lower()
    if ext not in languages:
        return f"OMITIDO (lenguaje no soportado): {entry['path']}"

    # newline="" conserva los finales de línea originales (LF o CRLF) al leer y escribir.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        original = handle.read()
    eol = detect_eol(original)
    original_lines = original.splitlines()

    body = list(original_lines)
    span = find_block_span(body)
    if span:
        del body[span[0]:span[1] + 1]
        insert_at = span[0]
        while insert_at > 0 and body[insert_at - 1].strip() == "":
            del body[insert_at - 1]
            insert_at -= 1
    else:
        insert_at = insertion_index(body, ext)

    block = render_block(entry, languages)
    new_lines = body[:insert_at] + block + body[insert_at:]
    new_text = eol.join(new_lines) + eol

    if dry_run:
        return f"DRY-RUN: {entry['path']} ({len(block)} líneas de anotación)"

    if backup:
        with open(path.with_suffix(path.suffix + ".bak"), "w", encoding="utf-8", newline="") as handle:
            handle.write(original)
    if new_text != original:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(new_text)
    return f"ANOTADO: {entry['path']}"


def parse_annotations(text):
    meta = {"id": None, "kind": None, "limit": None,
            "contract": None, "desc": None, "relates": []}

    compact = re.search(r"@file\((.*?)\)", text, re.S)
    if compact:
        for key, value in re.findall(r"(\w+)\s*=\s*([^,]+)", compact.group(1)):
            _assign(meta, key, value.strip())

    for tag, value in TAG_RE.findall(text):
        _assign(meta, tag.lower(), value.strip())

    return meta


def _assign(meta, key, value):
    key = key.lower()
    if key == "id":
        meta["id"] = value
    elif key == "kind":
        meta["kind"] = value
    elif key == "limit":
        match = re.search(r"(\d+)", value)
        if match:
            meta["limit"] = int(match.group(1))
    elif key == "contract":
        meta["contract"] = value
    elif key == "desc":
        meta["desc"] = value
    elif key in ("relates", "relate", "fk"):
        # Acumula las relaciones en lugar de sobrescribirlas: el diccionario permite
        # repetir @relates(...) una vez por relación además de la forma agrupada por comas.
        items = [item.strip() for item in value.split(",") if item.strip()]
        meta["relates"] = meta["relates"] + [i for i in items if i not in meta["relates"]]


def extract_block_text(text):
    start = text.find(MARKER_START)
    end = text.find(MARKER_END)
    if start == -1 or end == -1:
        return ""
    return text[start:end + len(MARKER_END)]


def synth_id(path, base):
    rel = rel_posix(path, base)
    if rel.endswith(Path(rel).suffix):
        rel = rel[: -len(Path(rel).suffix)]
    return rel.replace("/", ".")


def block_line_count(block_text):
    return len(block_text.splitlines()) if block_text else 0


def find_drift(config, languages):
    """Compara el bloque de cada archivo del manifiesto con el que `annotate` escribiría.

    Devuelve una lista de {path, reason} con reason en
    {missing_file, missing_block, stale_block}. Solo lectura: nunca escribe.
    """
    base = config["_base_dir"]
    drifted = []
    for entry in config.get("files", []):
        path = (base / entry["path"]).resolve()
        if not path.exists():
            drifted.append({"path": entry["path"], "reason": "missing_file"})
            continue
        if Path(path).suffix.lower() not in languages:
            continue
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        span = find_block_span(lines)
        if span is None:
            drifted.append({"path": entry["path"], "reason": "missing_block"})
            continue
        actual = "\n".join(line.rstrip() for line in lines[span[0]:span[1] + 1])
        expected = "\n".join(line.rstrip() for line in render_block(entry, languages))
        if actual != expected:
            drifted.append({"path": entry["path"], "reason": "stale_block"})
    return drifted


def build_graph(config, languages):
    base = config["_base_dir"]
    nodes, edges = [], []
    issues = {"dangling": [], "over_limit": [], "missing_annotations": [], "duplicate_ids": []}
    seen_ids = {}

    for path in collect_files(config, languages):
        text = path.read_text(encoding="utf-8", errors="replace")
        block = extract_block_text(text)
        meta = parse_annotations(block) if block else {"relates": []}
        line_count = len(text.splitlines())
        # El @limit es un freno de código, no del propio bloque de anotación (ver KB-003).
        code_lines = max(line_count - block_line_count(block), 0)

        node_id = meta.get("id")
        if not node_id:
            node_id = synth_id(path, base)
            issues["missing_annotations"].append(rel_posix(path, base))

        if node_id in seen_ids:
            issues["duplicate_ids"].append({"id": node_id, "paths": [seen_ids[node_id], rel_posix(path, base)]})
        seen_ids[node_id] = rel_posix(path, base)

        limit = meta.get("limit")
        over = bool(limit and code_lines > limit)
        if over:
            issues["over_limit"].append({"id": node_id, "path": rel_posix(path, base), "lines": code_lines, "limit": limit})

        node = {
            "id": node_id,
            "path": rel_posix(path, base),
            "kind": meta.get("kind"),
            "limit": limit,
            "lines": code_lines,
            "total_lines": line_count,
            "over_limit": over,
            "contract": meta.get("contract"),
            "desc": meta.get("desc"),
            "relations": meta.get("relates", []),
        }
        nodes.append(node)
        for related in meta.get("relates", []):
            edges.append({"from": node_id, "to": related, "type": "relates"})

    valid_ids = {node["id"] for node in nodes}
    issues["dangling"] = [edge for edge in edges if edge["to"] not in valid_ids]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "nodes": sorted(nodes, key=lambda n: n["id"]),
        "edges": edges,
        "issues": issues,
    }


def to_mermaid(graph):
    lines = ["graph LR"]
    for node in graph["nodes"]:
        label = node["id"].replace(".", "_")
        kind = node.get("kind") or "?"
        lines.append(f'    {label}["{node["id"]} ({kind})"]')
    for edge in graph["edges"]:
        a = edge["from"].replace(".", "_")
        b = edge["to"].replace(".", "_")
        lines.append(f"    {a} --> {b}")
    return "\n".join(lines) + "\n"


def compute_impact(graph, target, transitive=False):
    """Nodos que declaran depender de `target` (aristas from → to = dependiente → dependencia)."""
    direct = sorted({edge["from"] for edge in graph["edges"] if edge["to"] == target})
    if not transitive:
        return direct
    result, queue = set(direct), list(direct)
    while queue:
        current = queue.pop(0)
        for edge in graph["edges"]:
            if edge["to"] == current and edge["from"] not in result:
                result.add(edge["from"])
                queue.append(edge["from"])
    return sorted(result)
