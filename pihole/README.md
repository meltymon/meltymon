# MELTYMON Pi-hole Blocklist

A curated, automatically refreshed supplement for Pi-hole. The list aggregates selected advertising, tracking, device-telemetry, malware and phishing feeds into one normalized domain list.

## Pi-hole URL

Add this URL under **Settings → Blocklists**:

`https://raw.githubusercontent.com/meltymon/meltymon/main/pihole/custom-blocklist.txt`

## Scope

- **Ads & privacy:** KADhosts, W3KBL, Matomo referrer spam, AdAway, AdGuard DNS, anudeepND, EasyList, EasyPrivacy, Prigent Ads, Frogeye first-party trackers and FadeMind 2o7Net.
- **Device telemetry:** WindowsSpyBlocker and Perflyst Android, Smart TV and Amazon Fire TV lists.
- **Threat intelligence:** Phishing Army, URLhaus, Spam404, Quidsup malware, DandelionSprout Anti-Malware, Malware Filter phishing, Prigent Malware, RPiList Malware/Phishing, DigitalSide, PhishTank, Phishunt and FadeMind Spam.

The exact source URLs and categories are maintained in [sources.txt](sources.txt).

## Build and maintenance

GitHub Actions refreshes the list daily at 03:17 UTC and supports manual runs from the Actions tab. The builder:

- downloads each source independently and reports per-feed counts;
- accepts hosts-file and common Adblock domain syntax;
- emits exact DNS hostnames only (unsupported regex rules, IPs and URL paths are skipped);
- deduplicates domains across all included feeds;
- continues if an individual source is unavailable, but refuses to publish if fewer than 10 feeds work or fewer than 1,000 unique domains are parsed.

A failed or empty feed therefore cannot silently replace the published list with an empty file.

## Relationship to HaGeZi

This list is intended as a curated supplement to HaGeZi Pro++ and TIF, not as a replacement. Overlap is expected; Pi-hole Gravity deduplicates domains across subscribed lists. The number of entries in this file is not the same as the total number of unique domains in Gravity.

## Deliberately not included

Some submitted sources are omitted initially because they are older, less transparent, have uncertain maintenance, carry a higher false-positive risk, or add little value beside the existing HaGeZi lists. Examples include BarbBlock, Mahakala, hostsfile.org, hostsfile.mine.nu, Joewein, Kowabit, neoHosts, MVPS, yhosts, Disconnect.me, Ad-wars and the broad Frogeye multiparty list.

Perflyst's Pi-hole-compatible Smart TV list is used; the AdGuard Home-specific variant is not.

## License and attribution

This project aggregates third-party feeds. Each upstream source retains its own license and terms. See the upstream project pages for attribution and usage conditions.
