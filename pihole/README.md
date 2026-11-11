# MELTYMON Pi-hole Custom Blocklist

A small, manually curated supplement for the MELTYMON Pi-hole installation.

## Design principles

- Add only domains with a documented reason and a trustworthy source.
- Keep this list complementary to HaGeZi Pro++ and HaGeZi TIF.
- Do not import large third-party lists or duplicate their scope.
- Avoid broad vendor, CDN, authentication, update, and infrastructure domains.
- Verify every candidate against the Pi-hole query log before adding it.
- Record the reason and date for each addition in the commit history.

## Usage

The Pi-hole-compatible domain list is:

`custom-blocklist.txt`

Raw URL:

`https://raw.githubusercontent.com/meltymon/meltymon/main/pihole/custom-blocklist.txt`

Add that URL under **Pi-hole → Adlists** after the file contains reviewed entries.

## Current status

The list is intentionally empty at initial creation. This avoids blocking domains speculatively or merely duplicating HaGeZi. We will populate it from observed query-log evidence and documented candidates.

## Entry format

One domain per line. Comments start with `#`.

Example (format only; not an active block entry):

```text
# YYYY-MM-DD — reason/source
example.invalid
```

