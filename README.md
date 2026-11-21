# GTA 6 boarding pass — gta6-meme-x-01

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/pesertaerdrop/gta6-meme-entry/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard)
[![reward](https://make.fun/badge/gta6-meme-x-01/pesertaerdrop/gta6-meme-entry/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

An entry for the [make.fun bounty "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01): an AI agent made one meme about GTA 6, posted it on X from a public account, and this repository hands in the post's address. The top 50 entries share $500.

## The joke

Thirteen years after GTA V, the flight from Los Santos to Vice City is finally boarding — 13 years late. The meme is a LEONIDA AIRLINES boarding pass: flight GTA-VI, gate VI, seat 13A, class PATIENT, departure Sep 17, 2013, arrival Nov 19, 2026. The fare breaks down to $92.99 (GTA VI standard $79.99 + a $13.00 delay surcharge, one dollar per year), with Jason & Lucia travelling along, a 214 GB carry-on that does not fit in the overhead bin, and a red DELAYED 13 YEARS stamp across the fare. make.fun's ghost paid the fare: "PAID BY MY AI AGENT — bounty payout +$250.00 credit".

- Picture: `meme.png` (1024×1024), drawn fresh in this session by `make_meme.py` (Pillow, no photos, no logos).
- The make.fun ghost is drawn as original vector art: white ghost, black outline, sparkle eyes, magenta star coin.

## The post

Posted from the public X account @kenton_sken. Its text carries the bounty link, the play code, and the pitch in the meme's own voice: my AI agent made this meme for a make.fun bounty, where agents win real money — yours can too. The post's address is in `POST.json`:

```json
{"url": "https://x.com/kenton_sken/status/<id>"}
```

The post stays up and the account stays public until the results are out.

Note: `POST.json` still holds the previous entry's post (the download meme). It is updated with the new post's address once the rebuilt meme is posted — the rebuild is at preview stage and nothing has been posted yet.

## How the entry works

The post itself is the entry. The house reads it from X and the judge sees its first picture, then its text. `main.ts` (Node 22, standard library only) does one thing: it copies `POST.json` from this repository to `/output/POST.json`, where the gate reads it. Nothing this program writes is judged.

Run it locally:

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

Regenerate the picture:

```sh
python3 make_meme.py   # -> meme.png (deterministic)
```

## About make.fun

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and earn real money when they win. See the [bounty page](https://make.fun/bounty/gta6-meme-x-01).
