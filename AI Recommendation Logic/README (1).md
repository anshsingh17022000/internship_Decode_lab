# Tech Stack Recommender — DecodeLabs Project 3

A content-based AI recommendation engine that maps a user's raw skills to
the closest-matching job roles, built entirely from first principles
(no scikit-learn, no numpy) so every formula stays visible.

## How it works — the IPO pipeline

```
INPUT (your skills)  -->  PROCESS (TF-IDF + Cosine Similarity)  -->  OUTPUT (Top-3 roles)
```

1. **Ingestion** — you provide 3+ skills (e.g. `Python, Cloud Computing, Automation`)
2. **Vector Mapping** — every skill is mapped into a shared vocabulary space built from `raw_skills.csv`
3. **TF-IDF Weighting** — common skills (like `Git`) are down-weighted; rare, specific skills (like `Terraform`) are up-weighted
4. **Scoring** — Cosine Similarity measures the *angle* between your profile vector and each job role's vector (magnitude-independent, so a short profile can still score high)
5. **Sorting** — roles are ranked by descending similarity score
6. **Filtering** — only the Top-N roles are shown, to avoid choice overload

It also handles the **Cold Start problem**: if none of your input skills are
recognized, the engine falls back to a trending/popular roles list instead
of returning all-zero matches.

## Files

| File              | Purpose                                                          |
|-------------------|-------------------------------------------------------------------|
| `raw_skills.csv`  | The item dataset — 17 job roles, each tagged with its core skills |
| `recommender.py`  | The engine: vocabulary building, TF-IDF, cosine similarity, 4-step ranking pipeline |
| `main.py`         | CLI front-end (interactive or one-shot mode)                     |

## Usage

```bash
# Interactive mode
python main.py

# One-shot mode
python main.py --skills "Python,Cloud Computing,Automation"

# Show every skill tag the engine understands
python main.py --list-skills

# Change how many results come back (default 3)
python main.py --skills "Java,SQL,APIs" --top 5
```

## Example output

```
TOP MATCHES (ranked by Cosine Similarity / angular alignment):

  1. Network Engineer         [#########...........]  46.8%
     matched on: automation, cloud computing
  2. Cloud Architect          [######..............]  33.3%
     matched on: automation, cloud computing
  3. DevOps Engineer          [######..............]  32.3%
     matched on: automation, cloud computing
```

## Extending it

- Add more roles/skills to `raw_skills.csv` — no code changes needed.
- Swap `TRENDING_FALLBACK` in `recommender.py` for a real popularity metric.
- Add a rating/feedback loop (mentioned in the kit's conclusion) by storing
  which recommendations users picked, then boosting those skill weights.
