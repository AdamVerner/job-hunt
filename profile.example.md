# Profile

Copy this file to `profile.md` and fill it in, or ask Claude: "draft my profile.md from my CV".
`profile.md` is gitignored. `/scan` reads it on every run.

## Tracker
- URL: (left empty - `/scan` publishes the tracker on first run and writes the URL here)

## About me
- CV: `cv.pdf` (in this folder, gitignored; read only when drafting or updating this profile)
- Current role and seniority:
- Strongest skills:
- Preferred skills:
- Spoken languages:

## Hard filters
A job failing any of these is saved as `dropped` with the reason.
- Location: e.g. Prague on-site or hybrid; fully remote from EU
- Pay floor: e.g. 100k CZK/month gross employment, or 6k CZK/day contract
- Dealbreakers: e.g. 4+ days a week in office
- Contract form: employment / contract / both

## Search terms
Keywords used on every source, e.g. python, .NET, C#, backend, fullstack

## Ranking (most important first)
Used to score 1-5. Example:
1. Pay at or above the floor (unknown pay is neutral, flagged)
2. Interesting engineering
3. Prefer C# over Python
4. Prague over remote at equal pay

## Flags
Shown on the row, not a reason to drop. Example:
- No pay stated
- Office policy unclear
- Direct foreign employment without Czech payroll or EOR (tax and social-insurance admin falls on you)
