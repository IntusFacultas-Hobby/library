# Library
Library Web Application to improve web app development skills

To create a superuser (useful to access admin panel to add new books or see books directly)

1. cd into project directory
2. python manage.py createsuperuser
3. Follow prompts

To run:

1. Clone into a directory
2. Create a .env with a SECRET_KEY="somesecretkey" and DEBUG=True
3. cd into project directory
4. (Optional) create a new virtual environment if you don't want to pollute your global pip space
5. pip install -r requirements.txt
6. python manage.py migrate
7. python manage.py runserver


