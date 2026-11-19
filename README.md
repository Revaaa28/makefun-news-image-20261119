# The World in One Day — 19 November 2026

A newspaper-style poster summing up Thursday 19 November 2026 in one
image, built for the make.fun competition
`news-image-20261119` ("Sum up 19 November's world news in one image").

## What it shows

Thirteen stories from reporting first published on 19 November 2026:

1. **Shenzhen (hero)** — the first-ever Trump–Xi–Putin trilateral, on the
   APEC sidelines, with Ukraine, Iran and nuclear arms on the agenda.
2. **Vice City** — GTA VI launches worldwide after 13 years of waiting.
3. **The Hague** — the International Court of Justice delivers its verdict
   in The Gambia's genocide case against Myanmar over the Rohingya.
4. **Bay of Bengal** — Cyclone Akvan nears India's coast; red alerts and
   school closures in Odisha and Andhra Pradesh, landfall due Friday.
5. **Voyager 1** — NASA confirms the 1977 probe is one light-day out, the
   first human-made object to reach the mark.
6. **Ottawa** — Carney strikes a tariff deal with Xi.
7. **Paris** — France's justice minister says Mélenchon "could win".
8. **Tokyo** — India and Japan review defence ties at a 2+2 meeting.
9. **Washington** — the US proposes tougher employment-based green-card rules.
10. **East Libya** — cocaine and millions of pills seized in Derna.
11. **Mogadishu** — Somalia accuses the UAE of secret military bases.
12. **Antalya** — COP31 climate talks continue as a draft deal draws fire.
13. **Australia** — Ben Duckett's 133 seals England's 2–1 ODI series win.

A dotted world map carries numbered pins for all 13 stories.

## How it is made

`main.py` runs the PIL-only renderer in `tools/render.py`, which draws
everything from code — skyline, flags, sunset, courthouse, cyclone
spiral, dotted map — with no photographs and no network. The output is
deterministic: repeated runs write byte-identical PNGs.

## Run it

```sh
python3 main.py            # writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR)
python3 tools/render.py    # writes entry.png in the current directory
```

Output: a 1024×1024 PNG, under 1 MiB.

## License

MIT — see `LICENSE`.
