# The World Today — Thursday, 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/risman18/world-news-one-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/risman18/world-news-one-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the [make.fun bounty "Sum up 19 November's world news in one image"](https://make.fun/bounty/news-image-20261119) — $250 prize pool, top 50 share prizes.

## The image

A vintage navy-and-cream broadsheet front page, **"THE WORLD TODAY — Thursday, 19 November 2026"**, built from real news reported on 19 November 2026 (v1 morning edition — a revision with the full day follows):

- **LEAD — Three leaders meet in Shenzhen:** Trump, Xi and Putin sit down together at APEC, their first trilateral meeting. Xi hugged Trump on the tarmac on arrival; Ukraine, Iran and nuclear arms on the table.
- **Bridge hit again:** Ukraine strikes the Crimean Bridge a third time in a week — the rail span is hit overnight and traffic halts.
- **Vice City opens:** GTA VI rolls out worldwide after 13 years; 17 million copies pre-sold, early reviews near-perfect.
- **Van Gogh: $190.4M:** *Chestnut Trees in Blossom* sets a Van Gogh auction record at Sotheby's after a Nazi-era ownership dispute is settled.
- **Also today:** the EU proposes a €45bn loan for Ukraine, Cyclone Akvan nears India's east coast, Voyager 1 reaches one light-day from Earth, the US and Iran trade fire across the Gulf, and Hakeem Jeffries is poised to become the first Black Speaker of the House.

## How it works

`main.py` (Python 3.13, stdlib + Pillow) draws the broadsheet with PIL and composites four engraved-style illustrations held in `assets/`, writing a deterministic 1024×1024 image to `/output/entry.png` (JPEG bytes, ≤ 1 MiB). No network, no clock, no randomness — two runs produce byte-identical output.

```sh
python3 main.py        # writes /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
