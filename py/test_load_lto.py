#!/usr/bin/env python3
"""
Tests for the upsert logic in load_lto.py.

Three cases:
  1. New tuple (cspcid, date_from, date_to) → INSERT
  2. Existing tuple, incoming lto is not None → UPDATE lto
  3. Existing tuple, incoming lto is None → keep original lto unchanged
"""
import sys
from datetime import date
from decimal import Decimal

import psycopg2

sys.path.insert(0, '.')
from load_lto import DB_CONFIG, TARGET_TABLE, load_into_db

# Sentinel cspcid prefix unlikely to collide with real data
TEST_PREFIX = 'TEST_UPSERT_'
TABLE = TARGET_TABLE  # public.LTO_sk


def db_connect():
    return psycopg2.connect(**DB_CONFIG)


def fetch_row(cur, cspcid, date_from, date_to):
    cur.execute(
        f"SELECT lto, wholesale FROM {TABLE} WHERE cspcid=%s AND date_from=%s AND date_to=%s",
        (cspcid, date_from, date_to),
    )
    return cur.fetchone()


def cleanup(cur, cspcid_prefix):
    cur.execute(f"DELETE FROM {TABLE} WHERE cspcid LIKE %s", (cspcid_prefix + '%',))


def run_tests():
    passed = 0
    failed = 0

    conn = db_connect()
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            cleanup(cur, TEST_PREFIX)
            conn.commit()

        # ------------------------------------------------------------------ #
        # Case 1: new tuple → should be inserted                             #
        # ------------------------------------------------------------------ #
        cspcid    = TEST_PREFIX + '001'
        date_from = date(2025, 1, 1)
        date_to   = date(2025, 3, 31)
        lto_val       = Decimal('1.50')
        wholesale_val = Decimal('10.00')

        load_into_db([[cspcid, date_from, date_to, lto_val, wholesale_val]])

        with conn.cursor() as cur:
            row = fetch_row(cur, cspcid, date_from, date_to)

        if row is not None and Decimal(str(row[0])) == lto_val and Decimal(str(row[1])) == wholesale_val:
            print(f'PASS  Case 1 – new tuple inserted (lto={row[0]}, wholesale={row[1]})')
            passed += 1
        else:
            print(f'FAIL  Case 1 – expected lto={lto_val}, wholesale={wholesale_val}, got {row}')
            failed += 1

        # ------------------------------------------------------------------ #
        # Case 2: existing tuple, non-null incoming values → UPDATE          #
        # ------------------------------------------------------------------ #
        new_lto = Decimal('2.99')
        new_wholesale = Decimal('12.50')
        load_into_db([[cspcid, date_from, date_to, new_lto, new_wholesale]])

        with conn.cursor() as cur:
            row = fetch_row(cur, cspcid, date_from, date_to)

        if row is not None and Decimal(str(row[0])) == new_lto and Decimal(str(row[1])) == new_wholesale:
            print(f'PASS  Case 2 – existing tuple updated (lto={row[0]}, wholesale={row[1]})')
            passed += 1
        else:
            print(f'FAIL  Case 2 – expected lto={new_lto}, wholesale={new_wholesale}, got {row}')
            failed += 1

        # ------------------------------------------------------------------ #
        # Case 3: existing tuple, None incoming values → originals kept      #
        # ------------------------------------------------------------------ #
        load_into_db([[cspcid, date_from, date_to, None, None]])

        with conn.cursor() as cur:
            row = fetch_row(cur, cspcid, date_from, date_to)

        if row is not None and Decimal(str(row[0])) == new_lto and Decimal(str(row[1])) == new_wholesale:
            print(f'PASS  Case 3 – None values ignored, originals kept (lto={row[0]}, wholesale={row[1]})')
            passed += 1
        else:
            print(f'FAIL  Case 3 – expected lto={new_lto}, wholesale={new_wholesale} (unchanged), got {row}')
            failed += 1

    finally:
        # Always clean up test rows
        with conn.cursor() as cur:
            cleanup(cur, TEST_PREFIX)
        conn.commit()
        conn.close()

    print(f'\n{passed} passed, {failed} failed')
    return failed


if __name__ == '__main__':
    raise SystemExit(run_tests())
