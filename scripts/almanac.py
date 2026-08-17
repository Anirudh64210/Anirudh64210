"""Render a month-by-month almanac of contributions into README.md.

Reads the contribution calendar from the GitHub GraphQL API and rewrites
whatever sits between the ALMANAC markers. Run by .github/workflows/almanac.yml.

If GITHUB_TOKEN is a personal access token belonging to the user being
rendered, the API returns private contributions too -- so the almanac can
show real numbers even when the public calendar does not.
"""

import json
import os
import sys
import urllib.request
from collections import OrderedDict

USER = os.environ.get("ALMANAC_USER", "Anirudh64210")
TOKEN = os.environ["GITHUB_TOKEN"]
README = os.environ.get("ALMANAC_README", "README.md")

WIDTH = 16
START = "<!-- ALMANAC:START -->"
END = "<!-- ALMANAC:END -->"
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": "bearer " + TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "almanac",
        },
    )
    with urllib.request.urlopen(request) as response:
        payload = json.load(response)

    if "errors" in payload:
        sys.exit("graphql error: " + json.dumps(payload["errors"]))
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def longest_streak(days):
    best = run = 0
    for _, count in days:
        run = run + 1 if count else 0
        best = max(best, run)
    return best


def render(calendar):
    days = sorted(
        (day["date"], day["contributionCount"])
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    )

    months = OrderedDict()
    for iso, count in days:
        key = (int(iso[:4]), int(iso[5:7]))
        months[key] = months.get(key, 0) + count

    # the calendar starts mid-month a year back, so the first month is a
    # stub -- drop empty leading months rather than open on a dead row
    keys = list(months)
    while len(keys) > 1 and months[keys[0]] == 0:
        del months[keys.pop(0)]

    peak = max(months.values()) or 1
    lines = ["  ── the almanac ──────────────────────", ""]

    year = None
    for (this_year, month), count in months.items():
        if this_year != year:
            if year is not None:
                lines.append("")
            lines.append("   %d" % this_year)
            year = this_year
        # a month with any activity always earns at least one block
        filled = max(1, round(count / peak * WIDTH)) if count else 0
        bar = "█" * filled + "░" * (WIDTH - filled)
        lines.append("   %s  %s %4d" % (MONTHS[month - 1], bar, count))

    busiest = max(months, key=months.get)
    lines += [
        "",
        "  " + "─" * 36,
        "   busiest month .. %s %d" % (MONTHS[busiest[1] - 1], busiest[0]),
        "   longest streak . %d days" % longest_streak(days),
        "   total .......... %d" % calendar["totalContributions"],
    ]
    return "```\n" + "\n".join(lines) + "\n```"


def main():
    block = render(fetch())

    with open(README, encoding="utf-8") as handle:
        text = handle.read()

    start, end = text.find(START), text.find(END)
    if start == -1 or end == -1:
        sys.exit("could not find the ALMANAC markers in %s" % README)

    updated = text[: start + len(START)] + "\n\n" + block + "\n\n" + text[end:]
    if updated == text:
        print("almanac unchanged")
        return

    with open(README, "w", encoding="utf-8") as handle:
        handle.write(updated)
    print("almanac updated")


if __name__ == "__main__":
    main()
