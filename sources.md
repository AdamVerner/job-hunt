# Sources

Every source works without login. Never log in to LinkedIn: it restricts accounts it catches automating.
`{q}` is a search term from `profile.md`, URL-encoded.

| Source | List URL | Detail page | Read with | Notes |
|---|---|---|---|---|
| LinkedIn | `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={q}&location=Prague&start=0` (pages of 10: start=10, 20...) | `linkedin.com/jobs/view/<id>` | fetch | Cards lack pay and office policy; the detail page has the full text. For EU remote add `&f_WT=2&location=European%20Union`. |
| jobs.cz | `https://www.jobs.cz/prace/praha/?q[]={q}` | `/rpd/<id>/` | fetch | Some details redirect to a company subdomain (`*.jobs.cz`); follow it. |
| jobstack.it | `https://www.jobstack.it/it-jobs/<category>/praha`, categories: `python-developer`, `net-developer`, `backend-developer`, `fullstack-developer` | `/it-job/<category>/<hash>` | fetch | List shows level, pay, Hybrid/Remote. Category names besides `python-developer` are unverified. |
| cocuma.cz | `https://www.cocuma.cz/jobs/`, `/jobs/page/<n>/` | `/job/<slug>/<id>/` | fetch | Search params are ignored; browse and filter by title. Small (~265 jobs). |
| startupjobs.cz | `https://www.startupjobs.cz/nabidky?q={q}` | from the page | browser (Playwright) | Listings render in JavaScript; a plain fetch returns an empty shell. Unverified. |
| HN Who is hiring | `https://hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring&query=hiring` -> newest "Who is hiring?" story; comments via `https://hn.algolia.com/api/v1/items/<id>` | the comment | fetch (JSON) | One thread per month; scan only top-level comments mentioning remote/EU/Prague. |
| RemoteOK | `https://remoteok.com/api` | `url` field | fetch (JSON) | First element is metadata. Filter by `tags` and `location`. Low yield. |

Not used: Wellfound (generic sample without login), WeWorkRemotely (403).
