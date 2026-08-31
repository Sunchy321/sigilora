# external — files you must provide

This folder holds the **external dependency files** (commercial fonts, etc.) needed to build this game's font. These files are **not committed** to the repository (excluded by `.gitignore`) and must be obtained and placed here by you.

Place the following files in this folder:

| File | Purpose | Referenced by |
|---|---|---|
| `Plantin-Bold.ttf` | Font used to render loyalty-counter text as paths | `[compose.loyalty].font` in `config.toml` |

Once placed, the build command looks up these files in this folder.

> Note: make sure you have the right to use these files. Plantin is a commercial font by Monotype; the final font embeds glyph outline paths rendered from it (see `../LICENSES.md`).
