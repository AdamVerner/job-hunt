---
description: Scan job sites, score new listings against profile.md, add them to the tracker
---

Read `profile.md` and `sources.md`. If `profile.md` is missing, stop and offer to draft it from the user's CV using `profile.example.md`.

## 1. Tracker

If `profile.md` has no tracker URL, publish `tracker/index.html` with the Artifact tool:
- `capabilities: {"db": {}}`
- `icon: "briefcase"`

Then write the returned URL into `profile.md`.

List the tracker's `jobs` collection with the ArtifactData tool, reading every page. Keep the existing doc ids: these are the jobs already seen.

## 2. Collect (one subagent per source, in parallel)

Run collectors with `model: "haiku"`: the work is mechanical, and collection is most of a scan's tokens. Scoring stays in the main session so scores stay consistent.

Give each subagent:
- its row from `sources.md`
- the search terms, hard filters and location from `profile.md`
- the seen doc ids

Each subagent:
1. Reads the list pages for every search term.
2. Drops jobs whose doc id is already seen, then obvious mismatches by title, seniority or location.
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
- **Hard filters fail** (pay range top below the floor, dealbreaker office policy, wrong location or seniority): `status: "dropped"`, `why` = the reason.
- **Otherwise:** `status: "new"`, `score` 1-5 by the ranking in `profile.md`, `why` = one line on what makes it a fit or not.
- **Add flags** from the profile's flag list.

Document body:
```json
{"company": "", "title": "", "links": [""], "source": "", "location": "", "office": "",
 "pay": "", "pay_ok": "yes|no|unknown", "stack": [], "score": 3, "why": "", "flags": [],
 "status": "new", "found": "YYYY-MM-DD", "summary": "", "notes": []}
```

Write each document to a JSON file in the scratchpad. Then write them with ArtifactData `batch`, using `set` and `file_path` per entry, at most 50 per batch. Never overwrite an existing doc: it holds the user's status and notes.

## 4. Report

In chat:
- jobs found, new, dropped
- the top 5 new by score, each as one line with a link
- every source that failed and why
- the tracker URL
