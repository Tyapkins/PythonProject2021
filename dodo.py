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
    subprocess.call('rm -f ./locale/messages.pot', shell=True)
    subprocess.call('rm -f ./locale/ru/LC_MESSAGES/messages.po', shell=True)
    subprocess.call('rm -r -f ../dist', shell=True)
    subprocess.call('rm -r -f ../__pycache__', shell=True)
    subprocess.call('rm -r -f ./__pycache__', shell=True)
    subprocess.call('rm -r -f ./Application/__pycache__', shell=True)
    subprocess.call('rm -r -f ./Entertainment/__pycache__', shell=True)
    subprocess.call('rm -r -f ./Weather/__pycache__', shell=True)
    subprocess.call('rm -r -f ./tests/__pycache__', shell=True)
    subprocess.call('rm -r -f ./To-Do/__pycache__', shell=True)
    subprocess.call('rm -r -f ../build', shell=True)
    subprocess.call('rm -r -f ../PyProj.egg-info', shell=True)

    
def del_sphinx():
    subprocess.call('rm -f ./source/Applications.rst', shell=True)
    subprocess.call('rm -f ./source/change_window.rst', shell=True)
    subprocess.call('rm -f ./source/day.rst', shell=True)
    subprocess.call('rm -f ./source/Entertainment.rst', shell=True)
    subprocess.call('rm -f ./source/Graph.rst', shell=True)
    subprocess.call('rm -f ./source/main.rst', shell=True)
    subprocess.call('rm -f ./source/Main_App.rst', shell=True)
    subprocess.call('rm -f ./source/modules.rst', shell=True)
    subprocess.call('rm -f ./source/Polinoms.rst', shell=True)
    subprocess.call('rm -f ./source/skeleton.rst', shell=True)
    subprocess.call('rm -f ./source/TagGame.rst', shell=True)
    subprocess.call('rm -f ./source/test_check_draw.rst', shell=True)
    subprocess.call('rm -f ./source/test_check_possible_win.rst', shell=True)
    subprocess.call('rm -f ./source/test_sign.rst', shell=True)
    subprocess.call('rm -f ./source/test_solve.rst', shell=True)
    subprocess.call('rm -f ./source/Tic_tac_toe.rst', shell=True)
    subprocess.call('rm -f ./source/To_Do.rst', shell=True)
    subprocess.call('rm -f ./source/weather.rst', shell=True)
    subprocess.call('rm -r -f ./build', shell=True)

def del_po():
    subprocess.call('rm -f ./locale/ru/LC_MESSAGES/messages.po', shell=True)



def task_gen_clean():
    """Delete generated files."""
    return {
            'actions': [del_sphinx, del_all],
           }


def up():
    os.chdir("..")
    
def down_to_tests():
    os.chdir("tests")

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
           }

def task_flake8():
    """Flake8 check."""
    return {'actions': ['flake8 .']}


def task_pydocstyle():
    """Pydocstyle check."""
    return {'actions': ['pydocstyle .']}


def task_sphinx():
    """Sphinx documentation."""
    return {'actions': ['sphinx-apidoc -o source To-Do',
                        'sphinx-apidoc -o source Weather',
                        'sphinx-apidoc -o source Application',
                        'sphinx-apidoc -o source Entertainment',
                        'sphinx-apidoc -o source tests',
                        'sphinx-apidoc -o source .',
                        'make html',
                        'google-chrome build/html/genindex.html'
    ], }
    
def task_clean_sphinx():
   """Cleaning sphinx."""
   return {'actions': [del_sphinx]}
   

def task_full_clean():
   """Full clean-up."""
   return {'actions': [del_sphinx, del_all, del_po]}
    
def task_test():
    """Tests."""
    return {'actions': [down_to_tests, 'python3 -m unittest']}

