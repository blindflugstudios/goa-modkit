"""Keep the skills and helper agents identical for every supported agent.

Skills: Codex and OpenCode read .agents/skills/, Claude Code reads .claude/skills/.
The .agents copy is the one people edit; this script makes the .claude copy an exact
mirror of it, removing anything stale.

Agents: Claude Code reads .claude/agents/*.md, OpenCode reads .opencode/agents/*.md
with a different frontmatter. The .claude copy is the one people edit; this script
writes the OpenCode version from it (same instructions, translated frontmatter).

    python tools/sync_skills.py          copy / generate
    python tools/sync_skills.py --check  exit 1 if anything differs, change nothing

Standard library only, Python 3.9+.
"""

import argparse
import filecmp
import json
import pathlib
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
SOURCE = REPO / ".agents" / "skills"
TARGET = REPO / ".claude" / "skills"
IGNORED_NAMES = {".DS_Store", "__pycache__"}

CLAUDE_AGENTS = REPO / ".claude" / "agents"
OPENCODE_AGENTS = REPO / ".opencode" / "agents"
GENERATED_NOTE = "<!-- Generated from .claude/agents/{} by tools/sync_skills.py - edit that file instead. -->\n\n"


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


def split_frontmatter(text):
	"""(fields, body) of a Markdown file with simple `key: value` frontmatter."""

	if text.startswith("---\n") is False:
		return {}, text

	end = text.index("\n---\n", 4)
	fields = {}

	for line in text[4:end].splitlines():
		if ":" in line:
			key, value = line.split(":", 1)
			fields[key.strip()] = value.strip()

	return fields, text[end + 5:].lstrip("\n")


def opencode_agent(path):
	"""The OpenCode version of one Claude Code agent file.

	A Claude agent without Edit or Write in its tools must not change files, so its
	OpenCode twin gets `edit: deny`. The description is written as a JSON string,
	which is valid YAML whatever quotes or colons it contains.
	"""

	fields, body = split_frontmatter(path.read_text(encoding="utf-8"))
	tools = {tool.strip() for tool in fields.get("tools", "").split(",")}
	can_edit = bool(tools & {"Edit", "Write", "MultiEdit"})

	return (
		"---\n"
		"description: {}\n"
		"mode: subagent\n"
		"permission:\n"
		"  edit: {}\n"
		"---\n\n"
	).format(json.dumps(fields.get("description", "")), "allow" if can_edit else "deny") + GENERATED_NOTE.format(path.name) + body


def agent_differences():
	found = []
	sources = {path.name: path for path in CLAUDE_AGENTS.glob("*.md")} if CLAUDE_AGENTS.is_dir() else {}
	targets = {path.name: path for path in OPENCODE_AGENTS.glob("*.md")} if OPENCODE_AGENTS.is_dir() else {}

	for name in sorted(set(sources) - set(targets)):
		found.append("missing in .opencode/agents: {}".format(name))

	for name in sorted(set(targets) - set(sources)):
		found.append("stale in .opencode/agents: {}".format(name))

	for name in sorted(set(sources) & set(targets)):
		if targets[name].read_text(encoding="utf-8") != opencode_agent(sources[name]):
			found.append("differs: .opencode/agents/{}".format(name))

	return found


def sync_agents():
	if CLAUDE_AGENTS.is_dir() is False:
		return

	if OPENCODE_AGENTS.exists():
		shutil.rmtree(OPENCODE_AGENTS)

	OPENCODE_AGENTS.mkdir(parents=True)
	count = 0

	for path in sorted(CLAUDE_AGENTS.glob("*.md")):
		(OPENCODE_AGENTS / path.name).write_text(opencode_agent(path), encoding="utf-8")
		count += 1

	print("Generated {} agent(s) in {}".format(count, OPENCODE_AGENTS.relative_to(REPO)))


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
	sync_agents()
	return 0


def main(argv=None):
	parser = argparse.ArgumentParser(description="Mirror skills to .claude/skills and agents to .opencode/agents.")
	parser.add_argument("--check", action="store_true", help="report differences and exit 1, change nothing")
	arguments = parser.parse_args(argv)

	if arguments.check:
		found = differences() + agent_differences()

		for line in found:
			print(line)

		if found:
			print("Run: python tools/sync_skills.py")
			return 1

		print("Skills and agents are in sync.")
		return 0

	return sync()


if __name__ == "__main__":
	sys.exit(main())
