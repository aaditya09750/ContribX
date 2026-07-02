# ContribX - GitHub Contribution Graph Generator

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-2.x-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-4A154B?style=for-the-badge)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/aaditya09750/AG-ActivityGen/actions?query=workflow%3Abuild)

ContribX is a command-line utility that programmatically generates backdated Git commits to populate a GitHub Contributions Graph. The tool creates authentic commit objects with configurable date ranges, frequency distributions, and volume controls, producing a realistic contribution history across any specified time window.

**Author:** [Aaditya Gunjal](https://github.com/aaditya09750)

---

## Disclaimer

This tool is developed strictly for **educational purposes** and for demonstrating the internal mechanics of Git commit history and the GitHub Contributions Graph rendering system. It is not intended to misrepresent professional development activity, fabricate employment credentials, or inflate contribution metrics for any professional or commercial purpose. Use responsibly and ethically.

---

## Visual Demonstration

### Before

![Contribution Graph — Before](ag-activity-gen-main/.github/before.png)

### After

![Contribution Graph — After](ag-activity-gen-main/.github/after.png)

The screenshots above illustrate the transformation of a GitHub profile's contribution graph after a single execution of the ContribX script with default parameters (365 days, 80% frequency, up to 10 commits per day).

---

## Core Features

- **Automated Contribution Generation:** Produces up to a full year of realistic, backdated Git commits in a single script execution, eliminating any manual commit workflow.
- **Configurable Commit Frequency:** Fine-grained control over what percentage of days within the target window receive commits. The default is 80%, but values from 0 to 100 are accepted, allowing sparse or dense contribution patterns.
- **Adjustable Daily Commit Volume:** The maximum number of commits per day is configurable (1 to 20). The actual count for each day is randomly selected between 1 and the configured maximum, producing organic variation in the graph.
- **Weekend Exclusion:** An optional flag (`--no_weekends`) suppresses all commit generation on Saturdays and Sundays, producing a weekday-only contribution pattern consistent with professional development workflows.
- **Flexible Date Range Control:** The `--days_before` and `--days_after` parameters allow precise control over the start and end boundaries of the commit window relative to the current date, enabling targeted graph population for specific time periods.
- **Existing Repository Support:** The `--path` parameter allows ContribX to operate within an already-initialized local Git repository, finding the nearest parent `.git` root automatically. This enables incremental contribution additions without creating a new repository.
- **Automatic Remote Push:** When a `--repository` URL is provided (SSH or HTTPS format), the script automatically configures the remote origin, renames the branch to `main`, and pushes all generated commits in a single operation.
- **Per-Run Git Identity Overrides:** The `--user_name` and `--user_email` parameters override the local Git configuration for the current execution only, without modifying the global Git settings. This ensures the generated commits are attributed to the correct GitHub account.
- **Continuous Integration:** A GitHub Actions workflow validates code quality (flake8 linting) and functional correctness (unittest) across Python versions 3.8, 3.9, 3.10, and 3.11 on every push and pull request.

---

## Technology Stack

| Technology | Version | Purpose |
| ---------- | ------- | ------- |
| Python | 3.8+ | Primary script runtime and execution environment |
| Git | 2.x | Underlying version control system for commit generation and repository management |
| argparse | stdlib | Command-line interface argument parsing and validation |
| subprocess | stdlib | System-level Git command execution and process management |
| random | stdlib | Pseudorandom number generation for daily commit count variation |
| datetime | stdlib | Date arithmetic, timestamp formatting, and commit date backdating |
| os | stdlib | Filesystem navigation, directory creation, and path resolution |
| flake8 | latest | Static code analysis and PEP 8 compliance enforcement (CI pipeline) |
| unittest | stdlib | Unit testing framework for argument parsing and commit generation validation |
| GitHub Actions | — | Continuous integration and automated testing pipeline |

---

## Project Structure

```text
ContribX/
|
+-- ag-activity-gen-main/                  [Source Code Directory]
|   +-- .github/
|   |   +-- workflows/
|   |   |   +-- build.yml                 CI workflow: lint + test across Python 3.8-3.11
|   |   +-- before.png                    Contribution graph screenshot (before execution)
|   |   +-- after.png                     Contribution graph screenshot (after execution)
|   +-- contribute.py                     Core script: commit generation engine with CLI interface
|   +-- test_contribute.py                Unit tests: argument parsing, commit count, and integration
|   +-- LICENSE                           Apache License 2.0
|
+-- AG-Activity/                           [Commit Target Directory]
|   +-- README.md                         Target file for generated commit entries (see AG-Activity docs)
|
+-- .git/                                  Git repository metadata
+-- README.md                              Project documentation (this file)
```

---

## Quick Start

### Prerequisites

| Requirement | Minimum Version | Installation |
| ----------- | --------------- | ------------ |
| Python | 3.8 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| Git | 2.x or higher | [git-scm.com/downloads](https://git-scm.com/downloads) |
| GitHub Account | — | SSH or HTTPS authentication configured |

### Step 1 — Clone the Repository

```bash
git clone https://github.com/aaditya09750/AG-ActivityGen.git
cd AG-ActivityGen
```

### Step 2 — Execute the Script

**Automatic mode (generates commits and pushes to remote):**

```bash
python ag-activity-gen-main/contribute.py --repository=git@github.com:user/repo.git
```

**Local mode (generates commits without pushing):**

```bash
python ag-activity-gen-main/contribute.py
```

After local generation, push manually when ready:

```bash
git push origin main
```

**Targeted mode (commits into the AG-Activity directory of this repository):**

```bash
python ag-activity-gen-main/contribute.py --path=./AG-Activity --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

### Step 3 — Verify

1. Allow 2 to 5 minutes for GitHub to reindex contribution activity.
2. Navigate to your GitHub profile and inspect the Contributions Graph.
3. If the repository is private, confirm that private contribution visibility is enabled in your [GitHub profile settings](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile).

> **Note:** GitHub attributes contributions based on the email address associated with each commit. Ensure your local Git email matches the email registered on your GitHub account.

---

## How It Works

ContribX operates through the following execution pipeline:

1. **Repository Initialization:** If no `--path` is provided, the script creates a new directory and initializes an empty Git repository with `git init -b main`. If `--path` is provided, it traverses upward from the specified directory to locate the nearest `.git` root.

2. **Commit Generation Loop:** For each day in the configured date range (default: 365 days before the current date), the script evaluates two conditions:
   - The day passes the frequency probability check (default: 80% chance).
   - If `--no_weekends` is enabled, the day is a weekday (Monday through Friday).

3. **File Modification:** For each qualifying day, a random number of commits (between 1 and `--max_commits`) are generated. Each commit appends a timestamped line to the target `README.md` file in the format `Contribution: YYYY-MM-DD HH:MM`.

4. **Backdated Commit Creation:** Each modification is staged with `git add .` and committed with `git commit --date`, setting the commit timestamp to the target day. This causes GitHub to render the commit on the corresponding day in the Contributions Graph.

5. **Remote Push:** If a `--repository` URL is provided, the script configures the remote origin (or updates it if one already exists), renames the branch to `main`, and executes a force push to the remote.

---

## Command-Line Interface Reference

### Complete Argument Table

| Short | Long Form | Type | Default | Description |
| ----- | --------- | ---- | ------- | ----------- |
| `-mc` | `--max_commits` | int | 10 | Maximum number of commits generated per qualifying day. The actual count is randomly selected between 1 and this value for each day, producing natural variation. Values exceeding 20 are clamped to 20; values below 1 are clamped to 1. |
| `-fr` | `--frequency` | int | 80 | Percentage probability (0–100) that any given day in the range will receive commits. A value of 60 means approximately 60% of days will have commits, with the remaining 40% left empty. |
| `-nw` | `--no_weekends` | flag | false | When set, no commits are generated on Saturdays or Sundays, regardless of the frequency setting. |
| `-db` | `--days_before` | int | 365 | Number of days before the current date to begin generating commits. A value of 30 starts the commit window 30 days in the past. Must be a non-negative integer. |
| `-da` | `--days_after` | int | 0 | Number of days after the current date to continue generating commits. A value of 15 extends the commit window 15 days into the future. Must be a non-negative integer. |
| `-r` | `--repository` | str | none | Remote repository URL in SSH (`git@github.com:user/repo.git`) or HTTPS (`https://github.com/user/repo.git`) format. When provided, the script automatically pushes all generated commits to this remote. |
| `-p` | `--path` | str | none | Absolute or relative path to a directory inside an existing Git repository. The script will locate the nearest parent `.git` root and use it as the working repository. The specified directory must exist and must be within an initialized Git repository. |
| `-un` | `--user_name` | str | git config | Overrides the `user.name` Git configuration for this execution only. Useful when the global Git identity differs from the GitHub account that should receive the contribution credit. |
| `-ue` | `--user_email` | str | git config | Overrides the `user.email` Git configuration for this execution only. This email must match the email address registered on the target GitHub account for contributions to be counted. |

### Usage Examples

**Standard execution with default parameters (365 days, 80% frequency, up to 10 commits/day):**

```bash
python ag-activity-gen-main/contribute.py --repository=git@github.com:user/repo.git
```

**Reduced density with weekend exclusion:**

```bash
python ag-activity-gen-main/contribute.py --max_commits=5 --frequency=60 --no_weekends --repository=git@github.com:user/repo.git
```

**Targeted 30-day historical window with 10-day forward projection:**

```bash
python ag-activity-gen-main/contribute.py --days_before=30 --days_after=10 --repository=git@github.com:user/repo.git
```

**Execution against an existing local repository with identity override:**

```bash
python ag-activity-gen-main/contribute.py \
  --path=./AG-Activity \
  --user_name="Aaditya Gunjal" \
  --user_email="aadigunjal0975@gmail.com" \
  --repository=git@github.com:aaditya09750/AG-ActivityGen.git
```

Run `python ag-activity-gen-main/contribute.py --help` for the complete help output.

---

## System Requirements

| Requirement | Minimum Version | Notes |
| ----------- | --------------- | ----- |
| Python | 3.8+ | Tested on 3.8, 3.9, 3.10, and 3.11 via CI |
| Git | 2.x | Required for commit generation and remote operations |
| Operating System | Any | Windows, macOS, and Linux are fully supported |
| Network | — | Required only when `--repository` is set for auto-push |

---

## Testing

### Running Tests Locally

```bash
# Navigate to the source directory
cd ag-activity-gen-main

# Execute the unit test suite
python -m unittest test_contribute

# Run static analysis and PEP 8 compliance checks
pip install flake8
flake8 contribute.py
flake8 test_contribute.py
```

### Continuous Integration

The GitHub Actions CI pipeline (defined in `.github/workflows/build.yml`) executes automatically on every push and pull request. The pipeline runs the following steps across a Python version matrix (3.8, 3.9, 3.10, 3.11):

1. Checkout the repository
2. Install flake8 for static analysis
3. Lint `contribute.py` and `test_contribute.py`
4. Execute the full unittest suite

---

## Troubleshooting

### Contributions Not Appearing on GitHub

GitHub may take several minutes to reindex contribution activity after commits are pushed. Verify that the repository contains the expected commits by running `git log --oneline -10` and wait 2 to 5 minutes for the graph to update.

### Contributions Still Missing After Reindexing

If the repository is private, GitHub does not display private contributions by default. Enable private contribution visibility by navigating to your profile settings and toggling the option as described in the [GitHub documentation](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile).

### Email Address Mismatch

GitHub only attributes contributions to your account when the commit email matches an email address registered on your GitHub account. Verify your local Git email configuration:

```bash
# Display the currently configured email
git config --get user.email

# Update if it does not match your GitHub account email
git config --global user.email "your-github-email@example.com"
```

After updating, create a new repository and rerun the script. Alternatively, use the `--user_email` flag to override the email for a single execution.

### Script Errors on Execution

Ensure the target repository is empty and not previously initialized. If using `--path`, confirm the specified directory exists and resides within a valid Git repository. The script will exit with a descriptive error message if the path is invalid or the Git root cannot be located.

### Persistent Issues

If the above steps do not resolve the issue, open a detailed bug report on the [GitHub Issues](https://github.com/aaditya09750/AG-ActivityGen/issues) page, including the full command used, the error output, and the Python and Git versions installed.

---

## Other Projects by the Author

| Project | Description |
| ------- | ----------- |
| [HealanceAI-Orbit](https://github.com/aaditya09750/HealanceAI-Orbit) | A comprehensive full-stack health and wellness platform with AI-powered diagnostics, risk prediction, and personalized health tracking |

---

## Contributing

Contributions are welcome. To contribute to ContribX:

1. Fork the repository.
2. Create a feature branch from `main`: `git checkout -b feature/your-feature-name`
3. Implement your changes and ensure all tests pass: `python -m unittest test_contribute`
4. Verify linting compliance: `flake8 contribute.py`
5. Commit your changes with a descriptive message: `git commit -m "Add: description of your feature"`
6. Push the branch to your fork: `git push origin feature/your-feature-name`
7. Open a Pull Request against the `main` branch of this repository.

---

## Contact and Support

| Channel | Details |
| ------- | ------- |
| Email | aadigunjal0975@gmail.com |
| GitHub Issues | [aaditya09750/AG-ActivityGen/issues](https://github.com/aaditya09750/AG-ActivityGen/issues) |
| GitHub Profile | [aaditya09750](https://github.com/aaditya09750) |

---

## Acknowledgments

- GitHub for the Contributions Graph system and public API surface
- The Python Software Foundation and the Python standard library ecosystem
- The flake8 maintainers for static analysis tooling
- GitHub Actions for the CI/CD infrastructure

---

## License

This project is licensed under the **Apache License 2.0**. See [LICENSE](ag-activity-gen-main/LICENSE) for the full license text.
