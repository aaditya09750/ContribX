#!/usr/bin/env python

import argparse
import os
import sys
import subprocess
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)

    curr_date = datetime.now()

    repository = args.repository
    local_path = args.path
    user_name = args.user_name
    user_email = args.user_email

    directory = "repository-" + curr_date.strftime("%Y-%m-%d-%H-%M-%S")

    # Use existing local repository when --path is provided.
    if local_path:
        directory = os.path.abspath(local_path)

        if not os.path.exists(directory):
            sys.exit(f"Directory does not exist:\n{directory}")

        if not os.path.isdir(directory):
            sys.exit(f"Not a directory:\n{directory}")

        git_directory = os.path.join(directory, ".git")

        if not os.path.isdir(git_directory):
            sys.exit(
                "The specified path is not an existing Git repository:\n"
                f"{directory}\n\n"
                "Clone or initialize the repository first."
            )

        os.chdir(directory)

    # Original behavior when --path is not provided.
    else:
        if repository is not None:
            start = repository.rfind("/") + 1
            end = repository.rfind(".")
            directory = repository[start:end]

        if not os.path.exists(directory):
            os.mkdir(directory)

        os.chdir(directory)

        if not os.path.exists(".git"):
            run(["git", "init", "-b", "main"])

    # Git config overrides.
    if user_name:
        run(["git", "config", "user.name", user_name])

    if user_email:
        run(["git", "config", "user.email", user_email])

    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    days_after = args.days_after

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
                contribute(commit_time)

    # Push to remote when repository is provided.
    if repository:
        remotes = subprocess.check_output(["git", "remote"], text=True).strip().splitlines()

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


def contribute(date):
    with open(os.path.join(os.getcwd(), "README.md"), "a", encoding="utf-8") as file:
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
        help="""Path to an existing local Git repository.
If specified, the script uses this repository instead of creating a new one."""
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

    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()