# ContribX - Professional Upgrade Roadmap

A complete phase-wise upgrade plan to transform ContribX from a command-line commit generator into a professional-grade GitHub profile management platform.

---

## Overview

ContribX currently operates as a single Python script that generates backdated Git commits with configurable parameters. The roadmap below outlines 25 features across 6 phases, each building on the previous one. The progression follows a clear arc:

```text
Phase 1: Make the existing tool reliable and professional
Phase 2: Add visual capabilities that no competitor has
Phase 3: Add intelligence that makes output indistinguishable from real activity
Phase 4: Wrap everything in professional interfaces
Phase 5: Distribute to the global developer ecosystem
Phase 6: Build community and engagement around the tool
```

**Current state:** CLI script with basic randomized commit generation.
**Target state:** A full platform with visual graph design, intelligent pattern generation, multi-interface access (CLI, TUI, Web, GitHub Action), and global distribution via PyPI and Docker.

---

## Phase 1 — Foundation Hardening

**Goal:** Make the existing tool production-ready. Every feature in this phase is a quick win that immediately improves the user experience without requiring architectural changes.

**Estimated effort:** 1-2 weeks

### 1.1 Dry Run Mode

A `--dry-run` flag that simulates the entire execution without creating any commits. Outputs a detailed summary of what would happen: number of commits, which days, timestamp distribution, and total file size impact.

```bash
python contribute.py --dry-run --days_before=30 --frequency=70
```

```text
Dry run summary:
  Date range        : 2026-06-02 to 2026-07-02
  Qualifying days   : 21 / 30 (70.0%)
  Total commits     : 134
  Weekend commits   : 0 (--no_weekends active)
  Avg commits/day   : 6.4
  Estimated duration: ~45 seconds
```

**Value:** Eliminates trial-and-error. Users verify output before any irreversible commits are made.

---

### 1.2 Configuration File Support

Allow users to save their preferred settings in a `.contribx.yml` file. The CLI reads this file automatically if present in the working directory, with explicit flags overriding file values.

```yaml
# .contribx.yml
max_commits: 8
frequency: 65
no_weekends: true
days_before: 365
days_after: 0
user_name: "Your Name"
user_email: "you@example.com"
repository: "git@github.com:user/repo.git"
```

```bash
# Uses .contribx.yml automatically
python contribute.py

# Explicit config path
python contribute.py --config ./profiles/aggressive.yml

# CLI flags override config file values
python contribute.py --frequency=100
```

**Value:** Eliminates repetitive long commands. Users save their preferred profile once and reuse it. Enables maintaining multiple named profiles (conservative.yml, aggressive.yml, weekday-only.yml).

---

### 1.3 Undo and Rollback

A `--undo` command that identifies all ContribX-generated commits by their message pattern (`Contribution: YYYY-MM-DD HH:MM`) and cleanly removes them using an interactive rebase or filter-branch operation.

```bash
# Preview what would be removed
python contribute.py --undo --dry-run

# Execute the rollback
python contribute.py --undo

# Rollback only commits from a specific date range
python contribute.py --undo --after=2026-06-01 --before=2026-07-01
```

**Value:** Makes ContribX completely safe to experiment with. No other activity generator offers a clean rollback mechanism.

---

### 1.4 Commit Message Customization

Replace the generic `Contribution: YYYY-MM-DD HH:MM` format with configurable templates or realistic developer commit messages.

**Template mode:**
```bash
python contribute.py --message-template="chore: daily update {date}"
```

**Realistic mode:**
```bash
python contribute.py --realistic-messages
```

Generates messages like:
- `fix: resolve null pointer in user auth module`
- `feat: add pagination to dashboard endpoint`
- `refactor: extract validation logic into utility`
- `docs: update API reference for v2 endpoints`
- `test: add coverage for edge cases in parser`

Ships with a curated dictionary of 500+ realistic commit messages across fix, feat, refactor, docs, test, chore, and style categories.

**Value:** If anyone inspects the generated repository, the commit history looks like genuine development work instead of an obvious pattern.

---

### 1.5 Progress Bar and Colored Output

Replace silent execution with a rich terminal output using colored text, a progress bar, and a post-execution summary.

```text
ContribX v2.0 — Generating contributions

  Configuration
    Date range   : 2026-07-02 to 2025-07-02 (365 days)
    Frequency    : 80%
    Max commits  : 10/day
    Weekends     : excluded
    Repository   : git@github.com:user/repo.git

  Generating commits
    [========================================] 100%  287/287 commits

  Summary
    Days with commits : 248 / 365
    Total commits     : 287
    Longest streak    : 14 days
    Push status       : success (main -> origin)
    Duration          : 1m 23s
```

**Value:** Professional tools communicate clearly. Silent scripts feel broken; progress feedback builds confidence.

---

## Phase 2 — Visual Capabilities

**Goal:** Add features that make ContribX visually unique. This is the phase that differentiates ContribX from every other activity generator on the market.

**Estimated effort:** 3-4 weeks

### 2.1 Terminal Graph Preview

Before generating any commits, render a visual preview of the contribution graph directly in the terminal. Use colored Unicode blocks to simulate the GitHub grid, showing exactly what the profile will look like.

```bash
python contribute.py --preview --days_before=365 --frequency=70
```

```text
  Contribution Graph Preview (365 days, 70% frequency)

        Jan     Feb     Mar     Apr     May     Jun
  Mon   .  ##  .  ##  ##  .  .  ##  ##  ##  .  .
  Tue   ##  ##  .  .  ##  .  ##  ##  .  ##  ##  .
  Wed   .  ##  ##  .  .  ##  ##  .  ##  .  ##  ##
  Thu   ##  .  ##  ##  .  ##  .  ##  ##  .  .  ##
  Fri   .  ##  .  ##  ##  .  ##  .  .  ##  ##  .
  Sat   .  .  .  .  .  .  .  .  .  .  .  .
  Sun   .  .  .  .  .  .  .  .  .  .  .  .

  Legend: . = no commits  # = 1-4  ## = 5-10  ### = 11-20

  Generate these commits? [y/n]
```

**Value:** Users see the exact result before committing. Eliminates wasted runs entirely.

---

### 2.2 Text Pattern Designer

Let users spell words, names, or messages directly on the contribution graph. The script maps ASCII characters to a 7-row grid (matching GitHub's 7-day week layout) and generates commits only on the corresponding days.

```bash
python contribute.py --text="HIRE ME" --repository=git@github.com:user/repo.git
```

```bash
python contribute.py --text="2026" --font=bold --repository=git@github.com:user/repo.git
```

Built-in fonts: `default`, `bold`, `thin`, `block`. Each character occupies 5-6 columns on the grid with 1-column spacing.

**Value:** This is the single most viral feature possible. No other tool lets you write text on the GitHub contribution graph. Screenshots of "HIRE ME" written in green squares would spread across developer communities instantly.

---

### 2.3 QR Code on the Contribution Graph

Generate a scannable QR code pattern on the contribution graph. The green squares form a valid QR code that links to any URL (portfolio, LinkedIn, personal site).

```bash
python contribute.py --qr="https://yourportfolio.com" --repository=git@github.com:user/repo.git
```

Technical approach: Use a QR code library to generate the binary matrix, map each 1-bit to a high-commit day and each 0-bit to a zero-commit day. The GitHub graph's 52-column x 7-row grid supports QR codes up to Version 2 (25x25 modules) by mapping module density to commit intensity.

**Value:** A QR code that someone can scan directly from a GitHub profile page is something that has never been done before. This is a portfolio-grade conversation starter.

---

### 2.4 Theme Packs (Pre-Built Patterns)

Ship a library of named visual patterns that produce distinctive, aesthetic contribution graphs without any manual configuration.

```bash
python contribute.py --theme=wave --repository=git@github.com:user/repo.git
python contribute.py --theme=diagonal --repository=git@github.com:user/repo.git
python contribute.py --theme=checkerboard --repository=git@github.com:user/repo.git
python contribute.py --theme=gradient-fade --repository=git@github.com:user/repo.git
python contribute.py --theme=heartbeat --repository=git@github.com:user/repo.git
python contribute.py --theme=binary --repository=git@github.com:user/repo.git
```

Available themes:

| Theme | Visual Description |
| ----- | ------------------ |
| `wave` | Sinusoidal intensity curve across the year |
| `diagonal` | Diagonal stripes from bottom-left to top-right |
| `checkerboard` | Alternating high/low weeks |
| `gradient-fade` | Intensity increases from January to December |
| `heartbeat` | ECG-style pulse pattern repeating monthly |
| `binary` | Random binary blocks resembling machine output |
| `borders` | Only the edges of the graph are filled |
| `cross` | Large centered cross pattern |
| `diamond` | Diamond shape centered on the graph |
| `rain` | Vertical streaks of varying intensity |

**Value:** Instant visual differentiation with zero effort. Users pick a theme and get a distinctive, recognizable profile.

---

### 2.5 Graph Export as Image

Export the current or generated contribution graph as a high-resolution PNG or SVG file. Suitable for embedding in portfolios, resumes, LinkedIn banners, or presentation slides.

```bash
python contribute.py --export=graph.png --days_before=365
python contribute.py --export=graph.svg --days_before=365 --theme=gradient-fade
```

Supports custom color schemes:
```bash
python contribute.py --export=graph.png --colors="dark" --days_before=365
python contribute.py --export=graph.png --colors="#1a1a2e,#16213e,#0f3460,#533483,#e94560"
```

**Value:** GitHub does not natively offer graph export. This fills a real gap for developers building portfolios and resumes.

---

## Phase 3 — Intelligence Layer

**Goal:** Make ContribX output indistinguishable from genuine developer activity. Move from random generation to intelligent, context-aware patterns.

**Estimated effort:** 3-4 weeks

### 3.1 Clone Any GitHub User's Graph

Input any public GitHub username and ContribX reads their contribution graph via the GitHub API, then replicates the exact same pattern on your account.

```bash
python contribute.py --clone-user=torvalds --repository=git@github.com:user/repo.git
```

The script:
1. Fetches the target user's contribution data from the GitHub GraphQL API
2. Maps each day's contribution level (0-4) to a proportional commit count
3. Generates commits matching the exact pattern

**Value:** Want a graph that looks like a senior engineer at a top company? Clone it. This is powerful and unique.

---

### 3.2 Gap Filler — Enhance Your Real Graph

Connect to the GitHub API, read the authenticated user's actual contribution graph, identify empty days, and generate commits only for the gaps. This turns a patchy, real graph into a complete, consistent one without overwriting existing activity.

```bash
python contribute.py --fill-gaps --github-token=ghp_xxxx --repository=git@github.com:user/repo.git
```

Options:
```bash
# Fill only weekday gaps
python contribute.py --fill-gaps --no_weekends --github-token=ghp_xxxx

# Fill gaps but keep intensity proportional to surrounding days
python contribute.py --fill-gaps --match-intensity --github-token=ghp_xxxx

# Fill gaps only in the last 90 days
python contribute.py --fill-gaps --days_before=90 --github-token=ghp_xxxx
```

**Value:** Instead of generating an entirely fake history, this enhances a real one. The result is subtle and undetectable — it looks like you simply had fewer off-days than you actually did.

---

### 3.3 Realistic Developer Patterns

Replace pure random generation with intelligent patterns that mimic how real developers actually work:

- **Work-hour clustering:** 70% of commits fall between 9 AM and 7 PM, 20% in evening hours, 10% late night. Mimics genuine developer rhythm.
- **Sprint simulation:** 2-3 week bursts of high activity (8-15 commits/day) followed by 3-5 day cool-down periods (1-3 commits/day). Mirrors real agile sprint cycles.
- **Gradual ramp-up:** Commit frequency starts low in January and increases through the year, simulating a developer gaining momentum on a project.
- **Vacation gaps:** Automatically inserts 1-2 realistic vacation windows (5-14 consecutive zero-commit days) at natural intervals.
- **Monday spike:** Slightly higher commit counts on Mondays (catching up on weekend thoughts), gradual taper through Friday.

```bash
python contribute.py --style=realistic --repository=git@github.com:user/repo.git
python contribute.py --style=sprint-cycle --repository=git@github.com:user/repo.git
python contribute.py --style=ramp-up --repository=git@github.com:user/repo.git
```

**Value:** Random flat-distribution commits are the telltale sign of a generator. Realistic patterns are virtually indistinguishable from genuine activity.

---

### 3.4 Country-Aware Holiday Skipping

Pass a country code and the script automatically skips all national and public holidays for that country. Supports 50+ countries via a built-in holiday calendar database.

```bash
python contribute.py --country=IN --repository=git@github.com:user/repo.git
python contribute.py --country=US --repository=git@github.com:user/repo.git
```

For India (`--country=IN`), automatically skips: Republic Day, Holi, Independence Day, Diwali, Christmas, and all gazetted holidays.

Can combine with `--no_weekends` for maximum realism:
```bash
python contribute.py --country=IN --no_weekends --style=realistic
```

**Value:** An activity graph with holiday gaps matching your actual country looks significantly more authentic than one with uniform activity throughout the year.

---

### 3.5 Google Calendar Sync

Connect to Google Calendar and automatically skip days that have events tagged with specific keywords (vacation, PTO, holiday, travel, sick day). The generated graph respects your actual time-off schedule.

```bash
python contribute.py --google-calendar --skip-events="vacation,PTO,holiday" --repository=git@github.com:user/repo.git
```

**Value:** The most realistic possible output — your generated graph aligns perfectly with your actual schedule. If someone cross-references your graph with known company holidays or your travel posts, everything checks out.

---

## Phase 4 — Professional Interfaces

**Goal:** Make ContribX accessible through multiple interfaces — terminal, web, and automated. Each interface serves a different user persona.

**Estimated effort:** 4-5 weeks

### 4.1 Interactive Terminal UI (TUI)

A full-screen terminal interface built with `textual` or `rich` that provides:

- Visual sliders for frequency and max commits
- Live graph preview that updates as parameters change
- Step-by-step guided setup for first-time users
- Color-coded output with progress bars during generation
- Repository management (list, select, configure remotes)

```bash
python contribute.py --interactive
# or
contribx tui
```

**Value:** Transforms ContribX from a script into a polished, professional developer tool. The TUI alone signals that this is a serious project, not a throwaway script.

---

### 4.2 Web-Based Graph Designer

A local web application (Flask or FastAPI) that renders the GitHub contribution grid in a browser. Users interact with the grid visually:

- Click cells to toggle commits on/off
- Drag to paint regions
- Adjust intensity per cell (light/medium/dark green)
- Type text and see it rendered live on the grid
- Import themes and patterns
- Export the design as a CLI command or execute directly

```bash
python contribute.py --web
# Opens http://localhost:8080 with the visual designer
```

**Value:** The ultimate UX for designing contribution graphs. Accessible to non-technical users. This is the feature that converts casual users into fans.

---

### 4.3 Scheduled Daily Execution

A built-in scheduler that installs a recurring task to run ContribX automatically at a configured time each day. Supports cron (Linux/macOS) and Windows Task Scheduler natively.

```bash
# Linux / macOS
python contribute.py --schedule --time="08:00" --max_commits=3 --repository=git@github.com:user/repo.git

# Windows
python contribute.py --schedule --time="08:00" --max_commits=3 --repository=git@github.com:user/repo.git

# Remove the scheduled task
python contribute.py --unschedule
```

**Value:** Set-and-forget contribution maintenance. Ensures a permanent streak without any manual intervention.

---

### 4.4 Multi-Repository Distribution

Instead of concentrating all commits in a single repository, distribute them across multiple repositories for a more natural-looking profile. Each repository receives a configurable share of the total commits.

```bash
python contribute.py --repositories="repo1,repo2,repo3" --distribute=even
python contribute.py --repositories="repo1,repo2,repo3" --distribute=weighted
python contribute.py --repositories="repo1,repo2,repo3" --distribute=random
```

Distribution modes:

| Mode | Behavior |
| ---- | -------- |
| `even` | Equal split across all repositories |
| `weighted` | First repo gets 50%, remaining share the rest equally |
| `random` | Each commit is randomly assigned to a repository |
| `round-robin` | Commits cycle through repos in order |

**Value:** A profile with 3000 commits in a single repo and zero activity elsewhere looks suspicious. Distributing across 3-5 repos creates a natural, multi-project developer profile.

---

### 4.5 Streak Insurance

A lightweight background daemon that monitors your GitHub profile once daily. If no real commit has been made by a configurable cutoff time (default: 11:00 PM), it automatically generates a single commit to preserve your contribution streak.

```bash
# Install the streak guardian
python contribute.py --streak-guard --cutoff="23:00" --repository=git@github.com:user/repo.git

# Check status
python contribute.py --streak-status

# Disable
python contribute.py --streak-guard --disable
```

**Value:** Contribution streaks are a point of pride for many developers. This feature acts as a safety net — your streak is protected even on days you forget to commit.

---

## Phase 5 — Ecosystem Distribution

**Goal:** Make ContribX available to the global developer community through standard distribution channels. Reduce the barrier to entry from "clone a repo and run a script" to "one command to install, one command to run."

**Estimated effort:** 2-3 weeks

### 5.1 PyPI Package

Publish ContribX as a pip-installable Python package with a proper CLI entry point.

```bash
pip install contribx
contribx --max_commits=8 --frequency=70 --repository=git@github.com:user/repo.git
contribx --text="HELLO" --repository=git@github.com:user/repo.git
contribx --interactive
```

Package structure:
```text
contribx/
+-- __init__.py
+-- cli.py            (argparse entry point)
+-- generator.py      (core commit engine)
+-- patterns.py       (text, QR, themes)
+-- preview.py        (terminal graph renderer)
+-- config.py         (YAML config loader)
+-- fonts/            (character grid definitions)
+-- themes/           (named pattern definitions)
+-- messages/         (realistic commit message banks)
+-- holidays/         (country holiday calendars)
+-- setup.py
+-- pyproject.toml
```

**Value:** Instant global reach. Any developer with Python installed can access ContribX with a single pip command.

---

### 5.2 Docker Image

Package ContribX as a Docker container for zero-dependency, portable execution across any operating system.

```bash
docker run --rm -v ~/.ssh:/root/.ssh contribx --repository=git@github.com:user/repo.git
docker run --rm contribx --text="HELLO" --repository=https://github.com/user/repo.git
```

Published to Docker Hub and GitHub Container Registry.

**Value:** Eliminates all Python version and dependency issues. One command, works identically on any machine.

---

### 5.3 GitHub Action

Create a GitHub Action so users can run ContribX directly from a GitHub workflow on a recurring schedule. Fully serverless — no local machine required.

```yaml
# .github/workflows/contribx.yml
name: Daily Contributions
on:
  schedule:
    - cron: '0 8 * * *'
jobs:
  contribute:
    runs-on: ubuntu-latest
    steps:
      - uses: aaditya09750/contribx-action@v1
        with:
          repository: ${{ github.repository }}
          max_commits: 5
          frequency: 70
          no_weekends: true
          token: ${{ secrets.GITHUB_TOKEN }}
```

**Value:** The most seamless possible experience. Users add a YAML file to their repo and contributions are generated automatically every day by GitHub's own infrastructure. Zero maintenance.

---

### 5.4 NPX One-Liner (Node.js Wrapper)

Create a thin Node.js wrapper that downloads and executes ContribX without requiring Python installation:

```bash
npx contribx --max_commits=8 --frequency=70 --repository=git@github.com:user/repo.git
```

**Value:** Reaches the JavaScript/Node.js developer community who may not have Python installed. Maximizes accessibility.

---

## Phase 6 — Community and Engagement

**Goal:** Build a community around ContribX and create engagement loops that keep users coming back.

**Estimated effort:** 3-4 weeks

### 6.1 Contribution Analytics Dashboard

After each generation, produce a detailed analytics report covering:

- Total commits generated and daily distribution
- Commits per month breakdown (bar chart in terminal)
- Busiest day of the week and busiest month
- Longest streak achieved
- Comparison: before vs. after graph
- Intensity heatmap summary

Export formats: Markdown, JSON, HTML, or rendered directly in the terminal.

```bash
python contribute.py --analytics --days_before=365
python contribute.py --analytics --export=report.html
```

**Value:** Users love data about their own activity. The analytics report is shareable and provides a sense of accomplishment after generation.

---

### 6.2 Public Leaderboard

An opt-in public web leaderboard where ContribX users compare their generated graph statistics:

| Metric | Description |
| ------ | ----------- |
| Longest streak | Most consecutive days with commits |
| Total commits | Absolute commit count in the generated year |
| Consistency score | Standard deviation of daily commit counts (lower = more consistent) |
| Pattern creativity | Community votes on the most creative text/QR/theme designs |

```bash
python contribute.py --leaderboard --register --username="your-github-handle"
```

**Value:** Gamification drives engagement. Users compete for the most creative graph, the longest streak, and the most realistic pattern. Builds a community around the tool.

---

### 6.3 Community Pattern Gallery

A web gallery where users submit and share their custom graph designs (text patterns, QR codes, themes). Other users can browse, vote, and one-click import any pattern.

```bash
# Browse the gallery
python contribute.py --gallery

# Import a community pattern by ID
python contribute.py --import-pattern=gallery:heartbeat-v2 --repository=git@github.com:user/repo.git
```

**Value:** User-generated content extends ContribX's pattern library indefinitely without any work from the maintainer. The gallery becomes a destination in itself.

---

### 6.4 Animated Multi-Year Graph

Design patterns that create an animation effect when someone clicks through the year selector on a GitHub profile. Each year shows a different frame, producing a flipbook-style animation.

```bash
python contribute.py --animate="arrow-right" --years=2024,2025,2026 --repository=git@github.com:user/repo.git
```

Built-in animations:
- `arrow-right` — an arrow that moves across the grid year by year
- `growing-tree` — a tree that grows taller each year
- `wave-motion` — a wave that shifts phase each year
- `countdown` — displays "3", "2", "1", "GO" across four years

**Value:** Multi-year animated graphs are something nobody has ever done. This is the kind of feature that gets shared in blog posts and conference talks.

---

## Implementation Priority Matrix

| Priority | Feature | Phase | Effort | Impact | Uniqueness |
| -------- | ------- | ----- | ------ | ------ | ---------- |
| P0 | Dry Run Mode | 1 | Low | High | Medium |
| P0 | Config File Support | 1 | Low | High | Low |
| P0 | Progress Bar and Output | 1 | Low | Medium | Low |
| P0 | Undo / Rollback | 1 | Medium | High | High |
| P1 | Terminal Graph Preview | 2 | Medium | High | Medium |
| P1 | Text Pattern Designer | 2 | Medium | Very High | Very High |
| P1 | Theme Packs | 2 | Low | High | High |
| P1 | Commit Message Customization | 1 | Low | Medium | Medium |
| P2 | QR Code on Graph | 2 | High | Very High | Very High |
| P2 | Graph Export as Image | 2 | Medium | High | High |
| P2 | Clone User's Graph | 3 | Medium | High | Very High |
| P2 | Gap Filler | 3 | Medium | High | High |
| P2 | Realistic Developer Patterns | 3 | Medium | High | High |
| P2 | Country-Aware Holidays | 3 | Low | Medium | High |
| P3 | Interactive TUI | 4 | High | High | Medium |
| P3 | Web Graph Designer | 4 | High | Very High | Very High |
| P3 | Multi-Repo Distribution | 4 | Medium | High | Very High |
| P3 | Scheduled Execution | 4 | Low | Medium | Medium |
| P3 | Streak Insurance | 4 | Medium | Medium | High |
| P3 | Google Calendar Sync | 3 | Medium | Medium | Very High |
| P4 | PyPI Package | 5 | Low | High | Low |
| P4 | Docker Image | 5 | Low | Medium | Low |
| P4 | GitHub Action | 5 | Medium | Very High | High |
| P4 | NPX Wrapper | 5 | Low | Medium | Medium |
| P4 | Analytics Dashboard | 6 | Medium | Medium | High |
| P4 | Community Leaderboard | 6 | High | Medium | High |
| P4 | Pattern Gallery | 6 | High | High | Very High |
| P4 | Animated Multi-Year Graph | 6 | High | High | Very High |

---

## Recommended Execution Order

1. **Start with Phase 1** — these are low-effort, high-impact changes that immediately make ContribX feel production-grade. Dry run, config file, undo, and progress output can all be completed in 1-2 weeks.

2. **Build the Text Pattern Designer next** — this is the single most viral feature. The ability to write "HIRE ME" or your name on the GitHub contribution graph has massive shareability. Prioritize this over all other Phase 2 features.

3. **Add Theme Packs alongside the designer** — once the pattern engine exists, themes are just predefined pattern configurations. Low incremental effort.

4. **Publish to PyPI early** — do not wait until all features are built. Publish after Phase 1 + Text Designer. Each subsequent feature becomes a version bump that keeps the package growing.

5. **Build the QR Code feature** — this is the second viral feature. Combined with the text designer, ContribX becomes the only tool in the market that offers visual graph customization.

6. **Add intelligence (Phase 3) in parallel with distribution (Phase 5)** — realistic patterns and gap filler make the tool credible for professional use, while PyPI/Docker/GitHub Action expand reach.

7. **Build community features (Phase 6) last** — these only matter once there is a user base. The leaderboard and pattern gallery require critical mass to be valuable.

---

## Version Milestones

| Version | Contents | Target |
| ------- | -------- | ------ |
| v1.0 | Current state (CLI with basic generation) | Done |
| v2.0 | Phase 1 complete (dry run, config, undo, progress, messages) | Week 2 |
| v3.0 | Text designer + themes + terminal preview | Week 5 |
| v3.5 | PyPI package published | Week 6 |
| v4.0 | QR code + graph export + image export | Week 8 |
| v5.0 | Intelligence layer (clone, gap fill, realistic, holidays) | Week 12 |
| v6.0 | TUI + web designer + scheduler | Week 16 |
| v7.0 | GitHub Action + Docker + community features | Week 20 |
