# GitHub Achievements Reference

An independent, source-backed reference for GitHub profile achievements. Use it to
check how an achievement is earned, which thresholds are reported by the community,
and whether an achievement is currently a practical target.

Start with the [achievement catalog](data/achievements.json). Each entry records
its availability, qualifying activity, known thresholds, and source links.
GitHub’s [profile reference](https://docs.github.com/en/account-and-profile/reference/profile-reference#earning-achievements)
explains where awards appear and how to inspect their qualifying events. GitHub
describes the feature as a public preview. The official documentation does not
publish a full threshold table.

| Achievement | Qualifying activity |
| --- | --- |
| Pull Shark | Have pull requests you authored merged. |
| Pair Extraordinaire | Co-author a commit included in a merged pull request. |
| Galaxy Brain | Write answers that are accepted in eligible repository Discussions. |
| Starstruck | Receive stars on a single repository you created. |
| Quickdraw | Close an issue or pull request within five minutes of opening. |
| YOLO | Merge a pull request without a review. |
| Public Sponsor | Publicly sponsor open-source work through GitHub Sponsors. |

GitHub awards achievements on the profile itself. GitHub also documents
[profile highlights](https://docs.github.com/en/account-and-profile/reference/profile-reference#badges),
such as GitHub Pro. README trophy widgets are third-party displays. Badge art,
a status in this catalog, or an estimated count cannot confirm an award.

## Use the catalog

Read the JSON directly or filter it locally with Python 3.10 or newer.
No packages, token, or GitHub API access are required.

```sh
python3 scripts/catalog.py
python3 scripts/catalog.py --status experimental
python3 -m unittest discover -s tests -v
```

## Contribute

Report a stale criterion or suggest a better source using the
[issue tracker](https://github.com/samranjithpaul/Achievements/issues).
See [CONTRIBUTING.md](CONTRIBUTING.md) for the evidence and testing checklist.
