# The World Today

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Kkajasd/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Kkajasd/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Saturday 21 November 2026 in one image: a newspaper front page with the
day's most consequential stories — Iran's strikes on US bases in Bahrain,
the Russian missile on Kryvyi Rih, the AI stock sell-off, COP31 in
overtime, the capture of cartel boss Chapo Isidro, and twenty-four more
stories from around the world. Every story is verified against wire
reporting; see SOURCES.md.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` runs `tools/draw_frontpage.py` (Pillow, system DejaVu fonts, no
network, no clock, no randomness) and writes `entry.png` (1024x1024) to
the output directory. Two runs write byte-identical files.
