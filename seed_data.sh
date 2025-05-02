rm -rf championsapi/migrations
rm db.sqlite3
python manage.py makemigrations championsapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata volunteers