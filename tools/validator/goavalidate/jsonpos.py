"""Line numbers for JSON fields.

json.load discards positions, so this makes a second pass over the raw text and
records where each top-level key starts. It never interprets values, so it
cannot disagree with json.load about what the document means - only about where
things are. A miss yields no line number, never a wrong finding.
"""


def _skip_string(text, index):
	"""Return the index just past a string starting at `text[index] == '"'`."""

	index += 1

	while index < len(text):
		character = text[index]

		if character == "\\":
			index += 2
			continue

		if character == '"':
			return index + 1

		index += 1

	return index


def key_lines(text):
	"""Map each top-level key to the 1-based line its name appears on.

	Only depth 1 is recorded. Every rule that needs a line number points at a
	top-level field, and going deeper would mean tracking array indices for no
	benefit.
	"""

	lines = {}
	depth = 0
	line = 1
	index = 0
	length = len(text)

	while index < length:
		character = text[index]

		if character == "\n":
			line += 1
			index += 1
			continue

		if character == '"':
			start = index
			end = _skip_string(text, index)

			# A string at depth 1 followed by a colon is a top-level key.
			if depth == 1:
				lookahead = end

				while lookahead < length and text[lookahead] in " \t\r\n":
					lookahead += 1

				if lookahead < length and text[lookahead] == ":":
					name = text[start + 1:end - 1]

					if name not in lines:
						lines[name] = line

			line += text.count("\n", start, end)
			index = end
			continue

		if character in "{[":
			depth += 1
		elif character in "}]":
			depth -= 1

		index += 1

	return lines
