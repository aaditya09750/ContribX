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

    # ----------------------------
    # Use existing local repository
    # ----------------------------
    if local_path:
        directory = os.path.abspath(local_path)

        if not os.path.exists(directory):
            sys.exit(f"Directory does not exist:\n{directory}")

        if not os.path.isdir(directory):
            sys.exit(f"Not a directory:\n{directory}")

        os.chdir(directory)

        if not os.path.exists(".git"):
            print("Initializing git repository...")
            run(["git", "init", "-b", "main"])

    # ----------------------------
    # Original behavior
    # ----------------------------
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

    # ----------------------------
    # Git Config
    # ----------------------------
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

    for day in (
        start_date + timedelta(n)
        for n in range(days_before + days_after)
    ):

        if (
            (not no_weekends or day.weekday() < 5)
            and randint(0, 100) < frequency
        ):

            for commit_time in (
                day + timedelta(minutes=m)
                for m in range(contributions_per_day(args))
            ):
                contribute(commit_time)

    # ----------------------------
    # Push
    # ----------------------------
    if repository:

        remotes = subprocess.check_output(
            ["git", "remote"],
            text=True
        ).split()

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
    with open(os.path.join(os.getcwd(), "README.md"), "a") as file:
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
        action="store_true",
        default=False,
        help="Do not commit on weekends."
    )

    parser.add_argument(
        "-mc",
        "--max_commits",
        type=int,
        default=10,
        help="Maximum commits per day (1-20)."
    )

    parser.add_argument(
        "-fr",
        "--frequency",
        type=int,
        default=80,
        help="Percentage of days to commit."
    )

    parser.add_argument(
        "-r",
        "--repository",
        type=str,
        help="Remote Git repository URL."
    )

    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path to an existing local Git repository."
    )

    parser.add_argument(
        "-un",
        "--user_name",
        type=str,
        help="Override git user.name."
    )

    parser.add_argument(
        "-ue",
        "--user_email",
        type=str,
        help="Override git user.email."
    )

    parser.add_argument(
        "-db",
        "--days_before",
        type=int,
        default=365,
        help="Number of days before today."
    )

    parser.add_argument(
        "-da",
        "--days_after",
        type=int,
        default=0,
        help="Number of days after today."
    )

    return parser.parse_args(argsval)


if __name__ == "__main__":
    main()