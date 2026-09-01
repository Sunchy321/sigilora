# Sigilora

A symbol font project for game text. Sigilora uses OpenType ligatures to turn established game-community text representations into color symbols, rendered inline within a line of text via COLR/CPAL. Symbols keep their text identity: content stays copyable, searchable, and storable, and it degrades back to the game's text representation when the font is not loaded.

Sigilora is a neutral project published independently of the current website; the website is just one consumer.

## Repository Structure

```text
sigilora/
├── src/sigilora_build/       # Python build and validation logic
├── fonts/<game>/             # canonical source data per game
├── packages/fonts/           # @sigilora/fonts publish directory
├── website/                  # Nuxt official site, docs and playground
└── tests/                    # font structure, mapping and shaping validation
```

## Documentation

- Architecture design (English): [docs/project-architecture.md](docs/project-architecture.md)
- Architecture design (简体中文): [docs/project-architecture.zh-CN.md](docs/project-architecture.zh-CN.md)
- Agent guidance: [AGENTS.md](AGENTS.md)

## License

Layered licensing. Code, build tooling, and website source are MIT; the
font binaries and graphic assets are **CC BY-NC 4.0** (non-commercial,
attribution required). The underlying Magic: The Gathering symbol art is
owned by Wizards of the Coast. See [LICENSE](LICENSE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
