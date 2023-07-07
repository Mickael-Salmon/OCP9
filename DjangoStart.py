import os
import subprocess
import shutil
import time
from colorama import Fore, Style

# Fonction de vérification des dépendances
def check_dependency(dependency_name, success_message, failure_message):
    try:
        subprocess.run([dependency_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'{Fore.GREEN}{success_message}{Style.RESET_ALL}')
    except FileNotFoundError:
        print(f'{Fore.RED}{failure_message}{Style.RESET_ALL}')
        exit(1)

# Check dependencies
check_dependency('python3', 'Python3 est installé.', 'Python3 n\'est pas installé.')
check_dependency('pip', 'Pip est installé.', 'Pip n\'est pas installé.')

# Check Django
pip_list = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE).stdout.decode()
if 'Django' in pip_list:
    print(f'{Fore.GREEN}Django est installé.{Style.RESET_ALL}')
else:
    print(f'{Fore.RED}Django n\'est pas installé.{Style.RESET_ALL}')
    exit(1)

# Django project setup
project_name = input(f'{Fore.GREEN}Entrez le nom de votre projet Django: {Style.RESET_ALL}\n')
if os.path.isdir(project_name):
    replace = input(f'{Fore.YELLOW}Le répertoire {project_name} existe déjà. Voulez-vous le remplacer ? (y/n){Style.RESET_ALL}\n')
    if replace != 'y':
        print(f'{Fore.RED}Opération annulée.{Style.RESET_ALL}')
        exit(1)
    shutil.rmtree(project_name)

print(f'{Fore.GREEN}Création du répertoire du projet {project_name}...{Style.RESET_ALL}')
os.mkdir(project_name)
os.chdir(project_name)

print(f'{Fore.GREEN}Création et activation de l\'environnement virtuel...{Style.RESET_ALL}')
subprocess.run(['python3', '-m', 'venv', '.env'])
subprocess.run(['.env/bin/pip', 'install', 'django'])

# Create the Django project
print(f'{Fore.GREEN}Création du projet Django...{Style.RESET_ALL}')
subprocess.run(['.env/bin/django-admin', 'startproject', project_name, '.'])

# Wait for manage.py to be created - in the current directory, not inside the project directory
while not os.path.isfile('manage.py'):
    time.sleep(0.1)

# Get the Django app name from the user
app_name = input(f'{Fore.GREEN}Entrez le nom de votre application Django: {Style.RESET_ALL}\n')

# Create the Django app
print(f'{Fore.GREEN}Création de l\'application Django...{Style.RESET_ALL}')
subprocess.run(['.env/bin/python', 'manage.py', 'startapp', app_name])  # Use 'manage.py', not f'{project_name}/manage.py'


print(f'{Fore.GREEN}Création des dossiers des templates et des fichiers statiques...{Style.RESET_ALL}')
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

print(f'{Fore.GREEN}Création des dossiers et fichiers spécifiques à l\'application...{Style.RESET_ALL}')
os.makedirs(f'templates/{app_name}', exist_ok=True)
os.makedirs(f'static/{app_name}', exist_ok=True)

open(f'templates/{app_name}/index.html', 'w').close()
open(f'static/{app_name}/style.css', 'w').close()
open(f'static/{app_name}/script.js', 'w').close()

with open('.gitignore', 'w') as gitignore:
    gitignore.write('.env/\n')

print(f'{Fore.GREEN}Environnement de projet Django prêt. Pour l\'activer, utilisez \'source .env/bin/activate\' {Style.RESET_ALL}')

