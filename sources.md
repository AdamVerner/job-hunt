# Sources

Every source works without login. Never log in to LinkedIn: it restricts accounts it catches automating.

Placeholders, filled from `profile.md` > Search:
- `{q}`: a search term, URL-encoded.
- `{city}`: the city name in English, e.g. Prague.
- `{city_cz}`: the Czech URL slug, e.g. praha, brno.

## Anywhere

| Source | List URL | Detail page | Read with | Notes |
|---|---|---|---|---|
| LinkedIn | `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={q}&location={city}&start=0` (pages of 10: start=10, 20...) | `linkedin.com/jobs/view/<id>` | fetch | Cards lack pay and office policy; the detail page has the full text. For remote add `&f_WT=2` and set `location` to the remote region, e.g. `European%20Union`. |
| HN Who is hiring | `https://hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring&query=hiring` -> newest "Who is hiring?" story; comments via `https://hn.algolia.com/api/v1/items/<id>` | the comment | fetch (JSON) | One thread per month. Scan only top-level comments mentioning remote in the user's region, or `{city}`. |
| RemoteOK | `https://remoteok.com/api` | `url` field | fetch (JSON) | Remote only. First element is metadata. Filter by `tags` and `location`. Low yield. |

## Czech Republic

Skip this section when the profile's city is not in Czechia.

| Source | List URL | Detail page | Read with | Notes |
|---|---|---|---|---|
| jobs.cz | `https://www.jobs.cz/prace/{city_cz}/?q[]={q}` | `/rpd/<id>/` | fetch | Some details redirect to a company subdomain (`*.jobs.cz`); follow it. |
| jobstack.it | `https://www.jobstack.it/it-jobs/<category>/{city_cz}`, categories such as `python-developer`, `dot-net-developer`, `java-developer`, `full-stack-developer` | `/it-job/<category>/<hash>` | fetch | List shows level, pay, Hybrid/Remote. An unknown category returns the generic city list, not a 404; check category names on the site. |
| cocuma.cz | `https://www.cocuma.cz/jobs/`, `/jobs/page/<n>/` | `/job/<slug>/<id>/` | fetch | Search params are ignored; browse all pages and filter by title and location. Small (~265 jobs). |
| startupjobs.cz | `POST https://back.startupjobs.cz/api/search-offers?page=N`, JSON body `{"query":"{q}","locationPreferences":["remote","hybrid","onsite"],"locations":[{"locationId":"<id>","radiusKm":20}]}` | `GET https://back.startupjobs.cz/api/offers/{id}`; public link `https://www.startupjobs.cz/nabidka/{id}/{slug}` | fetch (JSON, curl) | Find `<id>` with `POST https://back.startupjobs.cz/api/search-offers/locations-autocomplete?name={city_cz}&locale=cs&types[]=place`. Prague is `ChIJi3lwCZyTC0cRkEAWZg-vAAQ`. Salary min/max are in hundredths. Search is fuzzy: `.NET` and `C#` return mostly noise. |

Not used: Wellfound (generic sample without login), WeWorkRemotely (403).
