#!/usr/bin/env python3
"""Repository checks that keep the docs honest.

    python tools/check_docs.py            em dashes + English/German pages in step
    python tools/check_docs.py --lenient  a missing German page is a warning, not an error

Standard library only, Python 3.9+.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EM_DASH = "—"

# Everything a reader or an agent sees.
EM_DASH_SCOPES = ["docs", "examples", "templates", ".agents", ".claude", ".opencode", "tools", "mods"]
EM_DASH_FILES = ["README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md", "TRADEMARKS.md", "mkdocs.yml"]
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".csv"}

HEADING = re.compile(r"^(#{1,3}) ", re.MULTILINE)
FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)


def iter_text_files():
	for name in EM_DASH_FILES:
		path = ROOT / name

		if path.is_file():
			yield path

	for scope in EM_DASH_SCOPES:
		base = ROOT / scope

		if not base.exists():
			continue

		for path in base.rglob("*"):
			if path.is_file() and path.suffix in TEXT_SUFFIXES and ".venv" not in path.parts:
				yield path


def check_em_dashes():
	problems = []

	for path in iter_text_files():
		if path.resolve() == pathlib.Path(__file__).resolve():
			continue

		for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
			if EM_DASH in line:
				problems.append(f"{path.relative_to(ROOT)}:{number}: em dash - use ' - ' instead")

	return problems


def heading_levels(path):
	text = FENCE.sub("", path.read_text(encoding="utf-8"))
	return [len(match.group(1)) for match in HEADING.finditer(text)]


def check_translations(lenient):
	errors, warnings = [], []
	english = ROOT / "docs" / "en"
	german = ROOT / "docs" / "de"

	for source in sorted(english.rglob("*.md")):
		relative = source.relative_to(english)
		target = german / relative

		if not target.exists():
			(warnings if lenient else errors).append(f"docs/de/{relative}: missing German page")
			continue

		if heading_levels(source) != heading_levels(target):
			errors.append(f"docs/de/{relative}: headings differ from docs/en/{relative} - the translation is out of step")

	for target in sorted(german.rglob("*.md")):
		relative = target.relative_to(german)

		if not (english / relative).exists():
			errors.append(f"docs/de/{relative}: no English source page")

	return errors, warnings


def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--lenient", action="store_true", help="missing German pages are warnings")
	arguments = parser.parse_args()

	errors = check_em_dashes()
	translation_errors, warnings = check_translations(arguments.lenient)
	errors += translation_errors

	for line in warnings:
		print("warning: " + line)

	for line in errors:
		print("error: " + line)

	print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(main())
