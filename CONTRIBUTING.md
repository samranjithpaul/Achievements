# Contributing

Corrections, primary sources, clearer explanations, and improvements to the
catalog checks are welcome. Check open issues and pull requests for overlapping work.

1. Fork and clone the repository, then create a branch for your change.
2. Update the relevant entry in [the catalog](data/achievements.json).
   Include a public source and explain what it establishes. Use the GitHub
   Docs, a GitHub staff announcement, or a GitHub profile dialog where possible.
   Label independently reported thresholds as community evidence. Leave an
   undocumented threshold out and explain the gap in the entry's note.
3. Run `python3 scripts/catalog.py` and
   `python3 -m unittest discover -s tests -v` using Python 3.10 or newer.
4. Open a pull request. Describe the change, cite evidence, and report the
   checks you ran. Use a single focused PR for a coherent change.

Use public sources and omit credentials and private account activity. If
sharing a screenshot, crop it to the relevant badge or error and redact
personal details. Reproduce disputed criteria with existing public evidence
where possible. Please avoid test issues, PRs, stars, or discussions on GitHub
solely to generate achievement activity.
