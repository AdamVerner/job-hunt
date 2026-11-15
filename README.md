# Job hunt

Claude Code scans job sites and scores listings against your profile. It keeps them on a small
local tracker board, where you log each application.

## Setup

1. Put your CV (PDF) in this folder. `*.pdf` is gitignored.
2. In Claude Code, run: `draft my profile.md from my CV using profile.example.md`. Then edit what it got wrong:
   location, pay floor, dealbreakers, ranking.
3. Start the tracker: `docker compose up -d`, or `python3 tracker/server.py` without Docker (Python 3.10+, no dependencies).
   It serves the board on http://127.0.0.1:20210. Jobs live in `~/data/job-hunt/jobs.json`; set `DATA_DIR` to move them.
4. Run `/scan`.

To open the board from your phone, put the port behind something private, such as `tailscale serve`.
The server has no login, so never expose it publicly.

## Use

- `/scan` - fetch new listings from every source in `sources.md`, score them, add them to the tracker.
- On the tracker page, open a row to change its status and add notes.
- Or tell Claude, for example "applied to Acme, recruiter call Tuesday", and it updates the row.
- Backups: every `/scan` first copies `jobs.json` to `backups/` (gitignored). Back up anytime with `python3 tracker/server.py backup`.
- Test: `cd tracker && python3 -m unittest test_server`.

## Your own expectations

Everything personal is in `profile.md`:
- **Search:** city, remote scope and search terms
- **Dealbreakers:** jobs that never reach the board
- **Preferences:** set the 1-5 score
- **Flags:** labels shown on rows

Keep dealbreakers few. Filter the rest on the board.

`sources.md` has sources that work anywhere, plus a Czech section that is skipped outside Czechia. To add a site for your country, add a row with its search URL.
