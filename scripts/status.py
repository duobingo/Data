#!/usr/bin/env python3
"""Record a finished pull in data/status.json and data/status.md. Usage: status.py MODE RC"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from scheduler import write_status  # noqa: E402

write_status(sys.argv[1], int(sys.argv[2]))
