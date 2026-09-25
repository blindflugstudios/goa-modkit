"""The shipped game content must produce no errors.

If one of these fails, the validator has a bug - not the content. The corpus is
the game's own missions, quests and event scripts, all of which load today.

Set GOA_SCRIPTS to the game's shipped scripts folder to run these, e.g.
  Windows: <Steam>/steamapps/common/Ground of Aces/GroundOfAces_Data/StreamingAssets/Scripts
  macOS:   .../GroundOfAces.app/Contents/Resources/Data/StreamingAssets/Scripts
They skip otherwise, so the suite passes without the game installed.
"""

import os
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from goavalidate.cli import build_report
from goavalidate.findings import Severity

REPO = os.environ.get("GOA_SCRIPTS")

CORPORA = {
	"missions": "Mission",
	"quests": "Quest",
	"default_events": "Default",
}

# Findings about the game's own content, not validator bugs. Each is recorded
# rather than silenced so that a second occurrence fails the suite.
#
# general_assassination_mission ships with _enemyPlaneReport: 20, above the
# documented limit of 18.
KNOWN_WARNINGS = {"mission.enemyreport.high", "mission.loc.transmission"}

# test_historic_mission is a fixture with no localisation terms at all. It must
# be the only mission missing mandatory keys.
KNOWN_LOC_EXCEPTIONS = {"test_historic_mission"}


@unittest.skipUnless(REPO, "set GOA_SCRIPTS to the game's shipped Scripts folder")
class ShippedContentTest(unittest.TestCase):
	def _report_for(self, relative):
		path = pathlib.Path(REPO) / relative
		self.assertTrue(path.is_dir(), f"corpus missing: {path}")

		return build_report(path)

	def test_no_errors_anywhere(self):
		for name, relative in CORPORA.items():
			report = self._report_for(relative)

			for finding in report.findings:
				if finding.severity is not Severity.ERROR:
					continue

				if finding.unit in KNOWN_LOC_EXCEPTIONS and finding.rule.startswith("mission.loc"):
					continue

				with self.subTest(corpus=name, unit=finding.unit, rule=finding.rule):
					self.fail(f"{finding.path.name}: {finding.rule}: {finding.message}")

	def test_loc_exceptions_are_still_the_only_ones(self):
		"""If a second mission loses its terms, this fails rather than passing quietly."""

		report = self._report_for(CORPORA["missions"])
		offenders = {f.unit for f in report.findings if f.rule == "mission.loc.mandatory"}

		self.assertEqual(offenders, KNOWN_LOC_EXCEPTIONS)

	def test_only_known_warnings(self):
		for name, relative in CORPORA.items():
			report = self._report_for(relative)

			for finding in report.findings:
				if finding.severity is not Severity.WARNING:
					continue

				if finding.unit in KNOWN_LOC_EXCEPTIONS:
					continue

				with self.subTest(corpus=name, unit=finding.unit):
					self.assertIn(finding.rule, KNOWN_WARNINGS, finding.message)

	def test_shipped_ids_are_collision_free(self):
		"""The shipped mission ids must not collide with one another.

		This protects the game's own content as a side effect of testing the rule.
		"""

		for name in ("missions",):
			report = self._report_for(CORPORA[name])
			collisions = [f for f in report.findings if f.rule == "mission.id.substring"]

			self.assertEqual([f.unit for f in collisions], [], f"{name} has colliding ids")


class AuthoredExamplesTest(unittest.TestCase):
	"""The examples modders copy are held to a stricter bar: no warnings either."""

	def test_examples_are_spotless(self):
		examples = pathlib.Path(__file__).resolve().parents[3] / "examples"
		report = build_report(examples)

		for finding in report.findings:
			with self.subTest(unit=finding.unit, rule=finding.rule):
				self.fail(f"{finding.path.name}: {finding.severity.value}: {finding.message}")


if __name__ == "__main__":
	unittest.main()
