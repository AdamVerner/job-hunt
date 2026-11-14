# Job hunt tracker - design

## Goal

Scan job sites, keep the listings that fit one person's profile, show them in one table,
and log each application. Anyone can clone the repo and use it for their own search.

## Shape

Claude Code does the work. There is almost no code.

| Piece | What it is | In git? |
|---|---|---|
| `profile.example.md` | Template for a personal profile | yes |
| `profile.md` | Your filters, ranking rules, CV path, tracker URL | no |
| `sources.md` | Per-site URLs and how to read each site | yes |
| `.claude/commands/scan.md` | The `/scan` procedure | yes |
| `tracker/index.html` | Tracker page, published as a private claude.ai Artifact with a database | yes |

Your CV and `profile.md` stay local. Each user publishes their own copy of the tracker,
so nobody's data touches anyone else's.

## Data

The tracker page's database has one collection, `jobs`, with one document per job.
The page and Claude read and write the same rows.

Fields:
- `company`, `title`, `links` (a list - the same job on several sites merges into one row)
- `source`, `location`, `office` (on-site / hybrid N days / remote)
- `pay` (raw text), `pay_ok` (yes / no / unknown)
- `score` (1-5), `why` (one line), `flags` (list)
- `status`: new -> interested -> applied -> interview -> offer / rejected / dropped
- `found` (date), `notes` (list of `{date, text}`)

## Scan

1. Fetch the list pages from every source in `sources.md`.
2. Skip jobs already in the database.
3. Cut obvious mismatches by title and location.
4. Open the detail page of each survivor; extract pay and office policy.
5. Apply the dealbreakers. Rejected jobs are saved as `dropped` with a reason so they don't return.
6. Score the rest and write them in one batch.
7. Report: how many are new, the top 5, and any source that failed. A failing source doesn't stop the scan.

## Sources

| Source | Method |
|---|---|
| LinkedIn | Logged-out guest endpoint. Never log in: LinkedIn restricts accounts it catches automating. |
| jobs.cz, jobstack.it, cocuma.cz | Plain fetch |
| startupjobs.cz | Playwright (listings load in JavaScript) |
| HN "Who is hiring" | Algolia JSON API, once a month |
| RemoteOK | JSON API |

Wellfound shows only a generic sample without a login, and WeWorkRemotely returns 403, so neither is used.

## Later

- Run the scan on a schedule, using cron with `claude -p /scan`.
- Read job-alert emails through the Gmail connector.

## Testing

Run the first scan. Review its top 20 and its drops with the user. Adjust `profile.md` until the scores match the user's judgment.
