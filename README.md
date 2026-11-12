# dns-zone-transfer-checker

Check DNS zone-transfer (AXFR) attempts from a CSV: ALLOWED with records transferred is EXPOSED, DENIED/REFUSED is BLOCKED, a TIMEOUT is INCONCLUSIVE — exposed zones first.

## How to run

```sh
python3 main.py attempts.csv
```

## Example output

```
ns1 example.com: EXPOSED (status ALLOWED, 42 record(s) transferred)
ns2 example.org: BLOCKED (status DENIED, 0 record(s) transferred)
1 zone(s) exposed to AXFR.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
