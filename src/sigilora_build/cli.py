"""sigilora-build command-line interface."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .build import build as build_font
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
    plantin = Path(args.plantin) if args.plantin else None
    counts = {"generated": 0, "static": 0}
    for sym in game.symbols:
        for style, _file in sym.svg.items():
            spec = sym.compose.get(style)
            target = out_dir / style / _file
            target.parent.mkdir(parents=True, exist_ok=True)
            if spec is None:
                # default style without a compose spec: normalize the raw default
                src = game.raw_dir / "default" / _file
                normalize_svg(src, target)
                counts["generated"] += 1
            else:
                compose_style(game, sym, style, target, plantin)
                normalize_svg(target, target)
                counts["generated" if spec["type"] != "static" else "static"] += 1
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
    fonts = []
    for lite in (False, True):
        suffix = "-Lite" if lite else ""
        ttf = build_dir / f"Sigilora-{game_label}{suffix}-{game.font_version}.ttf"
        woff2 = ttf.with_suffix(".woff2")
        if ttf.exists() and woff2.exists():
            fonts.append(("lite" if lite else "full", ttf, woff2))
    if not fonts:
        print(f"error: no built fonts found in {build_dir}", file=sys.stderr)
        return 1
    ok = True
    for label, ttf, woff2 in fonts:
        try:
            run_validation(game, ttf, woff2, lite=(label == "lite"))
            print(f"validate {label}: OK")
        except ValidationError as e:
            ok = False
            print(f"validate {label}: FAIL: {e}", file=sys.stderr)
    return 0 if ok else 1


def cmd_build(args: argparse.Namespace) -> int:
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
    if args.full:
        result = build_font(game, out_dir, lite=False)
        print(f"built {result['family']} -> {result['ttf']} / {result['woff2']}")
    if args.lite:
        result = build_font(game, out_dir, lite=True)
        print(f"built {result['family']} -> {result['ttf']} / {result['woff2']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sigilora-build")
    parser.add_argument("--root", default=Path.cwd(), type=Path, help="repo root (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_norm = sub.add_parser("normalize", help="compose and normalize target SVGs from raw materials")
    p_norm.add_argument("game", help="game code, e.g. magic")
    p_norm.add_argument("--out", type=Path, default=None, help="output dir (default: fonts/<game>/svg)")
    p_norm.add_argument("--plantin", type=str, default=None,
                        help="override path to Plantin-Bold.ttf (default: fonts/<game>/external/)")
    p_norm.set_defaults(func=cmd_normalize)

    p_build = sub.add_parser("build", help="build TTF/WOFF2 with ligature features via nanoemoji")
    p_build.add_argument("game", help="game code, e.g. magic")
    p_build.add_argument("--lite", action="store_true", help="build only the lite font (default style + liga)")
    p_build.add_argument("--full", action="store_true", help="build only the full font (all styles + ssXX)")
    p_build.add_argument("--out", type=Path, default=None, help="output dir (default: fonts/<game>/build)")
    p_build.set_defaults(func=cmd_build)

    p_val = sub.add_parser("validate", help="run release-blocking validation on the built fonts")
    p_val.add_argument("game", help="game code, e.g. magic")
    p_val.add_argument("--build", type=Path, default=None, help="build dir (default: fonts/<game>/build)")
    p_val.set_defaults(func=cmd_validate)

    p_pkg = sub.add_parser("package", help="assemble consumer artifacts into packages/fonts/<game>/")
    p_pkg.add_argument("game", help="game code, e.g. magic")
    p_pkg.add_argument("--build", type=Path, default=None, help="build dir (default: fonts/<game>/build)")
    p_pkg.add_argument("--out", type=Path, default=None, help="output dir (default: packages/fonts/<game>)")
    p_pkg.set_defaults(func=cmd_package)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
