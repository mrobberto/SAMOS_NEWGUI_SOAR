#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:32:42 2024

@author: robberto
"""

from soar_tcs import SoarTCS as class_TCS
host = "139.229.15.2"
port = 40050
TCS = class_TCS(host,port)
print(TCS.is_connected())

