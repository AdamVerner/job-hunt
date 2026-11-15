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
| `tracker/index.html` | Tracker board: filters, status, application log; phone layout under 700px | yes |
| `tracker/server.py` | Serves the board and a JSON API over `~/data/job-hunt/jobs.json`; `backup` copies it to `backups/` | yes |
| `compose.yaml` | Runs the server on `127.0.0.1:20210`, restarted automatically | yes |

Your CV, `profile.md`, the data and the backups stay local. Each user runs their own server.

## Data

`jobs.json` maps each job id to one document. The page and `/scan` both go through the server's API:
- `GET /api/jobs` lists every job.
- `POST /api/jobs` adds jobs and never overwrites an existing id.
- `PATCH /api/jobs/<id>` changes fields.

Fields:
- `company`, `title`, `links` (a list - the same job on several sites merges into one row)
- `source`, `location`, `office` (on-site / hybrid N days / remote)
- `pay` (raw text), `pay_ok` (yes / no / unknown)
- `score` (1-5), `why` (one line), `flags` (list)
- `status`: new -> interested -> applied -> interview -> offer / rejected / dropped
- `found` (date), `notes` (list of `{date, text}`)

## Scan

1. Fetch the list pages from every source in `sources.md`.
2. Skip jobs already on the board.
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
