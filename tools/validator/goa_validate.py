#!/usr/bin/env python3
"""Ground of Aces mod validator.

Usage:  python3 goa_validate.py <mod folder>

Checks that a mod will load: JSON structure, file pairing, mission ids and the
script handlers. Standard library only, no installation needed.
"""

import sys

from goavalidate.cli import main

if __name__ == "__main__":
	sys.exit(main())
