"""Renderers. Both consume a Report and nothing else."""

import dataclasses
import json

from .findings import Severity

SCHEMA_VERSION = 1

_ORDER = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.NOTE: 2}


def _relative(path, root):
	try:
		return path.relative_to(root).as_posix()
	except ValueError:
		return path.as_posix()


def render_text(report, root):
	"""One finding per line, `path:line: severity: message`.

	That is the gcc/ruff convention, so editors and CI log parsers pick the
	locations up without configuration.
	"""

	lines = []
	by_file = {}

	for finding in report.findings:
		by_file.setdefault(finding.path, []).append(finding)

	# A finding should always carry a path, but sorting is not the place to discover that
	# one does not: a bare key function turns a reporting gap into a crash that loses every
	# other finding in the run.
	for path in sorted(by_file, key=lambda p: p.as_posix() if p else ""):
		entries = sorted(by_file[path], key=lambda f: (_ORDER[f.severity], f.line or 0))

		for finding in entries:
			base = _relative(path, root) if path else "<unknown>"
			location = f"{base}:{finding.line}" if finding.line else base
			lines.append(f"{location}: {finding.severity.value}: {finding.message}")

			if finding.hint:
				for hint_line in finding.hint.splitlines():
					lines.append(f"    {hint_line}")

	errors = report.count(Severity.ERROR)
	warnings = report.count(Severity.WARNING)
	notes = report.count(Severity.NOTE)

	if lines:
		lines.append("")

	lines.append(f"{report.files_checked} file(s) checked - {errors} error(s), {warnings} warning(s), {notes} note(s)")

	return "\n".join(lines)


def render_json(report, root):
	payload = {
		"schema": SCHEMA_VERSION,
		"catalog": {
			"version": report.catalog_version,
			"generated_at": report.catalog_generated_at,
		},
		"summary": {
			"files_checked": report.files_checked,
			"errors": report.count(Severity.ERROR),
			"warnings": report.count(Severity.WARNING),
			"notes": report.count(Severity.NOTE),
		},
		"findings": [],
	}

	for finding in report.findings:
		entry = dataclasses.asdict(finding)
		entry["severity"] = finding.severity.value
		entry["path"] = _relative(finding.path, root)
		payload["findings"].append(entry)

	return json.dumps(payload, indent=2)
