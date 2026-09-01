// Copies the built consumer artifacts from packages/fonts/<game>/ into
// public/fonts/<game>/ so the site serves them. Run after
// `sigilora package <game>`.
//
// The game list and its order come from the repository root games.json
// (single source of truth); adding a game needs no changes here.
import { cp, mkdir } from 'node:fs/promises'
import { existsSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const srcDir = join(root, 'packages', 'fonts')
const siteDir = dirname(fileURLToPath(import.meta.url)) + '/..'
const publicDir = join(siteDir, 'public')
const dataDir = join(siteDir, 'app', 'data')

const { games } = JSON.parse(readFileSync(join(root, 'games.json'), 'utf-8'))

for (const game of games) {
  const from = join(srcDir, game)
  if (!existsSync(from)) {
    console.warn(`skip ${game}: packages/fonts/${game} missing (run sigilora package ${game})`)
    continue
  }
  const to = join(publicDir, 'fonts', game)
  await mkdir(to, { recursive: true })
  await cp(from, to, { recursive: true })
  console.log(`synced ${game} -> public/fonts/${game}`)

  // Metadata is imported at build time by the site, so it must live in the app
  await mkdir(dataDir, { recursive: true })
  for (const file of [`${game}.json`, `${game}-symbols.json`]) {
    await cp(join(from, file), join(dataDir, file))
  }
  console.log(`synced ${game} metadata -> app/data/`)
}
