"""Each defect fixture must produce exactly the expected finding.

Asserting on severity as well as rule id matters: a rule silently demoted to a
note still "fires", but no longer fails a build.
"""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from goavalidate.cli import EXIT_FINDINGS, EXIT_OK, EXIT_TOOL_FAILURE, build_report, main
from goavalidate.findings import Severity

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"

EXPECTED = {
	"outcomes_three": ("mission.outcomes.count", Severity.ERROR),
	"outcomes_five": ("mission.outcomes.count", Severity.ERROR),
	"stats_one": ("mission.stats.count", Severity.ERROR),
	"enemy_report_20": ("mission.enemyreport.high", Severity.WARNING),
	# The game looks a mission location up by _locationId alone; without one it is never found.
	"location_id_missing": ("mission.location.id", Severity.ERROR),
	"id_mismatch": ("mission.id.mismatch", Severity.ERROR),
	"dead_handler": ("mission.handler.dead", Severity.WARNING),
	# A mission with data but no script of its own is normal - it runs on the
	# shared default_mission module. It still needs its loc keys defined somewhere.
	"json_only_mission": ("mission.loc.mandatory", Severity.ERROR),
	"orphan_py": ("mission.pair.missing", Severity.ERROR),
	"syntax_error": ("script.syntax", Severity.ERROR),
	"malformed_json": ("json.parse", Severity.ERROR),
	"no_handler": ("mission.handler.missing", Severity.ERROR),
	"duplicate_id": ("mission.id.duplicate", Severity.ERROR),
	# _type 14 is not a known requirement type; the game loads it and never
	# evaluates it - silently, which is why the tool has to catch it.
	"quest_unknown_type": ("quest.requirement.unknowntype", Severity.ERROR),
	# A blank RunwayTier value reaches int.Parse and throws inside the eligibility check,
	# aborting the whole mission draw rather than just skipping this mission.
	"requirement_empty_value": ("mission.requirement.value", Severity.ERROR),
	# Mod scripts run without a sandbox; reaching the file system must be flagged.
	"unsafe_import": ("script.unsafe", Severity.WARNING),
	# IronPython 3.4 cannot parse syntax newer than 3.6 and skips the whole file.
	"too_new_syntax": ("script.syntax.too_new", Severity.ERROR),
	# File access outside the script data folder is legal but noted.
	"file_access": ("script.file_access", Severity.NOTE),
}

# Fixtures that must produce no findings at all.
CLEAN_FIXTURES = {"helper_module", "event_in_missions", "script_only_mission"}


class FixtureTest(unittest.TestCase):
	def test_every_fixture_produces_its_finding(self):
		for name, (rule, severity) in EXPECTED.items():
			with self.subTest(fixture=name):
				report = build_report(FIXTURES / name)
				matching = [f for f in report.findings if f.rule == rule]

				self.assertTrue(matching, f"{name}: expected {rule}, got {[f.rule for f in report.findings]}")
				self.assertEqual(matching[0].severity, severity)

	def test_every_fixture_directory_is_covered(self):
		"""A fixture with no expectation is a test someone forgot to write."""

		on_disk = {p.name for p in FIXTURES.iterdir() if p.is_dir()}

		self.assertEqual(on_disk - set(EXPECTED) - CLEAN_FIXTURES, set())

	def test_event_script_in_a_mod_tree_is_accepted(self):
		"""
		A .py in Missions/ with handlers but no .json is an event script.

		Missions/ is a mod's only script folder, so the folder name cannot settle what a
		script is - the reclassification has to run for proper mod trees, not just loose
		folders. Verified in-game: an event script sat in an Events/ folder for three days
		and never loaded once, because no such folder is ever scanned.
		"""

		report = build_report(FIXTURES / "event_in_missions")

		self.assertEqual([f.rule for f in report.findings], [])

	def test_script_only_mission_needs_no_json(self):
		"""
		A .py that registers initialize_mission authors its own data, so it needs no .json.

		orphan_py is the counter-case: it registers get_mission_id but never sets the mission
		up, so it really is a mission missing its data and still errors.
		"""

		report = build_report(FIXTURES / "script_only_mission")

		self.assertEqual([f.rule for f in report.findings], [])

	def test_helper_module_is_accepted(self):
		"""
		A .py with no handlers and no .json is a helper module, not a broken mission.

		Missions/ is the only folder a mod may put Python in, so this is where quest
		localisation terms and shared constants live. The tool used to report two errors on
		such a file and tell the author to move it to an Events/ folder that does not exist.
		"""

		report = build_report(FIXTURES / "helper_module")

		self.assertEqual([f.rule for f in report.findings], [])

	def test_duplicate_id_reported_once(self):
		"""Two mods defining the same mission: one finding, on the second one."""

		report = build_report(FIXTURES / "duplicate_id")
		duplicates = [f for f in report.findings if f.rule == "mission.id.duplicate"]

		self.assertEqual(len(duplicates), 1)
		self.assertEqual(duplicates[0].unit, "coastal_patrol")

	def test_json_only_mission_is_not_an_orphan(self):
		"""Since missions share default_mission.py, data without a script is fine."""

		report = build_report(FIXTURES / "json_only_mission")
		rules = [f.rule for f in report.findings]

		self.assertNotIn("mission.pair.missing", rules)

	def test_syntax_error_does_not_cascade(self):
		"""A broken script reports once and does not crash the tool."""

		report = build_report(FIXTURES / "syntax_error")
		rules = [f.rule for f in report.findings]

		self.assertEqual(rules.count("script.syntax"), 1)


class ExitCodeTest(unittest.TestCase):
	"""main() prints; the tests only care about the code, so stdout is muted."""

	def _run(self, argv):
		import io
		from contextlib import redirect_stdout

		with redirect_stdout(io.StringIO()):
			return main(argv)

	def test_errors_exit_one(self):
		self.assertEqual(self._run([str(FIXTURES / "stats_one")]), EXIT_FINDINGS)

	def test_warnings_alone_exit_zero(self):
		self.assertEqual(self._run([str(FIXTURES / "dead_handler")]), EXIT_OK)

	def test_strict_promotes_warnings(self):
		self.assertEqual(self._run([str(FIXTURES / "dead_handler"), "--strict"]), EXIT_FINDINGS)

	def test_missing_path_is_tool_failure(self):
		import io
		from contextlib import redirect_stderr

		with redirect_stderr(io.StringIO()):
			self.assertEqual(self._run([str(FIXTURES / "does_not_exist")]), EXIT_TOOL_FAILURE)

	def test_json_output_is_valid(self):
		import io
		import json
		from contextlib import redirect_stdout

		buffer = io.StringIO()

		with redirect_stdout(buffer):
			main([str(FIXTURES / "stats_one"), "--json"])

		payload = json.loads(buffer.getvalue())

		self.assertEqual(payload["schema"], 1)
		self.assertTrue(payload["findings"])


if __name__ == "__main__":
	unittest.main()


class JsonPositionTest(unittest.TestCase):
	"""The line scanner must not be confused by JSON's escaping rules."""

	def setUp(self):
		from goavalidate.jsonpos import key_lines

		self.key_lines = key_lines

	def test_reports_top_level_key_lines(self):
		text = '{\n  "first": 1,\n  "second": [\n    {"nested": 2}\n  ],\n  "third": 3\n}'
		lines = self.key_lines(text)

		self.assertEqual(lines["first"], 2)
		self.assertEqual(lines["second"], 3)
		self.assertEqual(lines["third"], 6)

	def test_nested_keys_are_not_reported(self):
		text = '{\n  "outer": [\n    {"inner": 1}\n  ]\n}'

		self.assertNotIn("inner", self.key_lines(text))

	def test_brace_inside_string_does_not_shift_depth(self):
		text = '{\n  "a": "{not a brace}",\n  "b": 1\n}'
		lines = self.key_lines(text)

		self.assertEqual(lines["b"], 3)

	def test_escaped_quote_does_not_end_string(self):
		text = '{\n  "a": "he said \\"hi\\"",\n  "b": 2\n}'
		lines = self.key_lines(text)

		self.assertEqual(lines["b"], 3)

	def test_finding_carries_the_line(self):
		report = build_report(FIXTURES / "outcomes_three")
		finding = next(f for f in report.findings if f.rule == "mission.outcomes.count")

		self.assertIsNotNone(finding.line)
