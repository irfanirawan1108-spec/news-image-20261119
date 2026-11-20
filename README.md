[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/irfanirawan1108-spec/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/irfanirawan1108-spec/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# news-image-20261119 — The World in One Day (round 3)

Entry for make.fun bounty
[`news-image-20261119`](https://make.fun/c/news-image-20261119):
sum up the world's news of **Thursday 19 November 2026** in one image.

## The image

A newspaper front page, drawn programmatically and deterministically
with Pillow (`render.py`), 1024×1024 PNG. Every story was checked
against same-day reporting; round 3 fixes round 2's two dated errors
(the Houthi camp strike was 19 October, the Onkalo licence 22 October)
and promotes the day's biggest story — the ICJ genocide verdict — to
the lead, adding the Bangladesh turmoil and the Gulf/Hormuz crisis
that round 2 missed.

- **Lead — The Hague:** ICJ finds Myanmar guilty of genocide against
  the Rohingya, 9–6 — the first state ever held responsible — and
  orders reparations.
- **Shenzhen — Summit:** Trump, Xi and Putin hold the first three-way
  summit; a four-point “Declaration toward Peace”.
- **New York — Markets:** Anthropic's IPO is the biggest ever, $81.3bn
  at $83 a share; ANT opens at $111.50, closes at $97.17.
- **Gaza — War:** Israeli troops cross the ceasefire line in a rare
  ground operation beyond the Yellow Line.
- **The Gulf — Energy:** Iran widens its attacks to Kuwait and Bahrain;
  the IEA calls the Hormuz crisis the greatest threat ever to energy
  security.
- **Dhaka — Unrest:** Yunus's home torched as violence hits 28
  districts; paramilitary troops deploy.
- **Vice City — Games:** GTA VI rolls out worldwide at midnight.
- **New York — Art:** Van Gogh's *Châtaigniers en fleurs* sells for a
  record $190.4m at Sotheby's.
- **Also today:** Crimea bridge hit again; EU proposes a €45bn Ukraine
  loan; Denmark approves the Greenland–US pact; US–Venezuela military
  deal; North Korea expands uranium enrichment; COP31 talks in Antalya.

## How it runs

`main.py` (Python 3.13, standard library only) copies the image held in
this repository to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`),
verifying the copy by sha256. No network, no randomness — the same
bytes every run.

Rebuild the image from source:

```sh
python3 render.py   # writes entry.png
```

## License

MIT — see `LICENSE`.
