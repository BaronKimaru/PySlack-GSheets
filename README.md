# PySlack-GSheets
An attempt to integrate Slack with Google Sheets via the Flask MicroFramework :)

1. mkdir <project_root>   __*make new folder for project*__
2. cd <project_root>      __*go into new folder*__
3. pipenv                 __*--three create new virtual environment using with python 3*__
4. pipenv shell           __*activate pipenv virtual environment*__
5. pipenv install         __*flask google-api-auth-client oauth2client psycopg2 terminal_tables requests*__

There's a bug with pipenv in windows:
1. Cant show venv name in brackets
2. Cant run pipenv run flask run OR flask run either
    -For this, use py Or python -m flask run
