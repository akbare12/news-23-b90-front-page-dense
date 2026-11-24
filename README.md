# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b90-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b90-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page front page summing up 23 November 2026's world news in a single
1024×1024 image: 31 stories across 6 regions.

## The day in brief

- **AI rout hits Asia** — the Kospi closes −3.3% at 4,708.54, shedding 161
  points after an intraday −5.8% slide; Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — at the Bridgetown summit,
  150 delegates back a risk framework (a blueprint, not a treaty).
- **US lead over China at record low** — Asia Power Index 2026: US 78.9,
  China 73.6, a 5.3 gap, the narrowest since 2018; India third at 40.5.

Below the heroes: 10 more stories, a world map with numbered pins, 18 more
items in "ALSO ON MONDAY", and a DATE CHECK box that keeps stories from other
days out of the 23 November record.

## How to render

```sh
python3 draw.py        # regenerates entry.png (PIL)
python3 main.py        # stdlib-only: copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` uses only the standard library (it parses the PNG header with
`struct` and checks chunk CRCs); it never writes next to itself, so it also
runs from a read-only copy of this repo.

## Sources

Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy
Institute (Asia Power Index 2026). Chips: REPORTED = confirmed by wires;
CLAIM = one side's claim, not independently confirmed.
