"""The finding model. Everything the validator reports is one of these."""

import dataclasses
import enum
import pathlib


class Severity(enum.Enum):
	"""How much a finding matters.

	ERROR   the mod will not load, or will load and crash, or will silently
	        load the wrong thing.
	WARNING it loads and runs, but does something the author did not intend.
	NOTE    informational, including "this check was skipped".
	"""

	ERROR = "error"
	WARNING = "warning"
	NOTE = "note"


@dataclasses.dataclass(frozen=True)
class Finding:
	"""One problem found in one file.

	`rule` is the stable identity - tests assert on it, JSON consumers key on
	it, and a future --ignore flag would filter on it. Never assert on prose.

	`message` says what is wrong; `hint` says what to do about it. They stay
	separate so each renderer can format them independently.
	"""

	rule: str
	severity: Severity
	path: pathlib.Path
	message: str
	line: int = None
	hint: str = None
	unit: str = None


@dataclasses.dataclass
class Report:
	"""Everything one validation run produced."""

	findings: list = dataclasses.field(default_factory=list)
	files_checked: int = 0
	catalog_version: str = None
	catalog_generated_at: str = None

	def add(self, finding):
		self.findings.append(finding)

	def extend(self, findings):
		self.findings.extend(findings)

	def count(self, severity):
		return sum(1 for f in self.findings if f.severity is severity)

	@property
	def has_errors(self):
		return self.count(Severity.ERROR) > 0
