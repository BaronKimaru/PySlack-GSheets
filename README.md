# PySlack-GSheets
An attempt to integrate Slack with Google Sheets via the Flask MicroFramework :)

1. mkdir <project_root>   __make new folder for project__
2. cd <project_root>      __go into new folder__
3. pipenv                 __--three create new virtual environment using with python 3__
4. pipenv shell           __activate pipenv virtual environment__
5. pipenv install         __*flask google-api-auth-client oauth2client psycopg2*__

There's a bug with pipenv in windows:
1. Cant show venv name in brackets
2. Cant run pipenv run flask run OR flask run either
    -For this, use py Or python -m flask run
