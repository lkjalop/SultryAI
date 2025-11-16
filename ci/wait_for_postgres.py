#!/usr/bin/env python3
"""Simple Postgres readiness checker used by CI.

Usage: python ci/wait_for_postgres.py --dsn postgresql://user:pass@host:port/db --timeout 60
"""
import argparse
import sys
import time

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--dsn', required=True, help='Postgres DSN')
    p.add_argument('--timeout', type=int, default=60, help='Seconds to wait')
    return p.parse_args()


def main():
    args = parse_args()
    try:
        import psycopg
    except Exception as e:
        print('psycopg not installed:', e)
        sys.exit(2)

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        try:
            conn = psycopg.connect(args.dsn)
            conn.close()
            print('Postgres ready')
            return 0
        except Exception as e:
            print('Waiting for Postgres...', e)
            time.sleep(2)

    print('Timed out waiting for Postgres')
    return 1


if __name__ == '__main__':
    sys.exit(main())
