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

Sources are tuned for Prague. Edit `sources.md` for another city.
