import glob
from doit.tools import create_folder
from pathlib import Path
import os
import re
import subprocess

os.chdir('PyProj')


def task_extr():
    """Creating <translation>.pot."""
    return {
            'actions':    [
                       (create_folder, ['locale']),
                       'pybabel extract -o locale/messages.pot .'
                           ],
            'file_dep': ['main.py'],
            'targets': ['./locale/messages.pot'],
           }


def task_init():
    """Creating <translation>.po."""
    return {
            'actions': ['pybabel init -l ru -d locale -i locale/messages.pot'],
            'file_dep': ['./locale/messages.pot'],
            'targets': ['./locale/ru/LC_MESSAGES/messages.mo'],
           }       


def task_upd():
    """Update translation."""
    return {
            'actions': ['pybabel update -d locale -l ru -i ./locale/messages.pot'],
            'file_dep': ['./locale/messages.pot'],
            'targets': ['./locale/ru/LC_MESSAGES/messages.po'],
           }


def task_com():
    """Compile translations."""
    return {
            'actions': ['pybabel compile -l ru -d locale'],
            'file_dep': ['locale/ru/LC_MESSAGES/messages.po'],
            'targets': ['locale/ru/LC_MESSAGES/messages.mo'],
           }

def del_all():
    subprocess.call('rm -r -f ./locale', shell=True)
    subprocess.call('rm -r -f ../dist', shell=True)
    subprocess.call('rm -r -f ../__pycache__', shell=True)
    subprocess.call('rm -r -f ./__pycache__', shell=True)
    subprocess.call('rm -r -f ./Application/__pycache__', shell=True)
    subprocess.call('rm -r -f ./Entertainment/__pycache__', shell=True)
    subprocess.call('rm -r -f ./Weather/__pycache__', shell=True)
    subprocess.call('rm -r -f ./To-Do/__pycache__', shell=True)
    subprocess.call('rm -r -f ../build', shell=True)
    subprocess.call('rm -r -f ../PythonProj.egg-info', shell=True)



def task_gen_clean():
    """Delete generated files."""
    return {
            'actions': [del_all],
           }


def up():
    os.chdir("..")

def task_source():
    """Create source distribution."""
    return {
            'actions': [up, 'python3 -m build -s'],
            'task_dep': ['upd', 'com'],
           }

def task_wheel():
    """Create wheel distribution."""
    return {
            'actions': [up,
            'python3 -m build -w'
            ],
            'task_dep': ['upd', 'com'],
           }

def task_flake8():
    """Flake8 check."""
    return {'actions': ['flake8 .']}


def task_pydocstyle():
    """Pydocstyle check."""
    return {'actions': ['pydocstyle .']}


def task_sphinx():
    """Sphinx documentation."""
    return {'actions': ['sphinx-build -M html docs build'], }

