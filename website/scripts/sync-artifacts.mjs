// Copies the built consumer artifacts from packages/fonts/<game>/ into
// public/fonts/<game>/ so the site serves them. Run after
// `sigilora-build package <game>`.
import { cp, mkdir } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..')
const games = ['magic']
const srcDir = join(root, 'packages', 'fonts')
const publicDir = join(dirname(fileURLToPath(import.meta.url)), '..', 'public')

for (const game of games) {
  const from = join(srcDir, game)
  if (!existsSync(from)) {
    console.warn(`skip ${game}: packages/fonts/${game} missing (run sigilora-build package ${game})`)
    continue
  }
  const to = join(publicDir, 'fonts', game)
  await mkdir(to, { recursive: true })
  await cp(from, to, { recursive: true })
  console.log(`synced ${game} -> public/fonts/${game}`)
}
