import sqlite3
from pathlib import Path


NOVA_DATA = Path.home() / ".local" / "share" / "nova"
DATABASE = NOVA_DATA / "database.db"


def initialize():
    NOVA_DATA.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE)

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            version TEXT NOT NULL,
            architecture TEXT NOT NULL,
            description TEXT,
            license TEXT
        );

        CREATE TABLE IF NOT EXISTS dependencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package TEXT NOT NULL,
            dependency TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package TEXT NOT NULL,
            path TEXT NOT NULL UNIQUE
        );
    """)

    connection.commit()
    connection.close()


def connection():
    initialize()
    return sqlite3.connect(DATABASE)


def list_packages():
    db = connection()

    packages = db.execute("""
        SELECT name, version, architecture
        FROM packages
        ORDER BY name
    """).fetchall()

    db.close()

    return packages


def get_package(name):
    db = connection()

    package = db.execute("""
        SELECT
            name,
            version,
            architecture,
            description,
            license
        FROM packages
        WHERE name = ?
    """, (name,)).fetchone()

    db.close()

    return package


def get_files(name):
    db = connection()

    files = db.execute("""
        SELECT path
        FROM files
        WHERE package = ?
        ORDER BY path
    """, (name,)).fetchall()

    db.close()

    return [file[0] for file in files]


def get_owner(path):
    db = connection()

    result = db.execute("""
        SELECT package
        FROM files
        WHERE path = ?
    """, (path,)).fetchone()

    db.close()

    return result[0] if result else None
