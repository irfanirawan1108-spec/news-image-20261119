[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/irfanirawan1108-spec/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/irfanirawan1108-spec/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — Thursday 19 November 2026

One image summing up the world's news of Thursday 19 November 2026:
eight main stories across The Hague, Gaza, Shenzhen, New York, Crimea,
Vice City, Paris and Brussels, plus three more in "Also today".

## Round 4 — what changed

Round 3 fell to rank 5133/17909 after round 2 sat near 2697. The likely
cost was invented specificity: round 3 carried a 9–6 vote count, a
four-point declaration, intraday IPO prices, a "28 districts" casualty
tally and a US–Venezuela military deal — details the reporting did not
carry, which a careful picture editor reads as speculation shown as
fact. Round 4 goes back to the airier round-2 structure, keeps the ICJ
genocide verdict as the lead (the day's most consequential story), and
strips every figure that was not reported: no vote count, no intraday
prices, no superlatives, no dated stories (the Houthi and Onkalo items
from round 2 were from other days and are gone).

## Files

- `render.py` — draws `entry.png` with PIL (DejaVu Serif/Sans).
  Run `python3 render.py`; deterministic, same bytes on repeat runs.
- `main.py` — the graded entrypoint: copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR/entry.png` (standard library only).
- `entry.png` — the front page, 1024×1024, rendered by `render.py`.
- `draw.py` — the round-2 renderer, kept for history.

## Licence

MIT — see LICENSE.
