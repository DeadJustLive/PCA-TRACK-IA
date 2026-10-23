#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @pca:start
# @id(tools.pca_annotator)
# @kind(service)
# @limit(lines: 250)
# @contract(cli: annotate|graph|impact|check|selftest)
# @relates(tools.pca_core)
# @relates(tools.pca_selftest)
# @relates(tools.readme)
# @relates(docs.sistema_anotaciones)
# @relates(docs.convenciones)
# @desc(CLI para inyectar anotaciones PCA, generar el grafo de impacto, detectar deriva y autoevaluarse)
# @pca:end

"""pca_annotator.py — CLI del anotador PCA (metodología PCA).

Inyecta bloques de anotación desde `pca.config.json`, genera el grafo
(JSON + Mermaid), calcula impacto, valida integridad, detecta deriva entre
manifiesto y archivos y ejecuta su propia suite de pruebas (`selftest`).

El núcleo vive en `pca_core.py` y las pruebas doradas en `pca_selftest.py`.
Solo biblioteca estándar. Ver `tools/README.md` y `docs/sistema_anotaciones.md`.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pca_core as core  # noqa: E402  (el path se fija arriba a propósito)

EXIT_OK = 0
EXIT_ERROR = 1


def load_environment(args):
    if args.config is None:
        args.config = str(Path(__file__).resolve().parent / "pca.config.json")
    if not Path(args.config).exists():
        print(f"Error: no se encontró el manifiesto '{args.config}'.", file=sys.stderr)
        return None, None
    config = core.load_config(args.config)
    return config, core.build_languages(config)


def cmd_annotate(config, languages, args):
    if args.check_drift:
        drifted = core.find_drift(config, languages)
        if args.json:
            print(json.dumps({"drift": drifted}, indent=2, ensure_ascii=False))
        elif drifted:
            print(f"DERIVA detectada ({len(drifted)} archivos; ejecuta 'annotate' para sincronizar):")
            for item in drifted:
                print(f"  - {item['path']} [{item['reason']}]")
        else:
            print("Sin deriva: los bloques coinciden con el manifiesto.")
        return EXIT_ERROR if drifted else EXIT_OK

    results, skipped = [], []
    for entry in config.get("files", []):
        path = (config["_base_dir"] / entry["path"]).resolve()
        if not path.exists():
            skipped.append(entry["path"])
            continue
        results.append(core.annotate_file(path, entry, languages, args.dry_run, args.backup))
    payload = {"results": results, "dry_run": args.dry_run}
    if skipped:
        payload["skipped"] = skipped
    emit(results, args, payload)
    return EXIT_OK


def cmd_graph(config, languages, args):
    graph = core.build_graph(config, languages)
    out_dir = (config["_base_dir"] / config.get("options", {}).get("output_dir", ".")).resolve()
    out_name = args.out or "grafo"
    json_path = out_dir / f"{out_name}.json"
    mmd_path = out_dir / f"{out_name}.mmd"
    json_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    mmd_path.write_text(core.to_mermaid(graph), encoding="utf-8")
    emit(
        [
            f"Grafo generado: {json_path.name} ({len(graph['nodes'])} nodos, {len(graph['edges'])} relaciones)",
            f"Mermaid: {mmd_path.name}",
        ],
        args,
        graph,
    )
    return EXIT_OK


def cmd_impact(config, languages, args):
    graph = core.build_graph(config, languages)
    known_ids = {node["id"] for node in graph["nodes"]}
    if args.id not in known_ids:
        print(f"ID no encontrado en el grafo: '{args.id}'. Revisa el typo o ejecuta 'check'.", file=sys.stderr)
        return EXIT_ERROR
    dependents = core.compute_impact(graph, args.id, args.transitive)
    if args.json:
        print(json.dumps({"id": args.id, "dependents": dependents}, indent=2, ensure_ascii=False))
    elif dependents:
        scope = "directa o indirectamente" if args.transitive else ""
        print(f"Archivos afectados por '{args.id}' ({len(dependents)}) {scope}:".strip())
        for item in dependents:
            print(f"  - {item}")
    else:
        print(f"Ningún archivo declara depender de '{args.id}' (nadie lo usa como @relates).")
    return EXIT_OK


def cmd_check(config, languages, args):
    graph = core.build_graph(config, languages)
    issues = graph["issues"]
    integrity = issues["dangling"] + issues["duplicate_ids"] + issues["missing_annotations"]
    report = {
        "over_limit": issues["over_limit"],
        "dangling": issues["dangling"],
        "missing_annotations": issues["missing_annotations"],
        "duplicate_ids": issues["duplicate_ids"],
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("== check ==")
        print(f"Nodos: {len(graph['nodes'])}  Relaciones: {len(graph['edges'])}")
        print(f"Sobre límite (advertencia): {len(issues['over_limit'])}")
        for item in issues["over_limit"]:
            print(f"  - {item['path']}: {item['lines']} líneas de código (límite {item['limit']})")
        print(f"Relaciones rotas (FK huérfanas): {len(issues['dangling'])}")
        for edge in issues["dangling"]:
            print(f"  - {edge['from']} --> {edge['to']}")
        print(f"Archivos sin anotación: {len(issues['missing_annotations'])}")
        for path in issues["missing_annotations"]:
            print(f"  - {path}")
        print(f"IDs duplicados: {len(issues['duplicate_ids'])}")
        for item in issues["duplicate_ids"]:
            print(f"  - {item['id']}: {', '.join(item['paths'])}")
    if args.strict and integrity:
        print("--strict: falla por problemas de integridad (FK huérfana, ID duplicado o archivo sin anotar).", file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


def cmd_selftest(config, languages, args):
    import pca_selftest

    passed, failures = pca_selftest.run_selftest()
    payload = {"passed": passed, "failed": [name for name, _ in failures]}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for name, detail in failures:
            print(f"FAIL {name}: {detail}")
        print(f"selftest: {passed} PASS, {len(failures)} FAIL")
    return EXIT_ERROR if failures else EXIT_OK


def emit(human_lines, args, payload):
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for line in human_lines:
            print(line)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="pca_annotator",
        description="Inyecta anotaciones PCA, genera el grafo de impacto y valida el manifiesto.",
    )
    parser.add_argument("--config", default=None, help="Ruta a pca.config.json")
    parser.add_argument("--json", action="store_true", help="Salida legible por máquina")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ann = sub.add_parser("annotate", help="Inyecta/actualiza anotaciones")
    p_ann.add_argument("--dry-run", action="store_true", help="Previsualiza sin escribir")
    p_ann.add_argument("--backup", action="store_true", help="Genera .bak antes de escribir")
    p_ann.add_argument("--check-drift", action="store_true",
                       help="Solo reporta bloques desfazados del manifiesto (no escribe; sale con 1 si hay deriva)")
    p_ann.set_defaults(func=cmd_annotate)

    p_graph = sub.add_parser("graph", help="Genera grafo.json + grafo.mmd")
    p_graph.add_argument("--out", default="grafo", help="Nombre base de salida")
    p_graph.set_defaults(func=cmd_graph)

    p_imp = sub.add_parser("impact", help="Analiza el impacto de un id")
    p_imp.add_argument("id", help="id del nodo a analizar")
    p_imp.add_argument("--transitive", action="store_true", help="Incluye dependencias indirectas")
    p_imp.set_defaults(func=cmd_impact)

    p_check = sub.add_parser("check", help="Valida límites y relaciones")
    p_check.add_argument("--strict", action="store_true",
                         help="Sale con 1 ante FK huérfana, ID duplicado o archivo sin anotar")
    p_check.set_defaults(func=cmd_check)

    p_self = sub.add_parser("selftest", help="Ejecuta las pruebas doradas de la herramienta")
    p_self.set_defaults(func=cmd_selftest)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    config, languages = load_environment(args)
    if config is None:
        return EXIT_ERROR
    return args.func(config, languages, args) or EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
