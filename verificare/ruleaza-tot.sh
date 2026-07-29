#!/usr/bin/env bash
# Rulează toate verificările. Cod de ieșire 0 doar dacă toate trec.
set -u
cd "$(dirname "$0")/.."
esec=0
for v in trasabilitate descriptori volum minute; do
  echo "── $v ──"
  python3 "verificare/$v.py" || esec=1
done
python3 verificare/test_fm.py || esec=1
exit $esec
