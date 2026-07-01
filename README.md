# GitHub Activity Generator - Contribution Graph Builder

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-2.x-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-Apache_2.0-D22128?style=for-the-badge&logo=apache&logoColor=white)
[![Build](https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/aaditya09750/AG-ActivityGen/actions?query=workflow%3Abuild)

A script that helps you instantly generate a beautiful GitHub Contributions Graph for the last year.

**Original Author:** [Aaditya Gunjal](https://github.com/aaditya09750)

---

## ⚠ Disclaimer

This script is for educational purposes and demonstrating GitHub mechanics. It should not be used to misrepresent professional contributions or coding activity.

---

## What It Looks Like

### Before :neutral_face: :no_mouth: :unamused:
![Before](ag-activity-gen-main/.github/before.png)

### After :muscle: :relieved: :heart: :sunglasses: :metal: :horse: :wink: :fire: :dancer: :santa: :fireworks: :cherries: :tada:
![After](ag-activity-gen-main/.github/after.png)

---

## Core Features

- **Instant Contribution Graph:** Generate a year's worth of realistic-looking GitHub contributions in minutes.
- **Customizable Frequency:** Control what percentage of days receive commits (default 80%).
- **Adjustable Commit Volume:** Set maximum commits per day (1–20, default 10) with daily randomization.
- **Weekend Exclusion:** Optional `--no_weekends` flag to skip Saturday and Sunday commits.
- **Flexible Date Range:** Specify `--days_before` and `--days_after` to control the exact commit window.
- **Local Repository Support:** Use `--path` to generate commits inside an existing local Git repository.
- **Auto Push:** Provide a `--repository` URL (SSH or HTTPS) and the script initializes, commits, and pushes automatically.
- **Git Config Overrides:** Override `user.name` and `user.email` per run without changing global settings.
- **CI Tested:** GitHub Actions workflow validates linting (flake8) and unit tests across Python 3.8–3.11.

---

## Technology Stack

| Technology | Version | Purpose |
| ---------- | ------- | ------- |
| Python | 3.8+ | Script runtime |
| Git | 2.x | Version control and commit generation |
| argparse | stdlib | CLI argument parsing |
| subprocess | stdlib | Git command execution |
| random | stdlib | Randomized commit counts |
| datetime | stdlib | Date arithmetic for commit timestamps |
| flake8 | latest | Linting (CI) |
| unittest | stdlib | Unit testing |
| GitHub Actions | — | CI/CD pipeline |

---

## Project Structure

```text
AG-ActivityGen/
├── ag-activity-gen-main/
│   ├── .github/
│   │   ├── workflows/
│   │   │   └── build.yml              (CI: lint + test across Python 3.8–3.11)
│   │   ├── before.png                 (contribution graph screenshot — before)
│   │   └── after.png                  (contribution graph screenshot — after)
│   ├── contribute.py                  (main script — commit generation engine)
│   ├── test_contribute.py             (unit tests for argument parsing & commits)
│   └── LICENSE                        (Apache License 2.0)
│
├── AG-Activity/
│   └── README.md
│
├── .git/
└── README.md                          (this file)
```

---

## Quick Start

### Prerequisites

- Python (3.8 or higher)
- Git (2.x or higher)
- An empty, **non-initialized** GitHub repository (for auto-push)

### Basic Usage

```bash
# 1. Clone or download this repository
git clone https://github.com/aaditya09750/AG-ActivityGen.git
cd AG-ActivityGen

# 2. Run the script with your empty repo URL
python contribute.py --repository=git@github.com:user/repo.git
```

Now you have a repository with lots of changes in your GitHub account.

> **Note:** It takes several minutes for GitHub to reindex your activity.

---

## How It Works

The script initializes an empty git repository, creates a text file and starts generating changes to the file for every day within the last year (0–20 commits per day). Once the commits are generated it links the created repository with the remote repository and pushes the changes.

---

## Customizations

You can customize how often to commit and how many commits a day to make, etc.

### CLI Arguments

| Flag | Long Form | Type | Default | Description |
| ---- | --------- | ---- | ------- | ----------- |
| `-mc` | `--max_commits` | int | 10 | Maximum commits per day (1–20). Exact count is randomized daily. |
| `-fr` | `--frequency` | int | 80 | Percentage of days that receive commits (0–100). |
| `-nw` | `--no_weekends` | flag | false | Skip commits on Saturdays and Sundays. |
| `-db` | `--days_before` | int | 365 | Number of days before today to start committing. |
| `-da` | `--days_after` | int | 0 | Number of days after today to continue committing. |
| `-r` | `--repository` | str | — | Remote repository URL (SSH or HTTPS). If set, script pushes automatically. |
| `-p` | `--path` | str | — | Path to a local folder inside an existing Git repo. Script finds nearest parent repo. |
| `-un` | `--user_name` | str | — | Override `user.name` git config for this run. |
| `-ue` | `--user_email` | str | — | Override `user.email` git config for this run. |

### Examples

**Custom frequency and commit volume:**

```sh
python contribute.py --max_commits=12 --frequency=60 --repository=git@github.com:user/repo.git
```
This makes 1–12 commits per day, committing on 60% of days.

**Skip weekends:**

```sh
python contribute.py --no_weekends
```

**Custom date range:**

```sh
python contribute.py --days_before=10 --days_after=15
```

**Use an existing local repository:**

```sh
python contribute.py --path=/path/to/existing/repo --repository=git@github.com:user/repo.git
```

**Override Git identity:**

```sh
python contribute.py --user_name="Your Name" --user_email="you@example.com" --repository=git@github.com:user/repo.git
```

If you do not set the `--repository` argument the script won't push the changes. This way you can import the generated repository yourself.

Run `python contribute.py --help` to get the full help output.

---

## System Requirements

| Requirement | Minimum Version |
| ----------- | --------------- |
| Python | 3.8+ |
| Git | 2.x |
| OS | Windows, macOS, or Linux |

---

## Testing

```bash
# Run unit tests
python -m unittest test_contribute

# Lint check
pip install flake8
flake8 contribute.py
flake8 test_contribute.py
```

The GitHub Actions CI pipeline automatically runs both lint and test on every push and pull request across Python 3.8, 3.9, 3.10, and 3.11.

---

## Troubleshooting

**I ran the script but my GitHub activity is still the same.**

- It might take several minutes for GitHub to reindex your activity. Check if the repository has new commits and wait a couple of minutes.

**The changes are still not reflected after some time.**

- Are you using a private repository? If so, enable showing private contributions [following this guide](https://help.github.com/en/articles/publicizing-or-hiding-your-private-contributions-on-your-profile).

**Email mismatch — contributions not counted.**

- Make sure the email address you have in GitHub is the same as your local Git settings. GitHub counts contributions only when they are made using the corresponding email.

```bash
# Check your local email
git config --get user.email

# Reset if it doesn't match GitHub
git config --global user.email "user@example.com"
```

Create a new repository and rerun the script.

**Errors in the script logs.**

- Maybe you tried to use an existing repository. Make sure you are using a new one which is *not initialized*.

**If none of the options helped, open an issue and it will be fixed as soon as possible.**

---

## Other Projects by the Author

| Project | Description |
| ------- | ----------- |
| [HealanceAI-Orbit](https://github.com/aaditya09750/HealanceAI-Orbit) | Full-stack AI-powered health and wellness platform |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push your branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## Contact & Support

- Email: aadigunjal0975@gmail.com
- Issues: [GitHub Issues](https://github.com/aaditya09750/AG-ActivityGen/issues)

---

## Acknowledgments

- GitHub for the contributions graph and API
- Python community for the standard library ecosystem
- flake8 for linting support
- GitHub Actions for CI/CD infrastructure

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE](ag-activity-gen-main/LICENSE) for details.
