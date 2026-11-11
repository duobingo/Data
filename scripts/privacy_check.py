#!/usr/bin/env python3
"""Refuse to publish personal information.

Runs before every commit (in the workflows) and fails if any file that would be published
contains a blocked word or a personal email address. Blocked words are stored only as SHA-256
hashes, so this check itself doesn't reveal what it protects. Also fails if a positions file
(lots / cash / pending orders) appears anywhere in the repo.

Usage: python scripts/privacy_check.py   (exit code 1 = blocked)
"""
import hashlib
import pathlib
import re
import subprocess
import sys

BLOCKED_HASHES = {
    "c4cfd351a5c5ee058022e74356fc5483782a4a396d80b058b3358027a88821bb",
    "3178e160fe176553b614d55ba83194a257b93c2139b23345f226a0a6df58c489",
    "2855df4891b14aced85046d0f53a17c00783020b3da08398cc43e07ba6f122d8",
    "a48d4f176b319b510346868c9c71690f15b665dffa544eeb7722223c6c7aa444",
    "2dc89cd55e05e30d7235fd417bfdb2f02dc747ab467d590fd61115bbd95f8b58",
}
EMAIL = re.compile(r"[\w.+-]+@(?!users\.noreply\.github\.com)(gmail|hotmail|outlook|yahoo|icloud|live|aol|proton(mail)?)\.\w+", re.I)
POSITIONS = re.compile(r"^\s*(positions|pending|cash)\s*:", re.M)
ALLOWED_POSITIONS_FILES = {"config/positions.example.yml"}


def files():
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, text=True, check=True).stdout.split()
    return [f for f in out if pathlib.Path(f).is_file()]


def main():
    problems = []
    for f in files():
        try:
            text = pathlib.Path(f).read_text(errors="ignore")
        except Exception:  # noqa: BLE001
            continue
        for tok in set(re.findall(r"[a-z0-9]+", text.lower())):
            if hashlib.sha256(tok.encode()).hexdigest() in BLOCKED_HASHES:
                problems.append(f"{f}: contains a blocked personal word")
                break
        if EMAIL.search(text):
            problems.append(f"{f}: contains a personal email address")
        if f.endswith((".yml", ".yaml")) and f not in ALLOWED_POSITIONS_FILES and POSITIONS.search(text):
            problems.append(f"{f}: looks like a positions/cash file")
    if problems:
        print("PRIVACY CHECK FAILED — nothing will be published:")
        print("\n".join(f"- {p}" for p in problems))
        return 1
    print("Privacy check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
