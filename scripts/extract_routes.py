#!/usr/bin/env python3
import argparse
import ipaddress
import re
from pathlib import Path

PATTERN = re.compile(r"\bAdd route to\s+([^\s]+)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract server-pushed CIDRs from an EZ4Connect log")
    parser.add_argument("log", type=Path)
    args = parser.parse_args()

    found = set()
    for match in PATTERN.finditer(args.log.read_text(encoding="utf-8", errors="replace")):
        try:
            found.add(ipaddress.ip_network(match.group(1), strict=True))
        except ValueError:
            pass

    for network in sorted(found):
        print(network)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
