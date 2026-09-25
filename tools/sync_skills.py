"""Mirror the canonical skills in .agents/skills/ to .claude/skills/.

Codex reads skills from .agents/skills/, Claude Code from .claude/skills/. The
.agents copy is the one people edit; this script makes the .claude copy an exact
mirror of it, removing anything stale.

    python tools/sync_skills.py          copy
    python tools/sync_skills.py --check  exit 1 if the two differ, change nothing

Standard library only, Python 3.9+.
"""

import argparse
import filecmp
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SOURCE = REPO / ".agents" / "skills"
TARGET = REPO / ".claude" / "skills"
IGNORED_NAMES = {".DS_Store", "__pycache__"}


def relative_files(root):
	"""Every file under root as a relative path, skipping OS and cache clutter."""

	if root.is_dir() is False:
		return set()

	files = set()

	for path in root.rglob("*"):
		if any(part in IGNORED_NAMES for part in path.relative_to(root).parts):
			continue

		if path.is_file():
			files.add(path.relative_to(root))

	return files


def differences():
	"""Human-readable list of what differs between SOURCE and TARGET."""

	source_files = relative_files(SOURCE)
	target_files = relative_files(TARGET)
	found = []

	for path in sorted(source_files - target_files):
		found.append("missing in .claude/skills: {}".format(path))

	for path in sorted(target_files - source_files):
		found.append("stale in .claude/skills: {}".format(path))

	for path in sorted(source_files & target_files):
		if filecmp.cmp(SOURCE / path, TARGET / path, shallow=False) is False:
			found.append("differs: {}".format(path))

	return found


def sync():
	if SOURCE.is_dir() is False:
		print("sync_skills: no {} folder".format(SOURCE.relative_to(REPO)), file=sys.stderr)
		return 2

	if TARGET.exists():
		shutil.rmtree(TARGET)

	shutil.copytree(SOURCE, TARGET, ignore=shutil.ignore_patterns(*IGNORED_NAMES))
	print("Mirrored {} skill(s) to {}".format(
		sum(1 for child in SOURCE.iterdir() if child.is_dir()),
		TARGET.relative_to(REPO)))
	return 0


def main(argv=None):
	parser = argparse.ArgumentParser(description="Mirror .agents/skills to .claude/skills.")
	parser.add_argument("--check", action="store_true", help="report differences and exit 1, change nothing")
	arguments = parser.parse_args(argv)

	if arguments.check:
		found = differences()

		for line in found:
			print(line)

		if found:
			print("Run: python tools/sync_skills.py")
			return 1

		print("Skills are in sync.")
		return 0

	return sync()


if __name__ == "__main__":
	sys.exit(main())
