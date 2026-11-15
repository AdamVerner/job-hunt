---
description: Scan job sites, score new listings against profile.md, add them to the tracker
---

Read `profile.md` and `sources.md`. If `profile.md` is missing, stop and offer to draft it from the user's CV using `profile.example.md`.

## 1. Tracker

The tracker is `tracker/server.py`, serving the board and a JSON API on the URL in `profile.md` (default `http://127.0.0.1:20210`).
- If `curl -sf <url>/api/jobs` fails, start it with `docker compose up -d`, or `python3 tracker/server.py &` without Docker.
- Back up before writing anything: `python3 tracker/server.py backup` (prints the backup path).
- `GET <url>/api/jobs` lists every job. Their `id`s are the jobs already seen.

## 2. Collect (one subagent per source, in parallel)

Run collectors with `model: "sonnet"`. In a side-by-side run on one source, Haiku dropped required fields and used more tokens. Scoring stays in the main session so scores stay consistent.

Run one more collector for the companies in `companies.md` (the section for the profile's city, plus Remote) and the profile's own Companies to watch, minus the profile's Skip list. It takes every engineering opening there, judged by the same dealbreakers but not filtered by search terms.

Give each subagent:
- its row from `sources.md`
- the Search section and the Dealbreakers from `profile.md`
- the seen doc ids

Each subagent:
1. Reads the list pages for every search term.
2. Drops jobs whose doc id is already seen, jobs outside the city and remote scope, and jobs that clearly hit a dealbreaker. Never drop for a preference: office policy, stack preference and domain are judged later.
3. Opens each survivor's detail page and extracts pay and office policy.
4. Returns JSON only, one object per job:
   `{id, company, title, link, source, location, office, pay, stack, description_summary}`
   - `stack`: the main languages or platforms the job needs, most important first, with canonical names: Python, C#, Java, Kotlin, Go, Rust, TypeScript, PHP, Ruby, Elixir, C/C++, Swift. Use .NET -> C# and Node/React -> TypeScript. Anything else goes under its common name.
   - `office`: "on-site", "hybrid N days", "remote", or "unknown"
   - `description_summary`: at most 3 lines on what the work is

   If the source fails (blocked, changed layout), return `{"error": "..."}` instead.

Collect the subagents' JSON into files instead of retyping it. Normalize ids yourself: `<company>--<title>`, ASCII-folded, lowercase, non-alphanumerics -> `-`, cut to 120 chars, with legal suffixes (s.r.o., a.s., Inc.) and any "(...)" stripped from the company. Agents disagree on the format. The same job on two sites gets the same id, so merge it into one job with both links.

## 3. Judge

For each new job:
- **A dealbreaker in `profile.md` applies:** `status: "dropped"`, `why` = the reason.
- **Otherwise:** `status: "new"`, `score` 1-5 by the Preferences in `profile.md`, `why` = one line on what makes it a fit or not. Preferences change the score, never the status. The user filters by status, stack, office and source on the board.
- **Add flags** from the profile's flag list.

Document body:
```json
{"company": "", "title": "", "links": [""], "source": "", "location": "", "office": "",
 "pay": "", "pay_ok": "yes|no|unknown", "stack": [], "score": 3, "why": "", "flags": [],
 "status": "new", "found": "YYYY-MM-DD", "summary": "", "notes": []}
```

Write all new documents, each with its `id`, as one JSON array to a file in the scratchpad. Then `curl -sf -X POST <url>/api/jobs -H 'Content-Type: application/json' --data @<file>`. The server never overwrites an existing id: that job holds the user's status and notes. To change an existing job, for example when the user says they applied, use `PATCH <url>/api/jobs/<id>` with only the changed fields.

## 4. Report

In chat:
- jobs found, new, dropped
- the top 5 new by score, each as one line with a link
- every source that failed and why
- the tracker URL and the backup path
