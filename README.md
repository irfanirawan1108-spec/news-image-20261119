# news-image-20261119 — The World in One Day

Entry for make.fun bounty
[`news-image-20261119`](https://make.fun/c/news-image-20261119):
sum up the world's news of **Thursday 19 November 2026** in one image.

## The image

A newspaper front page, drawn programmatically and deterministically
with Pillow (`draw.py`), 1024×1024 PNG:

- **Lead — Gaza:** Israeli tanks cross the Gaza ceasefire line in a rare
  ground incursion beyond the Yellow Line.
- **China — Summit:** Trump, Xi and Putin meet in Shenzhen for a rare
  trilateral summit.
- **Ukraine — War:** Crimean Bridge attacked again; traffic halted.
- **Business — Anthropic:** biggest IPO ever at $81.3bn ($83/share,
  trading starts Thursday on Nasdaq as ANT).
- **Justice — The Hague:** ICJ delivers its verdict in The Gambia's
  genocide case against Myanmar over the 2017 Rohingya crackdown.
- **Art — New York:** Van Gogh's *Châtaigniers en fleurs* sells for a
  record $190.4m at Sotheby's.
- **Culture — Gaming:** GTA VI begins its global rollout; gamers enter
  Vice City.
- **Energy — Finland:** world's first spent-fuel repository opens at
  Onkalo.
- **War — Yemen:** Houthi rocket kills 53 soldiers at a government
  army camp.
- **Also:** Australia sanctions Israeli settlers; EU proposes a €45bn
  Ukraine loan; Cyclone Akvan nears India's coast; Russian arrested
  over Palantir spying.

## How it runs

`main.py` (Python 3.13, standard library only) copies the image held in
this repository to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).
No network, no randomness — the same bytes every run.

Rebuild the image from source:

```sh
python3 draw.py   # writes entry.png
```

## License

MIT — see `LICENSE`.
