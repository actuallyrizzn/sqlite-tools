import sqlite3
import os
import subprocess
import sys
import argparse
import time

def check_db_lock(db_file):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('PRAGMA quick_check')
        return False
    except sqlite3.OperationalError as e:
        if 'database is locked' in str(e):
            return True
        raise e

def main():
    parser = argparse.ArgumentParser(description='Check if a SQLite database is locked and execute a script if it is not.')
    parser.add_argument('db_file', help='The SQLite database file to check')
    parser.add_argument('script', nargs='?', help='The script to run if the database is not locked')
    parser.add_argument('script_args', nargs=argparse.REMAINDER, help='Arguments to pass to the script')
    parser.add_argument('-r', '--retry', action='store_true', help='Retry after 30 seconds if the database is locked')

    args = parser.parse_args()

    while check_db_lock(args.db_file):
        if args.retry:
            time.sleep(30)
        else:
            print("Database locked")
            sys.exit(1)

    if args.script:
        command = [args.script] + args.script_args
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout.decode())
        if stderr:
            print(stderr.decode())

if __name__ == "__main__":
    main()
