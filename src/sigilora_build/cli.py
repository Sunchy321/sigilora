"""sigilora command-line interface."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from types import SimpleNamespace

from .build import build as build_font
from .build import flavor_specs
from .compose import compose_style
from .model import load_game
from .normalize import normalize_svg
from .package import package as package_font
from .validate import ValidationError, validate as run_validation


def _game_dir(game: str, root: Path) -> Path:
    return root / "fonts" / game


def cmd_normalize(args: argparse.Namespace) -> int:
    game_dir = _game_dir(args.game, args.root)
    if not (game_dir / "config.toml").exists():
        print(f"error: no source data found at {game_dir}", file=sys.stderr)
        return 1
    game = load_game(game_dir)
    out_dir = args.out / game.code if args.out else game.svg_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    counts = {"generated": 0, "static": 0}
    for sym in game.symbols:
        for style, _file in sym.svg.items():
            spec = sym.compose.get(style)
            target = out_dir / style / _file
            target.parent.mkdir(parents=True, exist_ok=True)
            if spec is None:
                # style without a compose spec: normalize the raw source for that style
                src = game.raw_dir / style / _file
                normalize_svg(src, target)
                counts["generated"] += 1
            else:
                compose_style(game, sym, style, target)
                normalize_svg(target, target)
                counts["generated" if spec["type"] != "static" else "static"] += 1
    # colr-fallback override art lives outside the symbols.toml svg maps (it is a
    # v0-only substitute, not a declared style); normalize it into svg/ too.
    fb = game.colr_fallback
    if fb is not None:
        for o in fb.override_art:
            target = out_dir / o.style / o.file
            target.parent.mkdir(parents=True, exist_ok=True)
            normalize_svg(game.raw_dir / o.style / o.file, target)
            counts["generated"] += 1
    print(f"normalized {game.code}: {counts['generated']} composed, {counts['static']} static -> {out_dir}")
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    game_dir = _game_dir(args.game, args.root)
    game = load_game(game_dir)
    build_dir = args.build if args.build else game.path / "build"
    out_dir = args.out if args.out else args.root / "packages" / "fonts" / game.code
    try:
        package_font(game, build_dir, out_dir)
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    print(f"packaged {game.code} -> {out_dir}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    game_dir = _game_dir(args.game, args.root)
    game = load_game(game_dir)
    build_dir = args.build if args.build else game.path / "build"
    game_label = game.code.capitalize()
    # Validate every binary the family set is built from (see flavor_specs): the
    # primary flavor plus, where a v1 family declares [colr-fallback], its -v0
    # COLRv0 fallback (same glyphs/mappings, COLR version 0).
    fonts = []
    for lite in (False, True):
        lite_suffix = "-Lite" if lite else ""
        base_label = "lite" if lite else "full"
        for spec in flavor_specs(game, lite):
            suffix = spec["suffix"]
            ttf = build_dir / f"Sigilora-{game_label}{lite_suffix}-{game.font_version}{suffix}.ttf"
            woff2 = ttf.with_suffix(".woff2")
            if ttf.exists() and woff2.exists():
                fonts.append((f"{base_label}{suffix}", ttf, woff2, spec["colr"]))
    if not fonts:
        print(f"error: no built fonts found in {build_dir}", file=sys.stderr)
        return 1
    ok = True
    for label, ttf, woff2, colr in fonts:
        try:
            run_validation(game, ttf, woff2, lite=label.startswith("lite"),
                           expected_colr_version=colr)
            print(f"validate {label}: OK")
        except ValidationError as e:
            ok = False
            print(f"validate {label}: FAIL: {e}", file=sys.stderr)
    return 0 if ok else 1


def cmd_compile(args: argparse.Namespace) -> int:
    game_dir = _game_dir(args.game, args.root)
    if not (game_dir / "config.toml").exists():
        print(f"error: no source data found at {game_dir}", file=sys.stderr)
        return 1
    game = load_game(game_dir)
    if not (game.svg_dir / "default").exists():
        print(f"error: run normalize first (missing {game.svg_dir})", file=sys.stderr)
        return 1
    out_dir = args.out if args.out else game.path / "build"
    if not args.full and not args.lite:
        args.full = args.lite = True
    # build() returns one result per flavor: the primary, plus the COLRv0
    # fallback when the game declares [colr-fallback].
    if args.full:
        for result in build_font(game, out_dir, lite=False):
            print(f"built {result['family']} -> {result['ttf']} / {result['woff2']}")
    if args.lite:
        for result in build_font(game, out_dir, lite=True):
            print(f"built {result['family']} -> {result['ttf']} / {result['woff2']}")
    return 0


def _step_ns(args: argparse.Namespace, **overrides) -> argparse.Namespace:
    """Namespace for a pipeline step: always carries game/root from the top call."""
    ns = SimpleNamespace(game=args.game, root=args.root)
    ns.__dict__.update(overrides)
    return ns


def cmd_build(args: argparse.Namespace) -> int:
    """normalize -> compile (full + lite) -> validate -> package in one run.

    Mirrors the per-game sequence in release.yml, so a local run is a release
    rehearsal. Stops at the first failing step. normalize always writes the
    canonical svg dir the compile reads; --build relocates the compiled outputs
    (and the validate/package inputs), --out relocates the packaged consumer
    artifacts.
    """
    game_dir = _game_dir(args.game, args.root)
    if not (game_dir / "config.toml").exists():
        print(f"error: no source data found at {game_dir}", file=sys.stderr)
        return 1
    if cmd_normalize(_step_ns(args, out=None)) != 0:
        return 1
    build_dir = args.build if args.build else game_dir / "build"
    if cmd_compile(_step_ns(args, out=build_dir, full=True, lite=True)) != 0:
        return 1
    if cmd_validate(_step_ns(args, build=build_dir)) != 0:
        return 1
    out_dir = args.out if args.out else args.root / "packages" / "fonts" / args.game
    if cmd_package(_step_ns(args, build=build_dir, out=out_dir)) != 0:
        return 1
    print(f"build {args.game}: OK -> {out_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sigilora")
    parser.add_argument("--root", default=Path.cwd(), type=Path, help="repo root (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize", help="compose and normalize target SVGs from raw materials")
    p_norm.add_argument("game", help="game code, e.g. magic")
    p_norm.add_argument("--out", type=Path, default=None, help="output dir (default: fonts/<game>/svg)")
    p_norm.set_defaults(func=cmd_normalize)

    p_compile = sub.add_parser("compile", help="compile staged SVGs into TTF/WOFF2 with ligature features via nanoemoji")
    p_compile.add_argument("game", help="game code, e.g. magic")
    p_compile.add_argument("--lite", action="store_true", help="compile only the lite font (default style + liga)")
    p_compile.add_argument("--full", action="store_true", help="compile only the full font (all styles + ssXX)")
    p_compile.add_argument("--out", type=Path, default=None, help="output dir (default: fonts/<game>/build)")
    p_compile.set_defaults(func=cmd_compile)

    p_val = sub.add_parser("validate", help="run release-blocking validation on the compiled fonts")
    p_val.add_argument("game", help="game code, e.g. magic")
    p_val.add_argument("--build", type=Path, default=None, help="build dir (default: fonts/<game>/build)")
    p_val.set_defaults(func=cmd_validate)

    p_pkg = sub.add_parser("package", help="assemble consumer artifacts into packages/fonts/<game>/")
    p_pkg.add_argument("game", help="game code, e.g. magic")
    p_pkg.add_argument("--build", type=Path, default=None, help="build dir (default: fonts/<game>/build)")
    p_pkg.add_argument("--out", type=Path, default=None, help="output dir (default: packages/fonts/<game>)")
    p_pkg.set_defaults(func=cmd_package)

    p_build = sub.add_parser("build", help="normalize, compile, validate, and package a game in one run")
    p_build.add_argument("game", help="game code, e.g. magic")
    p_build.add_argument("--build", type=Path, default=None, help="build dir (default: fonts/<game>/build)")
    p_build.add_argument("--out", type=Path, default=None, help="consumer output dir (default: packages/fonts/<game>)")
    p_build.set_defaults(func=cmd_build)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
