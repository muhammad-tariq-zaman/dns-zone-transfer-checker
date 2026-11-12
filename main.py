"""Check DNS zone-transfer (AXFR) attempts and flag exposed zones.

Usage: python3 main.py attempts.csv
CSV columns: server,zone,axfr_status,records_transferred.
axfr_status is one of ALLOWED, DENIED, REFUSED, TIMEOUT.
- EXPOSED: AXFR was ALLOWED and records were transferred — anyone
  can copy the whole zone, so this needs fixing at once.
- ALLOWED (EMPTY): AXFR was allowed but no records came back.
- BLOCKED: the server DENIED or REFUSED the transfer (good).
- INCONCLUSIVE: the attempt TIMED OUT — retest before trusting it.
EXPOSED rows first, so the worst finding is on top.
"""
import argparse, csv, sys

def check(rows):
    out = []
    for row in rows:
        status = row["axfr_status"].strip().upper()
        records = int(row["records_transferred"])
        if status == "ALLOWED" and records > 0:
            verdict = "EXPOSED"
        elif status == "ALLOWED":
            verdict = "ALLOWED (EMPTY)"
        elif status in ("DENIED", "REFUSED"):
            verdict = "BLOCKED"
        else:
            verdict = "INCONCLUSIVE"
        out.append((row["server"].strip(), row["zone"].strip(), status,
                    records, verdict))
    rank = {"EXPOSED": 0, "ALLOWED (EMPTY)": 1, "INCONCLUSIVE": 2, "BLOCKED": 3}
    return sorted(out, key=lambda r: (rank[r[4]], r[0], r[1]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)))
    for server, zone, status, records, verdict in results:
        print(f"{server} {zone}: {verdict} (status {status}, {records} record(s) transferred)")
    print(f"{sum(1 for *_, v in results if v == 'EXPOSED')} zone(s) exposed to AXFR.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
