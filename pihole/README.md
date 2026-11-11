# MELTYMON Pi-hole Blocklist

A focused, automatically refreshed supplement for the Pi-hole installation.

## Current scope

- Actively reported phishing domains from the Phishunt community feed.
- Domains are normalized, deduplicated, and syntax-checked before publication.
- Broad hosting platforms and provider root domains are not intentionally added.
- The upstream feed is licensed CC0 1.0.

## Pi-hole URL

Add this URL under **Settings → Blocklists**:

`https://raw.githubusercontent.com/meltymon/meltymon/main/pihole/custom-blocklist.txt`

## Maintenance

GitHub Actions refreshes the list daily at 03:17 UTC and can also be run manually from the Actions tab. The workflow refuses to replace the list if the upstream feed returns no valid domains.

This list complements rather than replaces HaGeZi Pro++ and TIF. Some overlap is expected; Pi-hole's gravity build deduplicates domains across lists.

## Source

- Phishunt blocklist: https://phishunt.io/blocklist/domains.txt
- Project/API documentation: https://phishunt.io/api/
