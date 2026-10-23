#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @pca:start
# @id(tools.pca_selftest)
# @kind(test)
# @limit(lines: 380)
# @contract(run_selftest(): (passed, failures))
# @relates(tools.pca_core)
# @relates(tools.pca_annotator)
# @desc(Pruebas doradas del anotador PCA: parser, inyección, grafo, impacto, deriva y códigos de salida)
# @pca:end

"""pca_selftest.py — Suite de pruebas doradas de la herramienta PCA.

Cubre la regresión KB-004 (varias líneas `@relates` deben acumularse), la
inyección de bloques (idempotencia, reemplazo, inserción, CRLF), la construcción
del grafo (aristas, FK huérfanas, IDs duplicados, `@limit` sin contar el bloque),
el impacto directo/trasitivo, la detección de deriva y los códigos de salida de
la CLI. Se ejecuta con `python tools/pca_annotator.py selftest`.

Solo biblioteca estándar; cada caso trabaja en un directorio temporal.
"""

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pca_annotator as cli  # noqa: E402
import pca_core as core  # noqa: E402

KT_SAMPLE = "package demo\n\nclass Sample\n"
PY_SAMPLE = "print('hola')\n"


def _entry(path, node_id, **extra):
    entry = {"path": path, "id": node_id, "kind": "component"}
    entry.update(extra)
    return entry


def _config(base, entries):
    return {"base_dir": ".", "files": entries, "_base_dir": Path(base)}


def _write(base, rel, text):
    target = Path(base) / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target


def _write_raw(path, text):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def _read_raw(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def _workspace():
    return tempfile.TemporaryDirectory(prefix="pca_selftest_")


def _run_cli(argv):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
        code = cli.main(argv)
    return code, buffer.getvalue()


def _write_manifest(base, entries):
    manifest = Path(base) / "pca.config.json"
    manifest.write_text(json.dumps({"base_dir": ".", "files": entries}, indent=2), encoding="utf-8")
    return manifest


# --- Parser -----------------------------------------------------------------

def test_parse_accumulates_repeated_relates():
    block = "<!--\n@id(a.b)\n@kind(doc)\n@relates(x.y)\n@relates(x.z)\n@relates(x.w)\n@desc(D)\n-->"
    meta = core.parse_annotations(block)
    assert meta["relates"] == ["x.y", "x.z", "x.w"], (
        f"KB-004: se esperaban las 3 relaciones acumuladas, llegó {meta['relates']}"
    )


def test_parse_comma_and_compact_forms():
    text = "@relates(a.b, c.d)\n@file(id=q.r, kind=model, limit=40, relates=s.t, desc=Hola)"
    meta = core.parse_annotations(text)
    assert meta["id"] == "q.r", f"form compacta: id={meta['id']}"
    assert meta["limit"] == 40, f"form compacta: limit={meta['limit']}"
    assert meta["relates"] == ["s.t", "a.b", "c.d"], f"coma + compacta: {meta['relates']}"


def test_parse_deduplicates_relations():
    meta = core.parse_annotations("@relates(a.b)\n@relates(a.b, c.d)")
    assert meta["relates"] == ["a.b", "c.d"], f"dedupe incorrecto: {meta['relates']}"


# --- Inyección de bloques ---------------------------------------------------

def test_annotate_is_idempotent():
    with _workspace() as tmp:
        entry = _entry("a.kt", "demo.a", desc="Demo A")
        path = _write(tmp, "a.kt", KT_SAMPLE)
        core.annotate_file(path, entry, core.build_languages({}))
        first = _read_raw(path)
        core.annotate_file(path, entry, core.build_languages({}))
        second = _read_raw(path)
        assert first == second, "annotate debe ser idempotente (segunda corrida sin cambios)"
        assert second.startswith("// @pca:start"), "el bloque debe quedar en la cabecera"
        assert second.count("// @pca:start") == 1, "no debe duplicar el bloque"


def test_annotate_replaces_stale_block():
    with _workspace() as tmp:
        stale = "// @pca:start\n// @id(old.id)\n// @kind(component)\n// @pca:end\npackage demo\n"
        entry = _entry("a.kt", "demo.a", desc="Demo A")
        path = _write(tmp, "a.kt", stale)
        core.annotate_file(path, entry, core.build_languages({}))
        text = _read_raw(path)
        assert "demo.a" in text and "old.id" not in text, "el bloque obsoleto debe reemplazarse"
        assert text.count("@pca:start") == 1, "solo puede existir un bloque"


def test_annotate_respects_shebang_and_coding():
    with _workspace() as tmp:
        entry = _entry("s.py", "demo.s", desc="Script")
        path = _write(tmp, "s.py", "#!/usr/bin/env python3\n# coding: utf-8\nprint(1)\n")
        core.annotate_file(path, entry, core.build_languages({}))
        lines = _read_raw(path).splitlines()
        assert lines[0].startswith("#!"), "el shebang debe quedar primero"
        assert lines[1].startswith("# coding:"), "la línea coding debe quedar antes del bloque"
        assert core.MARKER_START in lines[2], f"bloque en línea inesperada: {lines[2]!r}"


def test_annotate_inserts_after_front_matter():
    with _workspace() as tmp:
        entry = _entry("doc.md", "demo.doc", desc="Documento")
        path = _write(tmp, "doc.md", "---\ntitle: x\n---\n# Hola\n")
        core.annotate_file(path, entry, core.build_languages({}))
        lines = _read_raw(path).splitlines()
        assert lines[0] == "---" and lines[2] == "---", "el front-matter no debe separarse"
        assert core.MARKER_START in lines[3], f"bloque inesperado en: {lines[3]!r}"


def test_annotate_preserves_crlf():
    with _workspace() as tmp:
        entry = _entry("a.kt", "demo.a")
        path = Path(tmp) / "a.kt"
        _write_raw(path, "package demo\r\n\r\nclass A\r\n")
        core.annotate_file(path, entry, core.build_languages({}))
        text = _read_raw(path)
        assert "@pca:start" in text, "el bloque no se inyectó"
        assert "\n" not in text.replace("\r\n", ""), "los finales CRLF no deben convertirse en LF"


# --- Grafo ------------------------------------------------------------------

def _annotate_all(base, entries, languages=None):
    """Escribe cada archivo con su muestra y le inyecta su bloque (como en el proyecto real)."""
    languages = languages or core.build_languages({})
    for entry in entries:
        path = _write(base, entry["path"], KT_SAMPLE)
        core.annotate_file(path, entry, languages)


def test_graph_reports_dangling_relation():
    with _workspace() as tmp:
        languages = core.build_languages({})
        entries = [
            _entry("a.kt", "demo.a", relates=["demo.b"]),
            _entry("b.kt", "demo.b"),
            _entry("c.kt", "demo.c", relates=["missing.x"]),
        ]
        _annotate_all(tmp, entries, languages)
        graph = core.build_graph(_config(tmp, entries), languages)
        assert len(graph["nodes"]) == 3, f"nodos: {len(graph['nodes'])}"
        assert len(graph["edges"]) == 2, f"aristas: {len(graph['edges'])}"
        dangling = graph["issues"]["dangling"]
        assert len(dangling) == 1 and dangling[0]["from"] == "demo.c", f"dangling: {dangling}"


def test_graph_detects_duplicate_ids():
    with _workspace() as tmp:
        entries = [_entry("a.kt", "demo.a"), _entry("b.kt", "demo.a")]
        _annotate_all(tmp, entries)
        graph = core.build_graph(_config(tmp, entries), core.build_languages({}))
        duplicates = graph["issues"]["duplicate_ids"]
        assert len(duplicates) == 1 and duplicates[0]["id"] == "demo.a", f"duplicados: {duplicates}"


def test_limit_ignores_annotation_block():
    with _workspace() as tmp:
        languages = core.build_languages({})
        code = "".join(f"val v{i} = {i}\n" for i in range(12))
        entry = _entry("a.kt", "demo.a", limit=15, desc="Doce líneas de código")
        path = _write(tmp, "a.kt", code)
        core.annotate_file(path, entry, languages)
        graph = core.build_graph(_config(tmp, [entry]), languages)
        node = graph["nodes"][0]
        assert node["total_lines"] > entry["limit"], "el total debe superar el límite…"
        assert node["lines"] == 12 and not node["over_limit"], (
            f"el @limit debe medir solo código: lines={node['lines']}, over={node['over_limit']}"
        )
        entry_over = _entry("b.kt", "demo.b", limit=15)
        path_over = _write(tmp, "b.kt", "".join(f"val w{i} = {i}\n" for i in range(20)))
        core.annotate_file(path_over, entry_over, languages)
        graph2 = core.build_graph(_config(tmp, [entry_over]), languages)
        assert graph2["nodes"][0]["over_limit"], "un exceso real de código debe reportarse"


# --- Impacto y deriva -------------------------------------------------------

def test_impact_direct_and_transitive():
    with _workspace() as tmp:
        entries = [
            _entry("a.kt", "demo.a", relates=["demo.b"]),
            _entry("b.kt", "demo.b", relates=["demo.c"]),
            _entry("c.kt", "demo.c"),
        ]
        _annotate_all(tmp, entries)
        graph = core.build_graph(_config(tmp, entries), core.build_languages({}))
        direct = core.compute_impact(graph, "demo.c")
        transitive = core.compute_impact(graph, "demo.c", transitive=True)
        assert direct == ["demo.b"], f"impacto directo: {direct}"
        assert transitive == ["demo.a", "demo.b"], f"impacto transitivo: {transitive}"


def test_drift_reports_stale_and_missing_blocks():
    with _workspace() as tmp:
        languages = core.build_languages({})
        good = _entry("good.kt", "demo.good", desc="En orden")
        stale = _entry("stale.kt", "demo.stale", desc="Nuevo desc")
        missing = _entry("plain.kt", "demo.plain")
        core.annotate_file(_write(tmp, "good.kt", KT_SAMPLE), good, languages)
        _write(tmp, "stale.kt", "// @pca:start\n// @id(demo.stale)\n// @desc(Viejo desc)\n// @pca:end\n" + KT_SAMPLE)
        _write(tmp, "plain.kt", KT_SAMPLE)
        drifted = core.find_drift(_config(tmp, [good, stale, missing, _entry("absent.kt", "demo.x")]), languages)
        reasons = {item["path"]: item["reason"] for item in drifted}
        assert "good.kt" not in reasons, "un archivo sincronizado no debe reportarse"
        assert reasons.get("stale.kt") == "stale_block", f"stale: {reasons}"
        assert reasons.get("plain.kt") == "missing_block", f"missing block: {reasons}"
        assert reasons.get("absent.kt") == "missing_file", f"missing file: {reasons}"


# --- Códigos de salida de la CLI --------------------------------------------

def test_cli_check_strict_exit_codes():
    with _workspace() as tmp:
        clean = [
            _entry("a.kt", "demo.a", relates=["demo.b"]),
            _entry("b.kt", "demo.b"),
        ]
        _annotate_all(tmp, clean)
        manifest = _write_manifest(tmp, clean)
        code, _ = _run_cli(["--config", str(manifest), "check", "--strict"])
        assert code == cli.EXIT_OK, f"check limpio con --strict debe salir 0, salió {code}"

        broken = clean + [_entry("c.kt", "demo.c", relates=["missing.x"])]
        _annotate_all(tmp, [broken[-1]])
        _write_manifest(tmp, broken)
        code, _ = _run_cli(["--config", str(manifest), "check", "--strict"])
        assert code == cli.EXIT_ERROR, f"FK huérfana con --strict debe salir 1, salió {code}"
        code, _ = _run_cli(["--config", str(manifest), "check"])
        assert code == cli.EXIT_OK, f"sin --strict debe seguir saliendo 0, salió {code}"


def test_cli_impact_unknown_id_fails():
    with _workspace() as tmp:
        entry = _entry("a.kt", "demo.a")
        _annotate_all(tmp, [entry])
        manifest = _write_manifest(tmp, [entry])
        code, output = _run_cli(["--config", str(manifest), "impact", "no.existe"])
        assert code == cli.EXIT_ERROR, f"impact de id inexistente debe salir 1, salió {code}"
        assert "no encontrado" in output.lower(), f"mensaje confuso: {output.strip()}"


def test_cli_check_drift_exit_codes_and_read_only():
    with _workspace() as tmp:
        stale = _entry("stale.kt", "demo.stale", desc="Descripción nueva")
        path = _write(tmp, "stale.kt", "// @pca:start\n// @id(demo.stale)\n// @desc(Vieja)\n// @pca:end\n" + KT_SAMPLE)
        manifest = _write_manifest(tmp, [stale])
        before = _read_raw(path)
        code, output = _run_cli(["--config", str(manifest), "annotate", "--check-drift"])
        assert code == cli.EXIT_ERROR, f"deriva debe salir 1, salió {code}"
        assert "stale.kt" in output, f"debe nombrar el archivo con deriva: {output.strip()}"
        assert _read_raw(path) == before, "--check-drift no debe escribir el archivo"

        code, _ = _run_cli(["--config", str(manifest), "annotate"])
        assert code == cli.EXIT_OK, "annotate debe salir 0"
        code, _ = _run_cli(["--config", str(manifest), "annotate", "--check-drift"])
        assert code == cli.EXIT_OK, "tras sincronizar ya no debe haber deriva"


ALL_TESTS = [
    test_parse_accumulates_repeated_relates,
    test_parse_comma_and_compact_forms,
    test_parse_deduplicates_relations,
    test_annotate_is_idempotent,
    test_annotate_replaces_stale_block,
    test_annotate_respects_shebang_and_coding,
    test_annotate_inserts_after_front_matter,
    test_annotate_preserves_crlf,
    test_graph_reports_dangling_relation,
    test_graph_detects_duplicate_ids,
    test_limit_ignores_annotation_block,
    test_impact_direct_and_transitive,
    test_drift_reports_stale_and_missing_blocks,
    test_cli_check_strict_exit_codes,
    test_cli_impact_unknown_id_fails,
    test_cli_check_drift_exit_codes_and_read_only,
]


def run_selftest():
    """Ejecuta todos los casos y devuelve (cantidad de PASS, lista de (nombre, detalle))."""
    passed, failures = [], []
    for case in ALL_TESTS:
        try:
            case()
        except AssertionError as error:
            failures.append((case.__name__, str(error)))
        except Exception as error:  # noqa: BLE001 — un error inesperado también es un FAIL
            failures.append((case.__name__, f"{type(error).__name__}: {error}"))
        else:
            passed.append(case.__name__)
    return len(passed), failures


if __name__ == "__main__":
    count, failed = run_selftest()
    for name, detail in failed:
        print(f"FAIL {name}: {detail}")
    print(f"selftest: {count} PASS, {len(failed)} FAIL")
    sys.exit(1 if failed else 0)
