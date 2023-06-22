import os
import sqlite3
import argparse
import logging

def connect_to_database():
    # Get database name from environment variable
    db_name = os.getenv('DATABASE_NAME')
    if db_name is None:
        raise ValueError('DATABASE_NAME environment variable is not set.')

    try:
        # Connect to the database
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.OperationalError as e:
        print(f'Could not connect to database: {e}')
        exit(1)

def get_valid_tables(cursor):
    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    valid_tables = [table[0] for table in cursor.fetchall()]
    return valid_tables

def validate_table(cursor, table_name):
    valid_tables = get_valid_tables(cursor)
    if table_name not in valid_tables:
        print(f'Invalid table name: {table_name}')
        exit(1)

def get_valid_columns(cursor, table_name):
    # Get the list of columns in the table
    cursor.execute(f'PRAGMA table_info({table_name});')
    valid_columns = [column[1] for column in cursor.fetchall()]
    return valid_columns

def validate_columns(cursor, table_name, field_name, index_field_name):
    valid_columns = get_valid_columns(cursor, table_name)
    if field_name not in valid_columns:
        print(f'Invalid column name: {field_name}')
        exit(1)
    if index_field_name not in valid_columns:
        print(f'Invalid index field name: {index_field_name}')
        exit(1)

def execute_sql_statement(cursor, sql, data):
    try:
        # Execute the SQL statement
        cursor.execute(sql, data)
        cursor.connection.commit()
    except sqlite3.OperationalError as e:
        print(f'Error executing SQL statement: {e}')

def main():
    parser = argparse.ArgumentParser(description='Write data to a SQLite database.')
    parser.add_argument('table', help='Name of the table to write to. If the table name contains spaces or special characters, enclose it in quotes.')
    parser.add_argument('index', help='Index of the record to write to.')
    parser.add_argument('field', help='Name of the field to write to. If the field name contains spaces or special characters, enclose it in quotes.')
    parser.add_argument('data', help='Data to write. If the data contains spaces or special characters, enclose it in quotes.')
    parser.add_argument('--index_field', default='id', help='Name of the index field. Default is "id". If the index field name contains spaces or special characters, enclose it in quotes.')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose on-screen updates.')
    parser.add_argument('--log_file', help='Path to the log file for verbose logging.')
    args = parser.parse_args()

    conn = connect_to_database()
    cursor = conn.cursor()

    validate_table(cursor, args.table)
    validate_columns(cursor, args.table, args.field, args.index_field)

    row = cursor.execute(f'SELECT 1 FROM {args.table} WHERE {args.index_field}=?', (args.index,)).fetchone()

    if row is not None:
        sql = f'UPDATE {args.table} SET {args.field} = ? WHERE {args.index_field} = ?'
        data = (args.data, args.index)
    else:
        sql = f'INSERT INTO {args.table} ({args.index_field}, {args.field}) VALUES (?, ?)'
        data = (args.index, args.data)

    execute_sql_statement(cursor, sql, data)
    conn.close()

    # Verbose on-screen updates
    if args.verbose:
        print('Data written successfully to the SQLite database.')

    # Verbose logging to file
    if args.log_file:
        logging.basicConfig(filename=args.log_file, level=logging.INFO)
        logging.info(f'Data written to {args.table}: Index={args.index}, Field={args.field}, Data={args.data}')

if __name__ == '__main__':
    main()

ChatGPT
