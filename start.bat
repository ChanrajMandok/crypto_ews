@echo off

echo Collect static files
python manage.py collectstatic --noinput

echo Apply database migrations
python manage.py migrate

echo Run scripts
python manage.py runscript -v3 script_populate_tables

REM No need for "unset https_proxy" in Windows, just don't set it in the first place.

python -c "from urllib.request import urlopen ; print(urlopen('https://www.howsmyssl.com/a/check').read())"

REM Using waitress as the WSGI server
waitress-serve --listen=127.0.0.1:%PORT% markets.wsgi:application


endlocal
