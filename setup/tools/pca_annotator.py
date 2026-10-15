#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @pca:start
# @id(tools.pca_annotator)
# @kind(service)
# @limit(lines: 500)
# @contract(cli: annotate|graph|impact|check)
# @relates(docs.sistema_anotaciones)
# @relates(docs.convenciones)
# @desc(CLI para inyectar anotaciones PCA y generar el grafo de impacto del proyecto)
# @pca:end

"""pca_annotator.py — Anotador y grafo de impacto (metodología PCA).

Inyecta bloques de anotación en los archivos declarados en `pca.config.json`
y genera un grafo (JSON + Mermaid) con la información relevante de cada archivo
y sus relaciones, para evaluar el impacto de un cambio.

Solo usa la biblioteca estándar. Ver `tools/README.md` y
`docs/sistema_anotaciones.md`.
"""

import argparse
import fnmatch
import json
import os
import re
import sys
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


def annotate_file(path, entry, languages, dry_run=False, backup=False):
    ext = Path(path).suffix.lower()
    if ext not in languages:
        return f"OMITIDO (lenguaje no soportado): {entry['path']}"

    original = path.read_text(encoding="utf-8").splitlines()

    body = list(original)
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
    new_text = "\n".join(new_lines) + "\n"

    if dry_run:
        return f"DRY-RUN: {entry['path']} ({len(block)} líneas de anotación)"

    if backup:
        path.with_suffix(path.suffix + ".bak").write_text(
            "\n".join(original) + "\n", encoding="utf-8"
        )
    path.write_text(new_text, encoding="utf-8")
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
        meta["relates"] = [item.strip() for item in value.split(",") if item.strip()]


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

        node_id = meta.get("id")
        if not node_id:
            node_id = synth_id(path, base)
            issues["missing_annotations"].append(rel_posix(path, base))

        if node_id in seen_ids:
            issues["duplicate_ids"].append({"id": node_id, "paths": [seen_ids[node_id], rel_posix(path, base)]})
        seen_ids[node_id] = rel_posix(path, base)

        limit = meta.get("limit")
        over = bool(limit and line_count > limit)
        if over:
            issues["over_limit"].append({"id": node_id, "path": rel_posix(path, base), "lines": line_count, "limit": limit})

        node = {
            "id": node_id,
            "path": rel_posix(path, base),
            "kind": meta.get("kind"),
            "limit": limit,
            "lines": line_count,
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


def cmd_annotate(config, languages, args):
    results, skipped = [], []
    for entry in config.get("files", []):
        path = (config["_base_dir"] / entry["path"]).resolve()
        if not path.exists():
            skipped.append(entry["path"])
            continue
        results.append(annotate_file(path, entry, languages, args.dry_run, args.backup))
    payload = {"results": results, "dry_run": args.dry_run}
    if skipped:
        payload["skipped"] = skipped
    emit(results, args, payload)


def cmd_graph(config, languages, args):
    graph = build_graph(config, languages)
    out_dir = (config["_base_dir"] / config.get("options", {}).get("output_dir", ".")).resolve()
    out_name = args.out or "grafo"
    json_path = out_dir / f"{out_name}.json"
    mmd_path = out_dir / f"{out_name}.mmd"
    json_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    mmd_path.write_text(to_mermaid(graph), encoding="utf-8")
    emit(
        [
            f"Grafo generado: {json_path.name} ({len(graph['nodes'])} nodos, {len(graph['edges'])} relaciones)",
            f"Mermaid: {mmd_path.name}",
        ],
        args,
        graph,
    )


def cmd_impact(config, languages, args):
    graph = build_graph(config, languages)
    dependents = compute_impact(graph, args.id, args.transitive)
    if args.json:
        print(json.dumps({"id": args.id, "dependents": dependents}, indent=2, ensure_ascii=False))
    elif dependents:
        print(f"Archivos afectados por '{args.id}' ({len(dependents)}):")
        for item in dependents:
            print(f"  - {item}")
    else:
        print(f"Sin dependencias registradas para '{args.id}'.")


def cmd_check(config, languages, args):
    graph = build_graph(config, languages)
    issues = graph["issues"]
    report = {
        "over_limit": issues["over_limit"],
        "dangling": issues["dangling"],
        "missing_annotations": issues["missing_annotations"],
        "duplicate_ids": issues["duplicate_ids"],
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    print("== check ==")
    print(f"Nodos: {len(graph['nodes'])}  Relaciones: {len(graph['edges'])}")
    print(f"Sobre límite: {len(issues['over_limit'])}")
    for item in issues["over_limit"]:
        print(f"  - {item['path']}: {item['lines']} líneas (límite {item['limit']})")
    print(f"Relaciones rotas (FK huérfanas): {len(issues['dangling'])}")
    for edge in issues["dangling"]:
        print(f"  - {edge['from']} --> {edge['to']}")
    print(f"Archivos sin anotación: {len(issues['missing_annotations'])}")
    for path in issues["missing_annotations"]:
        print(f"  - {path}")
    print(f"IDs duplicados: {len(issues['duplicate_ids'])}")
    for item in issues["duplicate_ids"]:
        print(f"  - {item['id']}: {', '.join(item['paths'])}")


def emit(human_lines, args, payload):
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for line in human_lines:
            print(line)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pca_annotator",
        description="Inyecta anotaciones PCA y genera el grafo de impacto del proyecto.",
    )
    parser.add_argument("--config", default=None, help="Ruta a pca.config.json")
    parser.add_argument("--json", action="store_true", help="Salida legible por máquina")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ann = sub.add_parser("annotate", help="Inyecta/actualiza anotaciones")
    p_ann.add_argument("--dry-run", action="store_true", help="Previsualiza sin escribir")
    p_ann.add_argument("--backup", action="store_true", help="Genera .bak antes de escribir")
    p_ann.set_defaults(func=cmd_annotate)

    p_graph = sub.add_parser("graph", help="Genera grafo.json + grafo.mmd")
    p_graph.add_argument("--out", default="grafo", help="Nombre base de salida")
    p_graph.set_defaults(func=cmd_graph)

    p_imp = sub.add_parser("impact", help="Analiza el impacto de un id")
    p_imp.add_argument("id", help="id del nodo a analizar")
    p_imp.add_argument("--transitive", action="store_true", help="Incluye dependencias indirectas")
    p_imp.set_defaults(func=cmd_impact)

    p_check = sub.add_parser("check", help="Valida límites y relaciones")
    p_check.set_defaults(func=cmd_check)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.config is None:
        args.config = str(Path(__file__).resolve().parent / "pca.config.json")
    if not Path(args.config).exists():
        print(f"Error: no se encontró el manifiesto '{args.config}'.", file=sys.stderr)
        return 1
    config = load_config(args.config)
    languages = build_languages(config)
    # --json es global; aquí aseguramos el atributo en todos los subcomandos
    if not hasattr(args, "json"):
        args.json = False
    args.func(config, languages, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
