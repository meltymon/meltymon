#!/usr/bin/env python3
"""Build the MELTYMON Pi-hole list from curated public feeds."""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources.txt"
OUTPUT = ROOT / "custom-blocklist.txt"
USER_AGENT = "MELTYMON-Pi-hole-Blocklist/2.0"
TIMEOUT = 45
MIN_SUCCESSFUL_FEEDS = 10
MIN_UNIQUE_DOMAINS = 1_000

DOMAIN_RE = re.compile(
    r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?[.])+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)
ADBLOCK_RE = re.compile(r"^\\|\\|([a-z0-9.-]+)\\^", re.IGNORECASE)
HOSTS_IPS = {"0.0.0.0", "127.0.0.1", "::1", "::"}
LOCAL_NAMES = {"localhost", "local", "lan", "home", "home.arpa", "invalid", "test", "example"}


def parse_line(line: str) -> str | None:
    value = line.strip()
    if not value or value.startswith(("#", "!", "[", "@@")):
        return None

    # Adblock syntax: ||tracker.example^
    match = ADBLOCK_RE.match(value)
    if match:
        candidate = match.group(1).lower().rstrip(".")
    else:
        fields = value.split()
        if not fields:
            return None
        if fields[0] in HOSTS_IPS and len(fields) >= 2:
            candidate = fields[1].lower().rstrip(".")
        else:
            candidate = fields[0].lower().rstrip(".")

    # Ignore wildcard, regex, IP, URL/path and non-domain rules.
    if candidate.startswith("*."):
        candidate = candidate[2:]
    if "://" in candidate or "/" in candidate or "*" in candidate or "^" in candidate:
        return None
    if candidate.startswith("||"):
        candidate = candidate[2:].rstrip("^|")
    if candidate.startswith("www.") and candidate.count(".") < 2:
        pass
    if not DOMAIN_RE.fullmatch(candidate):
        return None
    labels = candidate.split(".")
    if len(labels) < 2 or labels[-1] in LOCAL_NAMES or candidate in LOCAL_NAMES:
        return None
    return candidate


def load_sources() -> list[tuple[str, str, str]]:
    result = []
    for raw in SOURCES.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 2)
        if len(parts) != 3:
            raise ValueError(f"Invalid source entry: {line}")
        result.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))
    return result


def main() -> int:
    all_domains: set[str] = set()
    source_counts: list[tuple[str, str, int]] = []
    failures: list[tuple[str, str]] = []

    for name, category, url in load_sources():
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                raw = response.read(50 * 1024 * 1024 + 1)
            if len(raw) > 50 * 1024 * 1024:
                raise ValueError("feed exceeds 50 MiB safety limit")
            text = raw.decode("utf-8-sig", errors="replace")
            if "<html" in text[:1000].lower() or "<!doctype html" in text[:1000].lower():
                raise ValueError("received HTML instead of a blocklist")
            domains = {domain for line in text.splitlines() if (domain := parse_line(line))}
            if not domains:
                raise ValueError("no valid domain entries parsed")
            all_domains.update(domains)
            source_counts.append((name, category, len(domains)))
            print(f"OK   {name}: {len(domains):,} valid domains")
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
            failures.append((name, str(exc)))
            print(f"WARN {name}: {exc}", file=sys.stderr)

    print(f"Successful feeds: {len(source_counts)}/{len(load_sources())}")
    print(f"Unique domains: {len(all_domains):,}")
    if failures:
        print("Unavailable/invalid feeds:")
        for name, reason in failures:
            print(f" - {name}: {reason}")

    if len(source_counts) < MIN_SUCCESSFUL_FEEDS:
        raise SystemExit(f"Only {len(source_counts)} feeds succeeded; refusing to publish.")
    if len(all_domains) < MIN_UNIQUE_DOMAINS:
        raise SystemExit(f"Only {len(all_domains)} domains parsed; refusing to overwrite current list.")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    categories = Counter(category for _, category, _ in source_counts)
    header = [
        "# MELTYMON Community Blocklist",
        "# Generated automatically from curated third-party feeds.",
        f"# Generated: {now}",
        f"# Successful feeds: {len(source_counts)}/{len(load_sources())}",
        f"# Unique exact domains: {len(all_domains)}",
        "# Categories: " + ", ".join(f"{key} ({value} feeds)" for key, value in sorted(categories.items())),
        "# Source manifest: https://github.com/meltymon/meltymon/blob/main/pihole/sources.txt",
        "# Feed overlap is expected; Pi-hole Gravity deduplicates across subscribed lists.",
        "# Domain-only output; unsupported adblock rules, URLs, IPs and regex rules are skipped.",
        "",
    ]
    OUTPUT.write_text("\n".join(header + sorted(all_domains)) + "\n", encoding="utf-8")
    print(f"Published {len(all_domains):,} unique domains to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
