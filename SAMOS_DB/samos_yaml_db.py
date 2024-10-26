#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 2024

@author: Brian York
"""
from datetime import datetime
from functools import wraps
from pathlib import Path
import yaml


class SAMOS_DB:
    def __init__(self, file_name='SAMOS2.yaml'):
        self.file = Path.cwd() / file_name
        self.db_dict = self._load_db()
    
    def show_DB(self):
        print("SAMOS Database {self.file}")
        for key in self.db_dict:
            print(key, self.db_dict[key])
        
    def fetch_DB(self, Parameter):
        if Parameter in self.db_dict:
            value, time, previous = self.db_dict[Parameter]
            return value
        print(f"{Parameter} not found in database")
        return None

    def update_DB(self, Parameter, Value):
        update_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        previous_value = None
        if Parameter in self.db_dict:
            value, time, previous = self.db_dict[Parameter]
            previous_value = previous
        self.db_dict[Parameter] = (Value, update_time, previous_value)
        self._update_db()

    def _update_db(self):
        try:
            with open(self.file, "wt") as out_file:
                yaml.dump(self.db_dict, out_file, default_flow_style=False)
        except Exception as e:
            print(f"Unable to write to database {self.file}")
            print(f"Error was {e}")

    def _load_db(self):
        if not self.file.is_file():
            # No database file
            print("Empty Database")
            return self._default_db
        try:
            with open(self.file) as in_file:
                db_dict = yaml.safe_load(in_file)
                return db_dict
        except Exception as e:
            print(f"Unable to load database {self.file}")
            print(f"Error was {e}")
            return self._default_db
    
    @property
    def _default_db(self):
        default_values = {
            "Observer": ("Massimo Robberto", "2024:10:20", None),
            "Telescope": ("SOAR", "2024:10:20", None)
        }
        return default_values


def with_database_update(DB, Parameter, Value):
    def with_database_update_outer(function):
        @wraps(function)
        def with_database_update_inner(*args, **kwargs):
            return function(*args, **kwargs)
        DB.update_DB(Parameter, Value)
        return with_database_update_inner
    return with_database_update_outer
