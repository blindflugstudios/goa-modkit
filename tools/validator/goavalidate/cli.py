"""Command line entry point."""

import argparse
import pathlib
import sys

from . import rules
from .catalog import Catalog, load as load_catalog
from .discover import discover
from .findings import Finding, Report, Severity
from .jsonpos import key_lines
from .pyscript import analyse
from .report import render_json, render_text

EXIT_OK = 0
EXIT_FINDINGS = 1
EXIT_TOOL_FAILURE = 2


def build_report(root, catalog=None):
	discovery = discover(root)

	if catalog is None:
		catalog = load_catalog()

	report = Report(
		files_checked=discovery.file_count,
		catalog_version=catalog.game_version,
		catalog_generated_at=catalog.generated_at,
	)

	# Missions in this run count as known, so a chain inside one mod does not
	# look like a reference to something missing.
	local_ids = {unit.stem for unit in discovery.missions}

	# Analyse every script first: a mission with no script of its own may still get
	# its localisation terms from any other script the mod loads, so the whole set
	# has to be known before the loc rule runs.
	mission_facts = {}
	event_facts = {}
	mod_terms = set()

	# Keyed by script path, not by stem. Two units can share a stem - Mission/x.json and
	# OldMission/x.py are separate units - and a stem key hands the JSON-only unit the
	# legacy script's facts, which reports that script's findings against no file at all.
	for unit in discovery.missions:
		if unit.py_path is None:
			continue

		facts = analyse(unit.py_path)
		mission_facts[unit.py_path] = facts

		if facts.syntax_error is None:
			mod_terms.update(key for key, _ in facts.set_terms)

	for unit in discovery.events:
		facts = analyse(unit.py_path)
		event_facts[unit.stem] = facts

		if facts.syntax_error is None:
			mod_terms.update(key for key, _ in facts.set_terms)

	for unit in discovery.missions:
		facts = mission_facts.get(unit.py_path) if unit.py_path else None

		report.extend(rules.check_pairing(unit, facts))
		data = None

		if unit.json_path:
			data, error = rules.load_json(unit.json_path)

			if error:
				report.add(
					Finding(
						rule="json.parse",
						severity=Severity.ERROR,
						path=unit.json_path,
						message=f"invalid JSON: {error}",
						unit=unit.stem,
					)
				)
			else:
				positions = key_lines(unit.json_path.read_text(encoding="utf-8-sig"))
				report.extend(rules.check_mission_json(unit, data, positions))
				report.extend(rules.check_mission_catalog(unit, data, positions, catalog, local_ids))

		if facts is not None and facts.syntax_error:
			message, line = facts.syntax_error
			report.add(
				Finding(
					rule="script.syntax",
					severity=Severity.ERROR,
					path=unit.py_path,
					line=line,
					message=f"Python syntax error: {message}",
					hint="The whole file is skipped by the game; no handler in it registers.",
					unit=unit.stem,
				)
			)
			continue

		if facts is not None:
			report.extend(rules.check_mission_script(unit, facts))
			report.extend(rules.check_script_safety(unit, facts, unit.py_path))

		# Runs with or without a script of its own - a JSON-only mission shares
		# default_mission.py and still needs its nine keys defined somewhere.
		if unit.json_path:
			report.extend(rules.check_localization(unit, facts, catalog, mod_terms, data))

	for unit in discovery.events:
		facts = event_facts[unit.stem]

		if facts.syntax_error:
			message, line = facts.syntax_error
			report.add(
				Finding(
					rule="script.syntax",
					severity=Severity.ERROR,
					path=unit.py_path,
					line=line,
					message=f"Python syntax error: {message}",
					unit=unit.stem,
				)
			)
		else:
			report.extend(rules.check_event_script(unit, facts, catalog))
			report.extend(rules.check_script_safety(unit, facts, unit.py_path))

	for unit in discovery.quests:
		data, error = rules.load_json(unit.json_path)

		if error:
			report.add(
				Finding(
					rule="json.parse",
					severity=Severity.ERROR,
					path=unit.json_path,
					message=f"invalid JSON: {error}",
					unit=unit.stem,
				)
			)
		else:
			positions = key_lines(unit.json_path.read_text(encoding="utf-8-sig"))
			report.extend(rules.check_quest(unit, data, positions, catalog))

	report.extend(rules.check_id_collisions(discovery.missions, catalog.mission_ids))

	return report


def main(argv=None):
	parser = argparse.ArgumentParser(
		prog="goa-validate",
		description="Check a Ground of Aces mod for problems that stop it loading.",
	)
	parser.add_argument("path", help="mod folder, content folder, or a single file")
	parser.add_argument("--json", action="store_true", dest="as_json", help="machine-readable output")
	parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
	parser.add_argument(
		"--no-catalog",
		action="store_true",
		help="skip checks that compare against the shipped game data",
	)

	arguments = parser.parse_args(argv)
	root = pathlib.Path(arguments.path)

	if not root.exists():
		print(f"goa-validate: no such path: {root}", file=sys.stderr)
		return EXIT_TOOL_FAILURE

	report = build_report(root, Catalog() if arguments.no_catalog else None)

	if arguments.as_json:
		print(render_json(report, root))
	else:
		print(render_text(report, root))

	if report.has_errors:
		return EXIT_FINDINGS

	if arguments.strict and report.count(Severity.WARNING):
		return EXIT_FINDINGS

	return EXIT_OK
