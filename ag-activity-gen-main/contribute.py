#!/usr/bin/env python

import argparse
import os
import sys
import subprocess
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen

# Global flag for conventional commits format
CONVENTIONAL_COMMITS = False


def parse_specific_dates(date_string, date_format="%Y-%m-%d"):
    """
    Parse a comma-separated string of dates into a list of datetime objects.
    Returns a list of datetime objects or None if parsing fails.
    """
    if not date_string:
        return None
    
    dates = []
    date_list = [d.strip() for d in date_string.split(",")]
    
    if not date_list:
        sys.exit("No dates provided in --specific-dates")
    
    for date_str in date_list:
        try:
            parsed_date = datetime.strptime(date_str, date_format)
            # Set time to 20:00 to match start_date behavior
            parsed_date = parsed_date.replace(hour=20, minute=0)
            dates.append(parsed_date)
        except ValueError as e:
            sys.exit(
                f"Invalid date format: '{date_str}'\n"
                f"Expected format: {date_format}\n"
                f"Error: {e}"
            )
    
    return sorted(dates) if dates else None


def find_git_root(start_path):
    """
    Walk upward from start_path until a .git directory or .git file is found.
    Returns the repository root directory if found, otherwise None.
    """
    current = os.path.abspath(start_path)

    while True:
        git_path = os.path.join(current, ".git")
        if os.path.isdir(git_path) or os.path.isfile(git_path):
            return current

        parent = os.path.dirname(current)
        if parent == current:
            return None

        current = parent


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)

    curr_date = datetime.now()

    repository = args.repository
    local_path = args.path
    user_name = args.user_name
    user_email = args.user_email

    directory = "repository-" + curr_date.strftime("%Y-%m-%d-%H-%M-%S")
    target_directory = None
    repo_root = None

    # Use existing local repository when --path is provided.
    if local_path:
        target_directory = os.path.abspath(local_path)

        if not os.path.exists(target_directory):
            sys.exit(f"Directory does not exist:\n{target_directory}")

        if not os.path.isdir(target_directory):
            sys.exit(f"Not a directory:\n{target_directory}")

        # Find the nearest parent git repository.
        repo_root = find_git_root(target_directory)
        if repo_root is None:
            sys.exit(
                "The specified path is not inside an existing Git repository:\n"
                f"{target_directory}\n\n"
                "Please clone or initialize the repository first."
            )

        os.chdir(repo_root)

    # Original behavior when --path is not provided.
    else:
        if repository is not None:
            start = repository.rfind("/") + 1
            end = repository.rfind(".")
            directory = repository[start:end]

        if not os.path.exists(directory):
            os.mkdir(directory)

        os.chdir(directory)
        repo_root = os.getcwd()
        target_directory = repo_root

        if not os.path.exists(".git"):
            run(["git", "init", "-b", "main"])

    # Git config overrides.
    if user_name:
        run(["git", "config", "user.name", user_name])

    if user_email:
        run(["git", "config", "user.email", user_email])

    no_weekends = args.no_weekends
    specific_dates_str = args.specific_dates
    date_format = args.date_format
    frequency = args.frequency
    days_before = args.days_before
    days_after = args.days_after
    
    # Set global flag for conventional commits
    global CONVENTIONAL_COMMITS
    CONVENTIONAL_COMMITS = args.conventional_commits

    # Handle specific dates mode
    if specific_dates_str:
        specific_dates = parse_specific_dates(specific_dates_str, date_format)
        
        if not specific_dates:
            sys.exit("No valid dates could be parsed from --specific-dates")
        
        # Generate commits for each specific date
        for day in specific_dates:
            # Respect no_weekends flag even in specific dates mode
            if not no_weekends or day.weekday() < 5:
                for commit_time in (
                    day + timedelta(minutes=m)
                    for m in range(contributions_per_day(args))
                ):
                    contribute(commit_time, target_directory)
    else:
        # Original date range mode
        if days_before < 0:
            sys.exit("days_before must not be negative")

        if days_after < 0:
            sys.exit("days_after must not be negative")

        start_date = curr_date.replace(hour=20, minute=0) - timedelta(days_before)

        for day in (start_date + timedelta(n) for n in range(days_before + days_after)):
            if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
                for commit_time in (
                    day + timedelta(minutes=m)
                    for m in range(contributions_per_day(args))
                ):
                    contribute(commit_time, target_directory)

    # Push to remote when repository is provided.
    if repository:
        remotes = subprocess.check_output(
            ["git", "remote"],
            text=True
        ).strip().splitlines()

        if "origin" not in remotes:
            run(["git", "remote", "add", "origin", repository])
        else:
            run(["git", "remote", "set-url", "origin", repository])

        run(["git", "branch", "-M", "main"])
        run(["git", "push", "-u", "origin", "main"])

    print(
        "\nRepository generation "
        "\x1b[6;30;42mcompleted successfully\x1b[0m!"
    )


def contribute(date, target_directory):
    readme_path = os.path.join(target_directory, "README.md")

    with open(readme_path, "a", encoding="utf-8") as file:
        file.write(message(date) + "\n\n")

    run(["git", "add", "."])

    run([
        "git",
        "commit",
        "-m",
        message(date),
        "--date",
        date.strftime("%Y-%m-%d %H:%M:%S")
    ])


def run(commands):
    Popen(commands).wait()


def message(date):
    """
    Generate commit message in either conventional or legacy format.
    Conventional format: feat: contribution on YYYY-MM-DD HH:MM
    Legacy format: Contribution: YYYY-MM-DD HH:MM
    """
    if CONVENTIONAL_COMMITS:
        return date.strftime("feat: contribution on %Y-%m-%d %H:%M")
    else:
        return date.strftime("Contribution: %Y-%m-%d %H:%M")


def contributions_per_day(args):
    max_c = args.max_commits

    if max_c > 20:
        max_c = 20

    if max_c < 1:
        max_c = 1

    return randint(1, max_c)


def arguments(argsval):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-nw",
        "--no_weekends",
        required=False,
        action="store_true",
        default=False,
        help="Do not commit on weekends."
    )

    parser.add_argument(
        "-mc",
        "--max_commits",
        type=int,
        default=10,
        required=False,
        help="""Defines the maximum amount of commits a day the script can make.
Accepts a number from 1 to 20. If N is specified the script commits from 1 to N
times a day. The exact number of commits is defined randomly for each day.
The default value is 10."""
    )

    parser.add_argument(
        "-fr",
        "--frequency",
        type=int,
        default=80,
        required=False,
        help="""Percentage of days when the script performs commits. If N is
specified, the script will commit N%% of days in a year. The default value is 80."""
    )

    parser.add_argument(
        "-r",
        "--repository",
        type=str,
        required=False,
        help="""A link on an empty non-initialized remote git repository.
If specified, the script pushes the changes to the repository.
The link is accepted in SSH or HTTPS format.
For example: git@github.com:user/repo.git or https://github.com/user/repo.git"""
    )

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        required=False,
        help="""Path to a local folder inside an existing Git repository.
If specified, the script will find the nearest parent repository and use it."""
    )

    parser.add_argument(
        "-un",
        "--user_name",
        type=str,
        required=False,
        help="""Overrides user.name git config.
If not specified, the global config is used."""
    )

    parser.add_argument(
        "-ue",
        "--user_email",
        type=str,
        required=False,
        help="""Overrides user.email git config.
If not specified, the global config is used."""
    )

    parser.add_argument(
        "-db",
        "--days_before",
        type=int,
        default=365,
        required=False,
        help="""Specifies the number of days before the current date when the
script will start adding commits. For example: if it is set to 30 the first
commit date will be the current date minus 30 days."""
    )

    parser.add_argument(
        "-da",
        "--days_after",
        type=int,
        default=0,
        required=False,
        help="""Specifies the number of days after the current date until which
the script will be adding commits. For example: if it is set to 30 the last
commit will be on a future date which is the current date plus 30 days."""
    )

    parser.add_argument(
        "-sd",
        "--specific-dates",
        type=str,
        required=False,
        default=None,
        help="""Comma-separated list of specific dates to generate commits on.
For example: 2026-09-13,2026-09-14 or 09/13/2026,09/14/2026
When specified, --days_before, --days_after, and --frequency are ignored.
Date format is controlled by --date-format (default: YYYY-MM-DD).
The --max_commits parameter still controls commits per day.
The --no_weekends flag is still respected if enabled."""
    )

    parser.add_argument(
        "-df",
        "--date-format",
        type=str,
        required=False,
        default="%Y-%m-%d",
        help="""Date format string for --specific-dates parsing.
Default is YYYY-MM-DD (%%Y-%%m-%%d).
Other examples: %%m/%%d/%%Y for MM/DD/YYYY or %%d-%%m-%%Y for DD-MM-YYYY"""
    )

    parser.add_argument(
        "-cc",
        "--conventional-commits",
        required=False,
        action="store_true",
        default=False,
        help="""Use conventional commit format (feat:, fix:, etc.).
Default format: 'Contribution: YYYY-MM-DD HH:MM'
Conventional format: 'feat: contribution on YYYY-MM-DD HH:MM'
Ideal for professional repositories following commit conventions."""
    )

    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()