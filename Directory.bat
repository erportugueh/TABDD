@echo off

:: Backend
:: Root directory
set ROOT_DIR=C:\Git\TABDD\TABDD\E_Commerce\backend

:: Creating the main directory structure
mkdir "%ROOT_DIR%\app\models"
mkdir "%ROOT_DIR%\app\services"
mkdir "%ROOT_DIR%\app\routes"
mkdir "%ROOT_DIR%\app\utils"
mkdir "%ROOT_DIR%\app\templates"
mkdir "%ROOT_DIR%\app\static\css"
mkdir "%ROOT_DIR%\app\static\js"
mkdir "%ROOT_DIR%\app\static\images"
mkdir "%ROOT_DIR%\tests"
mkdir "%ROOT_DIR%\migrations\versions"
mkdir "%ROOT_DIR%\logs"

:: Creating essential files
echo. > "%ROOT_DIR%\app\__init__.py"
echo. > "%ROOT_DIR%\app\config.py"
echo. > "%ROOT_DIR%\app\models\__init__.py"
echo. > "%ROOT_DIR%\app\services\__init__.py"
echo. > "%ROOT_DIR%\app\routes\__init__.py"
echo. > "%ROOT_DIR%\app\utils\__init__.py"
echo. > "%ROOT_DIR%\database\migrations\README.md"
echo. > "%ROOT_DIR%\database\schemas\README.md"
echo. > "%ROOT_DIR%\database\seeders\README.md"
echo. > "%ROOT_DIR%\tests\__init__.py"
echo. > "%ROOT_DIR%\migrations\alembic.ini"
echo. > "%ROOT_DIR%\logs\app.log"
echo. > "%ROOT_DIR%\logs\error.log"
echo. > "%ROOT_DIR%\requirements.txt"
echo. > "%ROOT_DIR%\Dockerfile"
echo. > "%ROOT_DIR%\docker-compose.yml"
echo. > "%ROOT_DIR%\README.md"
echo. > "%ROOT_DIR%\run.py"

:: Database
:: Root directory
set ROOT_DIR=C:\Git\TABDD\TABDD\E_Commerce\database

:: Creating the main directory structure
mkdir "%ROOT_DIR%\database\migrations"
mkdir "%ROOT_DIR%\database\schemas"
mkdir "%ROOT_DIR%\database\seeders"

:: Creating essential files
echo. > "%ROOT_DIR%\database\migrations\README.md"
echo. > "%ROOT_DIR%\database\schemas\README.md"
echo. > "%ROOT_DIR%\database\seeders\README.md"


:: Root directory
set ROOT_DIR=C:\Git\TABDD\TABDD\E_Commerce\frontend

:: Creating directories
mkdir "%ROOT_DIR%\frontend_project"
mkdir "%ROOT_DIR%\frontend_project\apps"
mkdir "%ROOT_DIR%\frontend_project\apps\main\templates\main"
mkdir "%ROOT_DIR%\frontend_project\apps\main\static\css"
mkdir "%ROOT_DIR%\frontend_project\apps\main\static\js"
mkdir "%ROOT_DIR%\frontend_project\apps\main\static\images"
mkdir "%ROOT_DIR%\static\css"
mkdir "%ROOT_DIR%\static\js"
mkdir "%ROOT_DIR%\static\images"
mkdir "%ROOT_DIR%\static\fonts"
mkdir "%ROOT_DIR%\templates"
mkdir "%ROOT_DIR%\media"
mkdir "%ROOT_DIR%\logs"

:: Creating essential files
echo. > "%ROOT_DIR%\frontend_project\__init__.py"
echo. > "%ROOT_DIR%\frontend_project\settings.py"
echo. > "%ROOT_DIR%\frontend_project\urls.py"
echo. > "%ROOT_DIR%\frontend_project\wsgi.py"
echo. > "%ROOT_DIR%\frontend_project\asgi.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\__init__.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\admin.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\apps.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\models.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\tests.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\views.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\urls.py"
echo. > "%ROOT_DIR%\frontend_project\apps\main\forms.py"
echo. > "%ROOT_DIR%\templates\base.html"
echo. > "%ROOT_DIR%\requirements.txt"
echo. > "%ROOT_DIR%\Dockerfile"
echo. > "%ROOT_DIR%\docker-compose.yml"
echo. > "%ROOT_DIR%\logs\debug.log"
echo. > "%ROOT_DIR%\logs\error.log"

:: Feedback
echo Django frontend directory structure created at %ROOT_DIR%.
pause
