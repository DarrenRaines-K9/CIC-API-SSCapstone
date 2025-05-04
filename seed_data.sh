rm -rf championsapi/migrations
rm db.sqlite3
python manage.py makemigrations championsapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata locations
python manage.py loaddata volunteers
python manage.py loaddata events
python manage.py loaddata event_volunteers
python manage.py loaddata inventory