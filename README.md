# Job hunt

Claude Code scans job sites, scores listings against your profile, and keeps them in a private
tracker page on claude.ai where you log each application.

## Setup

1. Put your CV (PDF) in this folder. `*.pdf` is gitignored.
2. In Claude Code, run: `draft my profile.md from my CV using profile.example.md`. Then edit what it got wrong:
   location, pay floor, dealbreakers, ranking.
3. Run `/scan`. The first run publishes your own tracker page and saves its URL in `profile.md`.

## Use

- `/scan` - fetch new listings from every source in `sources.md`, score them, add them to the tracker.
- On the tracker page, open a row to change its status and add notes.
- Or tell Claude, for example "applied to Acme, recruiter call Tuesday", and it updates the row.

## Your own expectations

Everything personal is in `profile.md`:
- **Search:** city, remote scope and search terms
- **Dealbreakers:** jobs that never reach the board
- **Preferences:** set the 1-5 score
- **Flags:** labels shown on rows

Keep dealbreakers few. Filter the rest on the board.

`sources.md` has sources that work anywhere, plus a Czech section that is skipped outside Czechia. To add a site for your country, add a row with its search URL.
