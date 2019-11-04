import os
import sqlite3

NAME = "db"
VERSION = 0


class Column:
    def __init__(self, name, data_type, primary_key=False, nullable=False):
        self.name = name
        self.data_type = data_type
        self.primary_key = primary_key
        self.nullable = nullable

    def __str__(self):
        nullable = "" if self.nullable else "NOT NULL"
        return f"{self.name} {self.data_type} {nullable}"


class ForeignKey:
    def __init__(self, columns, table_ref, columns_ref, cascade=True):
        self.columns = columns
        self.table_ref = table_ref
        self.columns_ref = columns_ref
        self.cascade = cascade

    def __str__(self):
        columns = ",".join(self.columns)
        columns_ref = ",".join(self.columns_ref)
        cascade = "ON DELETE CASCADE" if self.cascade else ""
        return f"FOREIGN KEY({columns}) REFERENCES {self.table_ref}({columns_ref}) {cascade}"


class Table:
    def __init__(self, name):
        self.name = name
        self._columns = []

    def __str__(self):
        primary_keys = [x.name for x in self._columns if isinstance(x, Column) and x.primary_key]
        prefix = f"CREATE TABLE {self.name}(\n"
        body = ",\n".join(str(x) for x in self._columns)
        suffix = (f",\nPRIMARY KEY ({', '.join(primary_keys)})\n);"
                  if primary_keys else "\n);")
        return f"{prefix}{body}{suffix}"

    def add_column(self, column):
        self._columns.append(column)


def check_exists():
    if os.path.exists(NAME):
        print("Database already exists!")
        exit()


def add_table(table):
    print(f"Adding table {table.name}...")
    db.execute(str(table))


def add_tables():

    # Settings General
    t = Table("SETTINGS_GENERAL")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("prefix", "TEXT"))
    t.add_column(Column("chance", "REAL"))
    t.add_column(Column("pick_limit", "INTEGER"))
    t.add_column(Column("min", "INTEGER"))
    t.add_column(Column("max", "INTEGER"))
    t.add_column(Column("cap", "INTEGER"))
    add_table(t)

    # Settings Channels
    t = Table("SETTINGS_CHANNELS")
    t.add_column(Column("server", "INTEGER"))
    t.add_column(Column("channel", "INTEGER"))
    add_table(t)

    # Settings Admins
    t = Table("SETTINGS_ADMINS")
    t.add_column(Column("server", "INTEGER"))
    t.add_column(Column("admin", "INTEGER"))
    add_table(t)

    # Settings Blacklist
    t = Table("SETTINGS_BLACKLIST")
    t.add_column(Column("server", "INTEGER"))
    t.add_column(Column("user", "INTEGER"))
    add_table(t)

    # Settings Candy
    t = Table("SETTINGS_CANDY")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("id", "INTEGER", True))
    t.add_column(Column("name", "TEXT"))
    t.add_column(Column("emoji", "TEXT"))
    t.add_column(Column("chance", "INTEGER"))
    t.add_column(Column("message", "TEXT", nullable=True))
    t.add_column(Column("command", "TEXT", nullable=True))
    add_table(t)

    # Candy Statistics
    t = Table("STATS_CANDY")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("id", "INTEGER", True))
    t.add_column(Column("value", "INTEGER"))
    t.add_column(ForeignKey(["server", "id"], "SETTINGS_CANDY", ["server", "id"]))
    add_table(t)

    # Shop Statistics
    t = Table("STATS_SHOP")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("value", "INTEGER"))
    add_table(t)

    # Inventory
    t = Table("INV")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("user", "INTEGER", True))
    t.add_column(Column("candy", "INTEGER", True))
    t.add_column(Column("value", "INTEGER"))
    t.add_column(ForeignKey(["server", "candy"], "SETTINGS_CANDY", ["server", "id"]))
    add_table(t)

    # Shop
    t = Table("SHOP")
    t.add_column(Column("server", "INTEGER", True))
    t.add_column(Column("role", "INTEGER", True))
    t.add_column(Column("candy", "INTEGER", True))
    t.add_column(Column("value", "INTEGER"))
    t.add_column(ForeignKey(["server", "candy"], "SETTINGS_CANDY", ["server", "id"]))
    add_table(t)

    # Donators
    t = Table("DONATORS")
    t.add_column(Column("tag", "TEXT", True))
    add_table(t)


check_exists()
print("Creating fresh DB")
db = sqlite3.connect(NAME)
db.execute(f"PRAGMA user_version = {VERSION}")
add_tables()
db.close()
print(f"Fresh DB created (v{VERSION})!\nPlease verify.")
