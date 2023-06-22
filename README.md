# SQLite Database Utilities

This repository includes two Python scripts that allow users to interact with SQLite databases in different ways:

1. `db-lock.py`: This script checks if a SQLite database is locked and, if it's not, executes another script. If the database is locked, it can optionally retry after 30 seconds.
2. `db-update.py`: This script writes data to a specified SQLite database, table, and field. The database name is set through an environment variable `DATABASE_NAME`.

## Prerequisites

- Python 3.x installed. You can download it from [here](https://www.python.org/downloads/).
- SQLite3 library for Python.
- SQLite database file to be updated.
- For `db-update.py`, environment variable `DATABASE_NAME` set with the name of the SQLite database.

## Installation

1. Clone the repository or download the zip file and extract it.
```shell
git clone https://github.com/your_username/your_repository.git
```
2. Navigate to the downloaded directory.
```shell
cd your_repository
```
3. Make sure you have the necessary Python packages installed. You can install them using pip.
```shell
pip install sqlite3
```
4. Make the scripts executable.
```shell
chmod +x db-lock.py db-update.py
```
5. For `db-update.py`, set the environment variable with the database name. 
```shell
export DATABASE_NAME="your_database_name.db"
```

## Usage

### db-lock.py

```shell
python3 db-lock.py [database_file] [script] [script_args] [-r]
```

- `database_file`: The SQLite database file to check.
- `script`: Optional. The script to run if the database is not locked.
- `script_args`: Optional. Arguments to pass to the script.
- `-r` or `--retry`: Optional. Retry after 30 seconds if the database is locked.

Example:

```shell
python3 db-lock.py mydb.sqlite myscript.py arg1 arg2 -r
```

### db-update.py

```shell
python3 db-update.py [table] [index] [field] [data] [--index_field] [--verbose] [--log_file]
```

- `table`: Name of the table to write to.
- `index`: Index of the record to write to.
- `field`: Name of the field to write to.
- `data`: Data to write.
- `--index_field`: Optional. Name of the index field. Default is "id".
- `--verbose`: Optional. Enable verbose on-screen updates.
- `--log_file`: Optional. Path to the log file for verbose logging.

Example:

```shell
python3 db-update.py myTable 1 myField "new data" --index_field id --verbose --log_file log.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
