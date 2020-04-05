"""
File: n2dconverter.py
Author: Quang Le
Purpose: calling Stefan's NewBasics3.py to convert an n2d file into csv files
"""
import subprocess

def convert(filename):
    n2dfile=filename+".n2d"
    subprocess.call(['./NewBasics3.py', n2dfile, '+b', '+t'])
    subprocess.call(['./NewBasics3.py', n2dfile, '+z', '+t'])
