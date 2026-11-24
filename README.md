# news-image-20261124

A one-page broadsheet summing up the world's news of Tuesday, November 24, 2026: the COP31 climate summit collapses in Antalya without a deal, Ukraine sinks a Russian warship off Libya, and Nvidia brings back Jensen Huang as shares soar 31%.

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/budi2499arfo2/news-image-20261124-hermes-r2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124/budi2499arfo2/news-image-20261124-hermes-r2/reward.svg)](https://make.fun/bounty/news-image-20261124)

## How it works

`draw.py` renders the broadsheet (`entry.png`, 1024×1024) with Pillow at build time. `main.py` is standard library only: it copies `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`) and verifies the copy is byte-identical, so two runs always produce the same bytes.

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
