#!/usr/bin/env python3
import argparse
import ipaddress
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> list[str]:
    source = ROOT / "data" / f"{name}.txt"
    networks = []
    for number, raw in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
        value = raw.split("#", 1)[0].strip()
        if not value:
            continue
        try:
            network = ipaddress.ip_network(value, strict=True)
        except ValueError as error:
            raise SystemExit(f"{source}:{number}: {error}") from error
        if network.version != 4:
            raise SystemExit(f"{source}:{number}: only IPv4 is supported")
        networks.append(network)

    if len(networks) != len(set(networks)):
        raise SystemExit(f"{source}: duplicate networks found")

    for index, network in enumerate(networks):
        for other in networks[index + 1 :]:
            if network.overlaps(other):
                raise SystemExit(f"{source}: overlapping networks: {network}, {other}")

    return [str(network) for network in sorted(networks)]


def render(networks: list[str]) -> str:
    return "payload:\n" + "".join(f"  - {network}\n" for network in networks)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Mihomo YAML rule providers")
    parser.add_argument("--check", action="store_true", help="fail if generated files differ")
    args = parser.parse_args()

    changed = False
    for name in ("nju-campus", "nju-private"):
        target = ROOT / "rules" / f"{name}.yaml"
        expected = render(load(name))
        actual = target.read_text(encoding="utf-8") if target.exists() else ""
        if actual != expected:
            changed = True
            if args.check:
                print(f"out of date: {target.relative_to(ROOT)}")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(expected, encoding="utf-8", newline="\n")
                print(f"updated: {target.relative_to(ROOT)}")

    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
