"""Source-data model: load fonts/<game>/ config.toml and symbols.toml."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Symbol:
    name: str
    ligature: list[str]
    category: str
    svg: dict[str, str]
    compose: dict[str, dict] = field(default_factory=dict)
    overflow: bool = False
    flat_foreground: bool = False


@dataclass
class ArtOverride:
    """Per-(symbol, style) art substitution used only by a v0 fallback flavor."""
    name: str
    style: str
    file: str


@dataclass
class ColrFallback:
    """A COLRv0 fallback flavor for a COLRv1 font: same glyphs/version, colour
    encoding downgraded to v0 so engines without COLRv1 still render symbols."""
    style_art: dict[str, str] = field(default_factory=dict)
    override_art: list[ArtOverride] = field(default_factory=list)


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
    colr_fallback: ColrFallback | None = None
    lite_colr_version: str = ""

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

    def colr_for(self, lite: bool) -> str:
        """COLR version of one family. The full family uses colr_version; the lite
        family (default style only) may declare its own lite-colr-version, which
        defaults to the full one."""
        return self.lite_colr_version if lite else self.colr_version


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
                category=s["category"],
                svg=dict(s["svg"]),
                compose={k: dict(v) for k, v in s.get("compose", {}).items()},
                overflow=s.get("overflow", False),
                flat_foreground=s.get("flat-foreground", False),
            )
        )
    return out


def _load_colr_fallback(config: dict, symbols: list[Symbol]) -> ColrFallback | None:
    raw = config.get("colr-fallback")
    if raw is None:
        return None
    if config.get("colr-version") != "v1":
        raise ValueError(
            f"colr-fallback requires colr-version \"v1\", got {config.get('colr-version')!r} "
            f"({config.get('code')})"
        )
    style_names = ["default"] + [st["name"] for st in config["styles"]]
    sym_names = {s.name: s for s in symbols}
    style_art = dict(raw.get("style-art", {}))
    for src, dst in style_art.items():
        if src not in style_names or dst not in style_names:
            raise ValueError(
                f"colr-fallback style-art {src}->{dst} references an unknown style "
                f"(known: {', '.join(style_names)})"
            )
    overrides = []
    for o in raw.get("override-art", []):
        sym = sym_names.get(o["name"])
        if sym is None:
            raise ValueError(f"colr-fallback override-art references unknown symbol {o['name']!r}")
        if o["style"] not in sym.svg:
            raise ValueError(
                f"colr-fallback override-art {o['name']}/{o['style']} has no such style in "
                f"symbols.toml (known: {', '.join(sym.svg)})"
            )
        overrides.append(ArtOverride(name=o["name"], style=o["style"], file=o["file"]))
    return ColrFallback(style_art=style_art, override_art=overrides)


def load_game(game_dir: Path) -> GameData:
    config = tomllib.loads((game_dir / "config.toml").read_text(encoding="utf-8"))
    symbols_toml = tomllib.loads((game_dir / "symbols.toml").read_text(encoding="utf-8"))
    symbols = _load_symbols(symbols_toml["symbols"])
    colr_version = config["colr-version"]
    lite_colr_version = config.get("lite-colr-version", colr_version)
    if lite_colr_version not in ("v0", "v1"):
        raise ValueError(
            f"unsupported lite-colr-version {lite_colr_version!r} for {config.get('code')} "
            "(expected \"v0\" or \"v1\")"
        )
    return GameData(
        path=game_dir,
        name=config["name"],
        code=config["code"],
        font_version=config["font-version"],
        colr_version=colr_version,
        categories=config["categories"],
        styles=config["styles"],
        compose=config["compose"],
        symbols=symbols,
        colr_fallback=_load_colr_fallback(config, symbols),
        lite_colr_version=lite_colr_version,
    )
