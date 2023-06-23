import os
import subprocess
import shutil
from colorama import Fore, Style
import click

@click.command()
@click.option('--project-dir', default='.', help='Directory to create the project in')
@click.option('--env-file', default='.env', help='Name of the virtual environment configuration file')
@click.option('--project-name', prompt=True, help='Name of the Django project to create')
@click.option('--app-name', prompt=True, help='Name of the Django app to create')
def create_django_project(project_dir, env_file, project_name, app_name):
    """
    Creates a Django project with the specified configuration.
    """

    def check_dependency(dependency_name, success_message, failure_message):
        try:
            subprocess.run([dependency_name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print(f'{Fore.GREEN}{success_message}{Style.RESET_ALL}')
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}{failure_message}{Style.RESET_ALL}')
            exit(1)

    check_dependency('python3', 'Python3 est installé.', 'Python3 n\'est pas installé.')
    check_dependency('pip', 'Pip est installé.', 'Pip n\'est pas installé.')

    pip_list = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE).stdout.decode()
    if 'Django' in pip_list:
        print(f'{Fore.GREEN}Django est installé.{Style.RESET_ALL}')
    else:
        print(f'{Fore.RED}Django n\'est pas installé.{Style.RESET_ALL}')
        exit(1)

    project_path = os.path.join(project_dir, project_name)
    if os.path.exists(project_path):
        if not click.confirm(f'{Fore.YELLOW}Le répertoire {project_name} existe déjà. Voulez-vous le remplacer ?{Style.RESET_ALL}'):
            print(f'{Fore.RED}Opération annulée.{Style.RESET_ALL}')
            exit(1)
        shutil.rmtree(project_path)

    print(f'{Fore.GREEN}Création du répertoire du projet {project_name}...{Style.RESET_ALL}')
    os.mkdir(project_path)
    os.chdir(project_path)

    print(f'{Fore.GREEN}Création et activation de l\'environnement virtuel...{Style.RESET_ALL}')
    subprocess.run(['python3', '-m', 'venv', env_file])
    subprocess.run([f'{env_file}/bin/pip', 'install', 'django'])

    print(f'{Fore.GREEN}Création du projet Django...{Style.RESET_ALL}')
    #subprocess.run([f'{env_file}/bin/django-admin', 'startproject', project_name, '.'])
    #subprocess.run([f'{env_file}/bin/django-admin', 'startproject', project_name, project_path])
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    subprocess.run([f'{env_file}/bin/django-admin', 'startproject', project_name, project_path])

    print(f'{Fore.GREEN}Création de l\'application Django...{Style.RESET_ALL}')
    #subprocess.run([f'{env_file}/bin/python', f'{project_name}/manage.py', 'startapp', app_name])
    subprocess.run([f'{env_file}/bin/python', os.path.join(project_path, 'manage.py'), 'startapp', app_name])

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
        gitignore.write(f'{env_file}/\n')

    print(f'{Fore.GREEN}Environnement de projet Django prêt. Pour l\'activer, utilisez \'source {env_file}/bin/activate\'{Style.RESET_ALL}')

if __name__ == '__main__':
    create_django_project()

