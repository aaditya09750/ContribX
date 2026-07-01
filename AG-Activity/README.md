# AG-Activity

This directory is the **commit target** for the GitHub Activity Generator script. When `contribute.py` runs, it appends timestamped entries to the `README.md` file inside this folder, creating real Git commits that populate your GitHub Contributions Graph.

---

## How It Works

The `contribute.py` script (located in `ag-activity-gen-main/`) generates commits by:

1. **Appending a line** to `AG-Activity/README.md` with a timestamp (e.g., `Contribution: 2026-07-01 14:30`)
2. **Staging the change** with `git add .`
3. **Creating a commit** with a backdated `--date` flag so the commit appears on the desired day
4. **Repeating** for every day in the configured date range (default: last 365 days), with a random number of commits per day

Each commit is a real Git commit with a past date, so GitHub renders them on your Contributions Graph as if they happened on those days.

```text
How a single commit cycle works:

contribute.py
    │
    ├─► Appends "Contribution: 2026-03-15 20:07" to AG-Activity/README.md
    ├─► git add .
    └─► git commit -m "Contribution: 2026-03-15 20:07" --date="2026-03-15 20:07:00"
         │
         └─► GitHub sees this as a commit made on March 15, 2026
```

---

## Setup Guide

### Prerequisites

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **Git 2.x+** — [Download](https://git-scm.com/downloads)
- A GitHub account with SSH or HTTPS access configured

### Step 1 — Clone the Repository

```bash
git clone https://github.com/aaditya09750/AG-ActivityGen.git
cd AG-ActivityGen
```

### Step 2 — Run the Script

**Option A: Generate commits and push automatically**

```bash
python ag-activity-gen-main/contribute.py --path=./AG-Activity --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

This will:
- Find the Git root (the `AG-ActivityGen/` directory)
- Generate backdated commits by appending lines to `AG-Activity/README.md`
- Push all commits to the remote repository

**Option B: Generate commits locally (no auto-push)**

```bash
python ag-activity-gen-main/contribute.py --path=./AG-Activity
```

Then push manually when ready:

```bash
git push origin main
```

### Step 3 — Customize (Optional)

```bash
# Fewer commits, 60% of days, skip weekends
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --max_commits=5 \
  --frequency=60 \
  --no_weekends \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

```bash
# Only the last 30 days + 10 days into the future
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --days_before=30 \
  --days_after=10 \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

```bash
# Override Git identity for this run
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --user_name="Aaditya Gunjal" \
  --user_email="aadigunjal0975@gmail.com" \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

### Step 4 — Verify

1. Wait 2–5 minutes for GitHub to reindex
2. Visit your [GitHub profile](https://github.com/aaditya09750) and check the Contributions Graph
3. If using a private repo, ensure private contributions are visible in your [profile settings](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile)

---

## CLI Quick Reference

| Flag | Default | What it does |
| ---- | ------- | ------------ |
| `--path` | — | Points to this `AG-Activity/` directory as the commit target |
| `--repository` | — | Remote URL; if set, script pushes after generating |
| `--max_commits` | 10 | Max commits per day (1–20, randomized) |
| `--frequency` | 80 | % of days that get commits |
| `--no_weekends` | false | Skip Sat/Sun |
| `--days_before` | 365 | How many days back from today to start |
| `--days_after` | 0 | How many days into the future to commit |
| `--user_name` | git config | Override Git user.name |
| `--user_email` | git config | Override Git user.email |

---

## What This File Looks Like After Running

After the script runs, this README will have appended contribution entries like:

```text
Contribution: 2026-01-15 20:00

Contribution: 2026-01-15 20:01

Contribution: 2026-01-15 20:02

Contribution: 2026-01-16 20:00

...
```

Each line corresponds to one Git commit with a matching backdated timestamp.

---

## Troubleshooting

**Contributions not showing on GitHub?**

- Wait a few minutes — GitHub reindexes activity periodically
- Ensure your Git email matches your GitHub account email:
  ```bash
  git config --get user.email
  ```
- If using a private repo, enable [private contribution visibility](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile)

**Script errors?**

- Make sure you're running from the repo root (`AG-ActivityGen/`)
- The `--path` must point to a folder inside an initialized Git repository
- Don't use `--path` with an uninitialized repo — clone first, then run

**Need to start fresh?**

- Delete all the appended contribution lines from this file
- Or reset with `git checkout -- AG-Activity/README.md`

---

## License

Part of [AG-ActivityGen](https://github.com/aaditya09750/AG-ActivityGen). Licensed under Apache 2.0.