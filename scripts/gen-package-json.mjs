// Generates packages/fonts/package.json from the game list in games.json,
// so the npm manifest never needs a hand-maintained game list.
import { readFileSync, writeFileSync } from 'node:fs'
import { join, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const { games } = JSON.parse(readFileSync(join(root, 'games.json'), 'utf-8'))

const exports = {}
for (const g of games) {
  exports[`./${g}.css`] = `./${g}/${g}.css`
  exports[`./${g}/*`] = `./${g}/*`
}

const pkg = {
  name: '@sigilora/fonts',
  version: '0.0.0',
  description: 'Color symbol fonts for game text via OpenType ligatures and COLR/CPAL.',
  repository: { type: 'git', url: 'https://github.com/Sunchy321/sigilora' },
  license: 'CC-BY-NC-4.0',
  files: games,
  sideEffects: ['*.css'],
  exports,
  keywords: ['fonts', 'opentype', 'ligatures', 'colr', 'cpal', 'color-fonts'],
  publishConfig: { access: 'public' },
}

writeFileSync(join(root, 'packages', 'fonts', 'package.json'), JSON.stringify(pkg, null, 2) + '\n')
console.log(`generated packages/fonts/package.json for games: ${games.join(', ')}`)
