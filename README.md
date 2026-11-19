# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Revaaa28/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Revaaa28/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

**Concept.** One image that sums up the whole of Thursday 19 November 2026:
a newspaper poster, "THE WORLD IN ONE DAY", with the date in red under the
masthead and 13 stories in a 1 + 3 + 9 structure. The lead story runs as a
hero splash — the first-ever Trump–Xi–Putin trilateral in Shenzhen, on the
APEC sidelines. Three more stories run as pictured panels — GTA VI launching
worldwide after 13 years, the world court delivering its Rohingya-genocide
verdict, and Cyclone Akvan bearing down on India's east coast. Nine more run
as numbered briefs around a dotted world map — Voyager 1 a light-day out,
Canada resetting its China ties, Mélenchon tipped as a possible French
president, India–Japan defence talks, tougher US green-card rules, a drugs
haul in eastern Libya, Somalia's accusation against the UAE, COP31 in
Antalya, and Duckett's 133 in the ODI.

**Design.** Every story is verified against reporting first published on
19 November 2026 (Reuters, AP, People, NASA, the ICJ, India's IMD); where an
event was scheduled for later in the day, the wording says so ("meets today",
"delivers its verdict today") and states no outcome in advance. Every letter
is rendered by code and every illustration is drawn with PIL shapes in
`tools/render.py` — no photos, no copied artwork — so the text is perfectly
legible with zero garbling. Type is kept large on purpose: the masthead, the
hero headline and the panel headlines all still read at 300 px across.
`main.py` (Python 3.13, standard library only) installs the committed
`entry.png` into the output directory; run twice it writes identical bytes.

**Story selection.** The day's most consequential stories, across regions
and fields, not one country's or one beat's:

- *Diplomacy:* Trump, Xi and Putin meet in Shenzhen; Canada resets China ties; India and Japan review defence ties.
- *Law:* the ICJ delivers its verdict in The Gambia's genocide case against Myanmar.
- *Culture / technology:* GTA VI launches worldwide; NASA confirms Voyager 1 one light-day from Earth; the US proposes tougher green-card rules.
- *Weather / disaster:* Cyclone Akvan nears India's east coast; COP31 talks continue in Antalya.
- *Middle East / Africa:* Somalia accuses the UAE of secret military bases; a drugs haul is seized in eastern Libya.
- *Europe / politics:* France's justice minister says Mélenchon could win the presidency.
- *Sport:* Ben Duckett hits 133 in the third ODI against Australia.

**How it is made.** `tools/render.py` draws the poster with PIL
(`entry.png`, 1024×1024, ~135 KB). `main.py` copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
Verify: run `main.py` twice into two directories and compare — the
bytes are identical.

Entry for the make.fun bounty
[news-image-20261119](https://make.fun/bounty/news-image-20261119)
("Sum up 19 November's world news in one image", $250 in prizes).
