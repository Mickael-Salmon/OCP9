#!/usr/bin/fish

# Codes de couleurs ANSI
set RED (printf "\033[31m")
set GREEN (printf "\033[32m")
set YELLOW (printf "\033[33m")
set RESET (printf "\033[0m")

# Vérification des dépendances
if not command -v python3 >/dev/null
    echo "$RED Python3 n'est pas installé. $RESET"
    exit 1
else
    echo "$GREEN Python3 est installé. $RESET"
end

if not command -v pip >/dev/null
    echo "$RED Pip n'est pas installé. $RESET"
    exit 1
else
    echo "$GREEN Pip est installé. $RESET"
end

if not pip list | grep Django >/dev/null
    echo "$RED Django n'est pas installé. $RESET"
    exit 1
else
    echo "$GREEN Django est installé. $RESET"
end

echo "$GREEN Entrez le nom de votre projet Django: $RESET"
read project_name

if test -d "$project_name"
    echo "$YELLOW Le répertoire $project_name existe déjà. Voulez-vous le remplacer ? (y/n) $RESET"
    read replace
    if test "$replace" != "y"
        echo "$RED Opération annulée. $RESET"
        exit 1
    end
    rm -rf $project_name
end

echo "$GREEN Création du répertoire du projet $project_name... $RESET"
mkdir $project_name
cd $project_name

echo "$GREEN Création et activation de l'environnement virtuel... $RESET"
python3 -m venv .env
source .env/bin/activate.fish

echo "$GREEN Installation de Django... $RESET"
pip install django

echo "$GREEN Création du projet Django... $RESET"
django-admin startproject $project_name .

echo "$GREEN Entrez le nom de votre application Django: $RESET"
read app_name

echo "$GREEN Création de l'application Django... $RESET"
python manage.py startapp $app_name

echo "$GREEN Création des dossiers des templates et des fichiers statiques... $RESET"
mkdir templates
mkdir static

echo "$GREEN Création des dossiers et fichiers spécifiques à l'application... $RESET"
mkdir -p templates/$app_name
mkdir -p static/$app_name
touch templates/$app_name/index.html
touch static/$app_name/style.css
touch static/$app_name/script.js

touch .gitignore
echo .env/ > .gitignore
echo "$GREEN Environnement de projet Django prêt. Pour l'activer, utilisez 'source .env/bin/activate.fish' $RESET"
