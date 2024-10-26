#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 21:47:46 2024

@author: robberto, york
"""

from contextlib import contextmanager
from datetime import datetime
from functools import wraps
from pathlib import Path
import sqlite3 


@contextmanager
def samos_db(db_file):
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        yield cur
    except Exception as e:
        print(f"ERROR in database operations: {e}")
        # do something with exception
        conn.rollback()
        raise e
    else:
        conn.commit()
    finally:
        conn.close()


class SAMOS_DB:
    def __init__(self, db_file="SAMOS2.db"):
        db_path = Path(db_file)
        if not db_path.is_file():
            print(f"Creating new database at {db_file}")
            self._create_db(db_path)
        self.db_path = db_path
    
    def show_DB(self):
        with samos_db(self.db_path) as cursor:
            cursor.execute("SELECT * FROM SAMOS2")
            output = cursor.fetchall()
        print(f"SAMOS2 Database at {self.db_path}:")
        for row in output:
            print(row)
        
    def fetch_DB(self, Parameter):
        print(f"Extracting the value of: {Parameter}")
        with samos_db(self.db_path) as cursor:
            cursor.execute("SELECT * FROM SAMOS2 WHERE Parameter = ?", (Parameter,))
            output = cursor.fetchone()
        if output is not None and len(output) > 1:
            print(f"Returning {output[1]}")
            return output[1]
        print(f"ERROR: Parameter {Parameter} not in database")
        return ""

    def update_DB(self, Parameter, Value):
        update_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        previous_value = self.fetch_DB(Parameter)
        with samos_db(self.db_path) as cursor:
            if previous_value == "":
                print(f"{Parameter} not in database. Inserting.")
                cursor.execute("INSERT INTO SAMOS2 VALUES (?, ?, ?, '')", (Parameter, Value, update_time))
            else:
                cursor.execute("UPDATE SAMOS2 SET Previous = ? WHERE Parameter = ?", (previous_value, Parameter))
                cursor.execute("UPDATE SAMOS2 SET Date = ? WHERE Parameter = ?", (update_time, Parameter))
                cursor.execute("UPDATE SAMOS2 SET Value = ? WHERE Parameter = ?", (Value, Parameter))

    def delete_parameter(self, Parameter):
        with samos_db(self.db_path) as cursor:
            cursor.execute("DELETE FROM SAMOS2 WHERE Parameter = ?", (Parameter,))

    def _create_db(self, db_path):
        """
        Create a SAMOS2 database table in an SQLITE database at the given path.
        """
        with samos_db(db_path) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS SAMOS2 (
                Parameter varchar(255),
                Value,
                Date varchar(255),
                Previous
            )""")
            cursor.execute("""INSERT INTO SAMOS2 VALUES (
                "Observer", "Massimo Robberto", "2024-10-20", ""
            )""")
            cursor.execute("""INSERT INTO SAMOS2 VALUES (
                "Telescope", "SOAR", "2024-10-20", ""
            )""")


def with_database_update(DB, Parameter, Value):
    def with_database_update_outer(function):
        @wraps(function)
        def with_database_update_inner(*args, **kwargs):
            return function(*args, **kwargs)
        DB.update_DB(Parameter, Value)
        return with_database_update_inner
    return with_database_update_outer
