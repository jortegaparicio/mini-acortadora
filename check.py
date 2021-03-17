#!/usr/bin/python3
"""
Script de comprobación de entrega de ejercicio

Para ejecutarlo, desde la shell:
 $ python3 check.py login_laboratorio

"""

import os
import random
import sys

ejercicio = 'mini-1-acortadora'

student_files = ['shortener.py']

optional_files = ['webapp.py']

repo_files = [
    'check.py',
    'README.md',
    '.gitignore',
    '.git',
    'LICENSE'
    ]

obligatory_files = student_files + repo_files
all_files = student_files + repo_files + optional_files
min_files = len(student_files + repo_files)
max_files = len(student_files + repo_files + optional_files)

if len(sys.argv) != 2:
    print()
    sys.exit("Usage: $ python3 check.py {--local | login_laboratorio}")

if sys.argv[1] == '--local':
    dir = '.'
    github_file_list = os.listdir(dir)
else:
    aleatorio = str(int(random.random() * 1000000))
    dir = '/tmp/' + aleatorio
    repo_git = "http://gitlab.etsit.urjc.es/" + sys.argv[1] + "/" + ejercicio

    print()
    print("Clonando el repositorio " + repo_git + "\n")
    os.system('git clone ' + repo_git + ' ' + dir + ' > /dev/null 2>&1')

    try:
        github_file_list = os.listdir(dir)
    except OSError:
        error = 1
        print("Error: No se ha podido acceder al repositorio " + repo_git + ".")
        print()
        sys.exit()

error = 0

if (len(github_file_list) < min_files) or (len(github_file_list) > max_files):
    error = 1
    print("Error: número de ficheros en el repositorio incorrecto")

for filename in obligatory_files:
    if filename not in github_file_list:
        error = 1
        print("\tError: " + filename + " no encontrado en el repositorio.")

for filename in github_file_list:
    if filename not in all_files:
        error = 1
        print("\tError: " + filename + " no debería estar en el repositorio.")

if not error:
    print("No se han detectado errores (pero ojo, quizás haya alguno).")

print()
print("La salida de pep8 es: (si todo va bien, no ha de mostrar nada)")
print()
for filename in student_files:
    if filename in github_file_list:
        os.system('pycodestyle --repeat --show-source --statistics '
                  + dir + '/' + filename)
    else:
        print("Fichero " + filename + " no encontrado en el repositorio.")
print()

