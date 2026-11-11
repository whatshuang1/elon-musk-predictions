# Elon Musk predictions dataset

Every dated prediction Elon Musk has made in public, with the deadline he gave, every time he moved it, and what actually happened. Maintained by [twoweeks.lol](https://twoweeks.lol) and synced from the live site every day.

<!-- stats -->
Snapshot 2026-11-11: **354 claims**, 135 deadline moves.

| Verdict | Claims |
|---|---|
| delivered | 50 |
| delivered-late | 78 |
| partial | 16 |
| missed | 73 |
| cancelled | 12 |
| disputed | 1 |
| pending | 124 |

Of the 229 resolved claims, 50 were delivered on time (22%).

By company: Tesla 174, SpaceX 96, xAI 38, General 20, Neuralink 11, X 11, Boring Company 4
<!-- /stats -->

## Timelines

Every dated statement on the most-asked topics, in Musk's own words, with sources. Regenerated daily.

- [Tesla Roadster](timelines/tesla-roadster.md)
- [Humans on Mars](timelines/humans-on-mars.md)
- [Tesla Cybercab](timelines/tesla-cybercab.md)
- [Tesla Optimus](timelines/tesla-optimus.md)
- [Grok 5](timelines/grok-5.md)
- [Tesla Full Self-Driving](timelines/full-self-driving.md)

## Files

| File | One row per | Use it for |
|---|---|---|
| `data/claims.csv`, `data/claims.json` | claim (one promise, e.g. "first Neuralink human implant") | scorecards, on-time rates |
| `data/predictions.csv`, `data/predictions.json` | statement (one time he said it, with a deadline) | quotes, goalpost moves |
| `data/changelog.json` | change on the board | what changed and when |
| `data/schema.json` | field definitions | the meaning of every column |

A **claim** is one promise. A **statement** is one time Musk said it, in his own words, with a deadline. Saying it again with a later date is a **goalpost move**.

Verdicts: `pending`, `delivered`, `delivered-late`, `partial`, `missed`, `cancelled`, `disputed`. How each verdict is decided: [twoweeks.lol/about](https://twoweeks.lol/about/). Every row links to its page on twoweeks.lol, which shows the source for each quote and date.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Use it for anything, including commercial work and journalism. Credit "twoweeks.lol" with a link to https://twoweeks.lol.

## Corrections

Found a wrong date, a missing source or a prediction we missed? Open an issue with a link to the source.
