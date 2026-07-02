# ContribX - Activity Log

This directory serves as the **commit target** for the ContribX contribution generator. When `contribute.py` executes, it appends timestamped entries to this `README.md` file, stages the change, and creates a backdated Git commit for each entry. The accumulated commits populate the GitHub Contributions Graph on your profile.

This file is intentionally structured with a documentation header followed by an open-ended commit log section at the bottom. The script appends new entries below the separator, preserving the documentation above while building a continuous activity record.

---

## Purpose

The `AG-Activity/` directory exists for a single, specific purpose: to provide a stable, dedicated file path where the ContribX script writes its generated contribution entries. By isolating the commit target into its own directory, the project separates the tool's source code (in `ag-activity-gen-main/`) from its output (here), keeping the repository structure clean and the commit history attributable to a single file.

---

## How Commits Are Generated

The `contribute.py` script (located in `../ag-activity-gen-main/`) follows this execution cycle for each qualifying day in the configured date range:

```text
Execution Pipeline (per qualifying day):

  contribute.py
      |
      |-- [1] Determine commit count: random integer between 1 and --max_commits
      |
      +-- For each commit on this day:
          |
          |-- [2] Append line to AG-Activity/README.md
          |        Format: "Contribution: YYYY-MM-DD HH:MM"
          |
          |-- [3] Stage all changes
          |        Command: git add .
          |
          +-- [4] Create backdated commit
                   Command: git commit -m "Contribution: YYYY-MM-DD HH:MM"
                                       --date="YYYY-MM-DD HH:MM:SS"
                   |
                   +-- GitHub renders this commit on the specified date
                       in the Contributions Graph
```

**Key technical details:**

- Each commit is a real, valid Git commit object with a deliberately backdated author timestamp.
- GitHub's Contributions Graph reads the commit date (not the push date) when rendering activity squares, so backdated commits appear on their respective historical dates.
- The script generates between 1 and `--max_commits` (default: 10, maximum: 20) entries per qualifying day, with the exact count randomized to produce organic variation.
- A day qualifies for commits only if it passes the frequency probability check (default: 80%) and, if `--no_weekends` is enabled, falls on a weekday.

---

## Setup Guide

### Prerequisites

| Requirement | Minimum Version | Installation |
| ----------- | --------------- | ------------ |
| Python | 3.8 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| Git | 2.x or higher | [git-scm.com/downloads](https://git-scm.com/downloads) |
| GitHub Account | — | SSH or HTTPS authentication must be configured |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/aaditya09750/AG-ActivityGen.git
cd AG-ActivityGen
```

### Step 2 — Run the Script

There are two primary modes of operation. Both generate commits targeting this `AG-Activity/README.md` file.

**Mode A: Generate and push automatically**

This is the recommended approach for most users. The script generates all commits locally and pushes them to the remote repository in a single operation.

```bash
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

Execution summary:
- The script locates the Git root directory (the parent `AG-ActivityGen/` folder).
- For each qualifying day in the date range, it appends a timestamped entry to this file and creates a backdated commit.
- After all commits are generated, it configures the remote origin and pushes the `main` branch.

**Mode B: Generate locally, push manually**

Use this mode if you want to inspect the generated commits before pushing, or if you prefer to push from a different environment.

```bash
python ag-activity-gen-main/contribute.py --path=./AG-Activity
```

Inspect the generated commits:

```bash
git log --oneline -20
```

Push when satisfied:

```bash
git push origin main
```

### Step 3 — Customize the Generation Parameters

All parameters are optional. The defaults produce a realistic, dense contribution graph spanning the last 365 days.

**Reduced density with weekend exclusion:**

```bash
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --max_commits=5 \
  --frequency=60 \
  --no_weekends \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

**Targeted 30-day historical window with 10-day forward extension:**

```bash
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --days_before=30 \
  --days_after=10 \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

**Git identity override for single execution:**

```bash
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --user_name="Aaditya Gunjal" \
  --user_email="aadigunjal0975@gmail.com" \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

### Step 4 — Verify the Results

1. Allow 2 to 5 minutes for GitHub to reindex contribution activity.
2. Navigate to your [GitHub profile](https://github.com/aaditya09750) and inspect the Contributions Graph.
3. If the repository is private, confirm that private contribution visibility is enabled in your [profile settings](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile).
4. Verify that your local Git email matches your GitHub account email:
   ```bash
   git config --get user.email
   ```

---

## CLI Quick Reference

| Flag | Long Form | Type | Default | Description |
| ---- | --------- | ---- | ------- | ----------- |
| `-p` | `--path` | str | none | Path to this `AG-Activity/` directory (or any directory inside a Git repo). The script locates the nearest parent `.git` root automatically. |
| `-r` | `--repository` | str | none | Remote repository URL (SSH or HTTPS). When provided, the script pushes all generated commits after generation completes. |
| `-mc` | `--max_commits` | int | 10 | Maximum number of commits per qualifying day (1-20). The actual count is randomized daily for organic variation. |
| `-fr` | `--frequency` | int | 80 | Percentage probability (0-100) that any given day in the range receives commits. |
| `-nw` | `--no_weekends` | flag | false | Suppresses all commit generation on Saturdays and Sundays. |
| `-db` | `--days_before` | int | 365 | Number of days before the current date to begin the commit generation window. |
| `-da` | `--days_after` | int | 0 | Number of days after the current date to extend the commit generation window. |
| `-un` | `--user_name` | str | git config | Overrides the Git `user.name` configuration for this execution only. |
| `-ue` | `--user_email` | str | git config | Overrides the Git `user.email` configuration for this execution only. Must match the email on the target GitHub account. |

---

## Troubleshooting

### Contributions Not Appearing on the GitHub Graph

GitHub reindexes contribution activity periodically. After pushing commits, wait 2 to 5 minutes before checking your profile. Verify that the repository contains the expected commits locally:

```bash
git log --oneline -10
```

### Private Repository Contributions Not Visible

By default, GitHub does not display contributions to private repositories on your public profile. Enable this in your GitHub settings by following the [official guide](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile).

### Email Address Mismatch

GitHub attributes contributions only when the commit email matches an email registered on your account. Check and update if necessary:

```bash
# Verify current Git email
git config --get user.email

# Update to match your GitHub account
git config --global user.email "your-github-email@example.com"
```

Alternatively, use the `--user_email` flag to set the correct email for a single script execution without modifying global Git settings.

### Script Errors

- Ensure you are running the script from the repository root directory (`AG-ActivityGen/`).
- When using `--path`, the specified directory must exist and reside inside an initialized Git repository.
- Do not use `--path` pointing to a directory outside any Git repository; the script will exit with a descriptive error.

### Resetting This File

To remove all generated entries and start with a clean state:

```bash
git checkout -- AG-Activity/README.md
```

This restores the file to its last committed version, discarding all uncommitted appended entries.

---

## License

Part of [ContribX](https://github.com/aaditya09750/AG-ActivityGen). Licensed under the Apache License 2.0.

---

## Commit Activity Log

The section below is the designated target area for the ContribX script. When `contribute.py` executes, all generated contribution entries are appended sequentially below this line. Each entry corresponds to a single Git commit with a matching backdated timestamp.

Do not manually edit the content below this separator. The script manages this section automatically.

---
Contribution: 2026-07-02 20:00

Contribution: 2026-07-02 20:01

Contribution: 2026-07-02 20:00

Contribution: 2026-07-02 20:01

Contribution: 2026-07-02 20:02

Contribution: 2026-07-02 20:00

