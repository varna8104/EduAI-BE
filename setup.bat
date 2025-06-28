@echo off
echo Setting up KidAI Backend...

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Running migrations...
python manage.py migrate

echo Setup complete! 
echo.
echo To start the development server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Don't forget to create a .env file from .env.example!
