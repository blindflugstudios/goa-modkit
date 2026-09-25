#!/usr/bin/env python3
"""Give every translated heading the anchor of its English original.

Links between pages use English anchors (`../basics/mods.md#which-mod-wins`). A German
heading would get a German anchor and break them, so each translated heading carries the
English id explicitly: `## Welcher Mod gewinnt { #which-mod-wins }`.

Headings are matched by position, which works because tools/check_docs.py enforces the
same heading structure in every language.

    python tools/sync_anchors.py           add or fix the ids in docs/<lang>/
    python tools/sync_anchors.py --check   exit 1 if any translated heading is missing its id

Standard library only, Python 3.9+.
"""

import argparse
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SOURCE = "en"

HEADING = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*$")
EXPLICIT_ID = re.compile(r"\s*\{\s*#([\w\-.:]+)[^}]*\}\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")


def slugify(text):
	"""The id Python-Markdown's toc extension gives a heading (its default slugify)."""

	text = re.sub(r"`([^`]*)`", r"\1", text)
	text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
	text = re.sub(r"<[^>]+>", "", text)
	text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
	text = re.sub(r"[^\w\s-]", "", text).strip().lower()
	return re.sub(r"[-\s]+", "-", text)


def headings(lines):
	"""(line index, level, text, explicit id or None) for every heading outside code fences."""

	result = []
	in_fence = False

	for index, line in enumerate(lines):
		if FENCE.match(line):
			in_fence = not in_fence
			continue

		if in_fence:
			continue

		match = HEADING.match(line)

		if match:
			text = match.group(2)
			explicit = EXPLICIT_ID.search(text)
			result.append((index, len(match.group(1)), text, explicit.group(1) if explicit else None))

	return result


def english_ids(path):
	return [explicit or slugify(text) for _, _, text, explicit in headings(path.read_text(encoding="utf-8").splitlines())]


def sync(target, ids, check_only):
	lines = target.read_text(encoding="utf-8").splitlines()
	found = headings(lines)
	problems = []

	if len(found) != len(ids):
		return [f"{target.relative_to(ROOT)}: {len(found)} headings, English has {len(ids)} - fix the structure first"]

	for (index, level, text, explicit), wanted in zip(found, ids):
		# The page title (H1) is never linked to by anchor.
		if level == 1 or explicit == wanted:
			continue

		if slugify(EXPLICIT_ID.sub("", text)) == wanted and explicit is None:
			continue

		problems.append(f"{target.relative_to(ROOT)}:{index + 1}: heading needs {{ #{wanted} }}")

		if not check_only:
			bare = EXPLICIT_ID.sub("", text)
			lines[index] = "#" * level + " " + bare + " { #" + wanted + " }"

	if problems and not check_only:
		target.write_text("\n".join(lines) + "\n", encoding="utf-8")

	return problems


def main():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("--check", action="store_true")
	arguments = parser.parse_args()

	problems = []
	source_root = DOCS / SOURCE

	for language in sorted(p for p in DOCS.iterdir() if p.is_dir() and p.name not in (SOURCE, "assets")):
		for target in sorted(language.rglob("*.md")):
			source = source_root / target.relative_to(language)

			if source.exists():
				problems += sync(target, english_ids(source), arguments.check)

	for line in problems:
		print(line)

	if arguments.check:
		print(f"{len(problems)} heading(s) without their English anchor")
		return 1 if problems else 0

	print(f"fixed {len(problems)} heading(s)")
	return 0


if __name__ == "__main__":
	sys.exit(main())
