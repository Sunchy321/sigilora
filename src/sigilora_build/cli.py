"""sigilora-build command-line interface."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compose import compose_style
from .model import load_game
from .normalize import normalize_svg


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

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
