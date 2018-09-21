# Notes_project
git clone https://github.com/Mary-raccoon/Notes_project.git

sudo pip3.6 install -r requirements.txt

virtualenv -p python3 djangoPy3Env

source djangoPy3Env/bin/activate

(djangoPy3Env)> pip install Django==1.10

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
