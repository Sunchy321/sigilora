"""Source-data model: load fonts/<game>/ config.toml and symbols.toml."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Symbol:
    name: str
    ligature: list[str]
    display_name: str
    category: str
    svg: dict[str, str]
    compose: dict[str, dict] = field(default_factory=dict)
    overflow: bool = False


@dataclass
class GameData:
    path: Path
    name: str
    code: str
    font_version: str
    colr_version: str
    categories: list[dict]
    styles: list[dict]
    compose: dict
    symbols: list[Symbol]

    def by_name(self, name: str) -> Symbol | None:
        for s in self.symbols:
            if s.name == name:
                return s
        return None

    @property
    def raw_dir(self) -> Path:
        return self.path / "raw"

    @property
    def svg_dir(self) -> Path:
        return self.path / "svg"

    @property
    def style_order(self) -> list[str]:
        """Stable style order: 'default' first, then declared styles in config order."""
        return [st["name"] for st in self.styles]


def _load_symbols(toml_syms: list[dict]) -> list[Symbol]:
    out = []
    for s in toml_syms:
        lig = s["ligature"]
        if isinstance(lig, str):
            lig = [lig]
        out.append(
            Symbol(
                name=s["name"],
                ligature=lig,
                display_name=s.get("display-name", s["name"]),
                category=s["category"],
                svg=dict(s["svg"]),
                compose={k: dict(v) for k, v in s.get("compose", {}).items()},
                overflow=s.get("overflow", False),
            )
        )
    return out


def load_game(game_dir: Path) -> GameData:
    config = tomllib.loads((game_dir / "config.toml").read_text(encoding="utf-8"))
    symbols_toml = tomllib.loads((game_dir / "symbols.toml").read_text(encoding="utf-8"))
    return GameData(
        path=game_dir,
        name=config["name"],
        code=config["code"],
        font_version=config["font-version"],
        colr_version=config["colr-version"],
        categories=config["categories"],
        styles=config["styles"],
        compose=config["compose"],
        symbols=_load_symbols(symbols_toml["symbols"]),
    )
