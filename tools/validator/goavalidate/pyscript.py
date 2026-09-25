"""Static analysis of a mod's Python, via ast.

The scripts are never imported or executed - ast.parse only builds a syntax
tree. That is deliberate and must stay that way: a mod script is untrusted
input.
"""

import ast
import dataclasses


@dataclasses.dataclass
class HandlerRef:
	event: str          # as written, e.g. "MissionEvent.GET_MISSION_ID"
	constant: str       # the constant name alone, e.g. "GET_MISSION_ID"
	function: str
	arg_count: int
	line: int


@dataclasses.dataclass
class ScriptFacts:
	handlers: list = dataclasses.field(default_factory=list)
	set_terms: list = dataclasses.field(default_factory=list)   # (key, line)
	mission_id: str = None
	mission_id_line: int = None
	mission_id_dynamic: bool = False
	syntax_error: tuple = None                                   # (message, line)
	term_helpers: dict = dataclasses.field(default_factory=dict)  # name -> key template
	risky_uses: list = dataclasses.field(default_factory=list)    # (what, line)
	file_uses: list = dataclasses.field(default_factory=list)     # (what, line)
	uses_script_data_path: bool = False
	too_new_syntax: list = dataclasses.field(default_factory=list)  # (feature, line)

	def handler_for(self, constant):
		for handler in self.handlers:
			if handler.constant == constant:
				return handler

		return None


def _constant_name(node):
	"""`MissionEvent.GET_MISSION_ID` -> `GET_MISSION_ID`; a bare name stays."""

	if isinstance(node, ast.Attribute):
		return node.attr

	if isinstance(node, ast.Name):
		return node.id

	return None


def _module_constants(tree):
	"""Module-level `NAME = "literal"` assignments, for resolving MISSION_ID."""

	constants = {}

	for node in tree.body:
		if not isinstance(node, ast.Assign) or not isinstance(node.value, ast.Constant):
			continue

		if not isinstance(node.value.value, str):
			continue

		for target in node.targets:
			if isinstance(target, ast.Name):
				constants[target.id] = node.value.value

	return constants


def _resolve_string(node, constants):
	"""Best-effort static value of a string expression.

	Handles a literal, a module constant, `"...".format(CONST)` and an f-string
	interpolating a known constant. Anything else returns None, which callers
	must treat as "unknown", never as a failure.
	"""

	if isinstance(node, ast.Constant) and isinstance(node.value, str):
		return node.value

	if isinstance(node, ast.Name):
		return constants.get(node.id)

	if isinstance(node, ast.JoinedStr):
		parts = []

		for value in node.values:
			if isinstance(value, ast.Constant) and isinstance(value.value, str):
				parts.append(value.value)
			elif isinstance(value, ast.FormattedValue):
				resolved = _resolve_string(value.value, constants)

				if resolved is None:
					return None

				parts.append(resolved)
			else:
				return None

		return "".join(parts)

	if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format":
		template = _resolve_string(node.func.value, constants)

		if template is None:
			return None

		arguments = [_resolve_string(argument, constants) for argument in node.args]

		if any(argument is None for argument in arguments):
			return None

		try:
			return template.format(*arguments)
		except (IndexError, KeyError, ValueError):
			return None

	return None


def _returned_string(function_node, constants):
	"""The string a single-return function yields, if statically knowable."""

	for node in ast.walk(function_node):
		if isinstance(node, ast.Return) and node.value is not None:
			return _resolve_string(node.value, constants)

	return None


def analyse(path):
	"""Parse one script. Never raises on bad input - reports it instead."""

	facts = ScriptFacts()

	try:
		source = path.read_text(encoding="utf-8", errors="replace")
		tree = ast.parse(source)
	except SyntaxError as error:
		facts.syntax_error = (error.msg, error.lineno or 1)
		return facts
	except OSError as error:
		facts.syntax_error = (f"cannot read file: {error}", 1)
		return facts

	constants = _module_constants(tree)

	# Helpers must be known before their call sites are resolved, so this runs
	# as its own pass rather than inline below.
	for node in tree.body:
		if isinstance(node, ast.FunctionDef):
			_read_term_helper(node, facts, constants)

	for node in ast.walk(tree):
		_read_risky_use(node, facts)
		_read_too_new_syntax(node, facts)

		if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
			_read_handlers(node, facts, constants)
		elif isinstance(node, ast.Call):
			_read_set_term(node, facts, constants)
			_read_term_helper_call(node, facts, constants)

	return facts


def _read_term_helper(node, facts, constants):
	"""Recognise `def _term(slot, text): localization.SetTerm(lang, KEY, text)`.

	Mission scripts almost always wrap SetTerm in a small helper, so following
	one level of indirection is the difference between seeing nine loc keys and
	seeing none. Anything more elaborate is left alone.
	"""

	body = [statement for statement in node.body if not isinstance(statement, ast.Pass)]

	if len(body) != 1 or not isinstance(body[0], ast.Expr):
		return

	call = body[0].value

	if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
		return

	if call.func.attr != "SetTerm" or len(call.args) < 2:
		return

	parameters = [argument.arg for argument in node.args.args]

	if not parameters:
		return

	# Resolve the key expression with each parameter standing in for itself, so
	# "missions/{}/{}".format(MISSION_ID, slot) becomes "missions/<id>/{slot}".
	placeholders = dict(constants)

	for parameter in parameters:
		placeholders[parameter] = "\x00" + parameter + "\x00"

	template = _resolve_string(call.args[1], placeholders)

	if template is not None:
		facts.term_helpers[node.name] = (template, parameters)


def _read_term_helper_call(node, facts, constants):
	if not isinstance(node.func, ast.Name):
		return

	helper = facts.term_helpers.get(node.func.id)

	if helper is None:
		return

	template, parameters = helper
	key = template

	for index, parameter in enumerate(parameters):
		marker = "\x00" + parameter + "\x00"

		if marker not in key:
			continue

		if index >= len(node.args):
			return

		value = _resolve_string(node.args[index], constants)

		if value is None:
			return

		key = key.replace(marker, value)

	if "\x00" not in key:
		facts.set_terms.append((key, node.lineno))


def _read_handlers(node, facts, constants):
	for decorator in node.decorator_list:
		if not isinstance(decorator, ast.Call):
			continue

		if getattr(decorator.func, "id", None) != "event_handler" or not decorator.args:
			continue

		constant = _constant_name(decorator.args[0])

		if constant is None:
			continue

		facts.handlers.append(
			HandlerRef(
				event=ast.unparse(decorator.args[0]),
				constant=constant,
				function=node.name,
				arg_count=len(node.args.args),
				line=node.lineno,
			)
		)

		if constant == "GET_MISSION_ID":
			value = _returned_string(node, constants)
			facts.mission_id = value
			facts.mission_id_line = node.lineno
			facts.mission_id_dynamic = value is None


def _read_set_term(node, facts, constants):
	func = node.func

	if not isinstance(func, ast.Attribute) or func.attr != "SetTerm":
		return

	# localization.SetTerm(language, key, text)
	if len(node.args) < 2:
		return

	key = _resolve_string(node.args[1], constants)

	if key is not None:
		facts.set_terms.append((key, node.lineno))


# Modules that reach outside the game: the .NET bridge, the file system, processes and the
# network. The game runs mod scripts without a sandbox, so a mod never needs these and a
# player cannot tell what they do. Importing from the game's own Blindflug.* namespaces is
# the normal scripting API and is not listed here.
RISKY_MODULES = frozenset({
	"clr", "sys", "subprocess", "socket", "ctypes", "urllib", "http", "ftplib", "smtplib",
	"pickle", "marshal", "importlib", "System", "Microsoft",
})

RISKY_CALLS = frozenset({"__import__", "exec", "eval", "compile"})

# File access has one legitimate use: a script keeping its own state in the folder
# game_api.GetScriptDataPath(...) hands out, as the shipped birthday mission does.
FILE_MODULES = frozenset({"os", "shutil", "io"})
FILE_CALLS = frozenset({"open"})


def _classify(name, what, line, facts):
	if name in RISKY_MODULES or name in RISKY_CALLS:
		facts.risky_uses.append((what, line))
	elif name in FILE_MODULES or name in FILE_CALLS:
		facts.file_uses.append((what, line))


def _read_risky_use(node, facts):
	if isinstance(node, ast.Import):
		for alias in node.names:
			_classify(alias.name.split(".")[0], "import " + alias.name, node.lineno, facts)
	elif isinstance(node, ast.ImportFrom):
		module = node.module or ""
		_classify(module.split(".")[0], "from " + module + " import ...", node.lineno, facts)
	elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
		_classify(node.func.id, node.func.id + "(...)", node.lineno, facts)
	elif isinstance(node, ast.Attribute) and node.attr == "GetScriptDataPath":
		facts.uses_script_data_path = True


def _read_too_new_syntax(node, facts):
	"""Syntax the game's IronPython 3.4 cannot parse. f-strings are fine; the game uses them."""

	if isinstance(node, ast.NamedExpr):
		facts.too_new_syntax.append(("the walrus operator :=", node.lineno))
	elif hasattr(ast, "Match") and isinstance(node, ast.Match):
		facts.too_new_syntax.append(("a match statement", node.lineno))
	elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
		if node.args.posonlyargs:
			facts.too_new_syntax.append(("positional-only parameters (/)", node.lineno))
