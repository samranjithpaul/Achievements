"""Read and validate the GitHub achievements reference catalog."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

CATALOG = Path(__file__).resolve().parents[1] / "data" / "achievements.json"
STATUSES = ("active", "limited", "experimental", "historical")
TIERS = ("base", "bronze", "silver", "gold")


def load_catalog(path=CATALOG):
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list) or not entries:
        raise ValueError("The catalog must be a nonempty array")

    seen = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry {index} must be an object")
        for field in ("id", "name", "status", "activity", "note"):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Entry {index} requires a nonempty {field}")

        slug = entry["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate ID: {slug}")
        seen.add(slug)

        status = entry["status"]
        if status not in STATUSES:
            raise ValueError(f"{slug}: unknown status {status}")

        thresholds = entry.get("thresholds")
        if not isinstance(thresholds, dict):
            raise ValueError(f"{slug}: thresholds must be an object")
        tiers = [tier for tier in TIERS if tier in thresholds]
        if set(thresholds) != set(TIERS[:len(tiers)]):
            raise ValueError(f"{slug}: thresholds must start at base and use consecutive tiers")
        if status == "active" and not tiers:
            raise ValueError(f"{slug}: active entries need a base threshold")
        values = [thresholds[tier] for tier in tiers]
        if any(type(value) is not int or value <= 0 for value in values):
            raise ValueError(f"{slug}: thresholds must be positive integers")
        if any(first >= second for first, second in zip(values, values[1:])):
            raise ValueError(f"{slug}: thresholds must strictly increase")

        sources = entry.get("sources")
        if not isinstance(sources, list) or not sources:
            raise ValueError(f"{slug}: at least one source is required")
        for link in sources:
            if not isinstance(link, str) or any(char.isspace() for char in link):
                raise ValueError(f"{slug}: sources must be HTTPS URLs")
            url = urlsplit(link)
            if url.scheme != "https" or not url.hostname:
                raise ValueError(f"{slug}: invalid HTTPS source {link!r}")
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--status", choices=STATUSES, help="show only matching entries")
    args = parser.parse_args()
    try:
        entries = load_catalog()
    except (OSError, ValueError) as error:
        parser.exit(1, f"Catalog error: {error}\n")

    for entry in entries:
        if args.status is None or entry["status"] == args.status:
            values = " / ".join(
                f"{tier} {entry['thresholds'][tier]}" for tier in TIERS
                if tier in entry["thresholds"]
            )
            print(f"{entry['name']} [{entry['status']}] — {entry['activity']}")
            if values:
                print(f"  {values}")
            print(f"  {entry['note']}")


if __name__ == "__main__":
    main()
