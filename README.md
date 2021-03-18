# fastapi-starter-kit

A basic skeleton to create REST API with Python

You need Python 3.6+ installed on your machine to be able to use this repo, please check [FastAPI official website](https://fastapi.tiangolo.com/) for more details.

### Usage

Before runnig this app, please rename `.env.example` file to `.env` and update its variables. And also you need to update `alembic.ini` file and change it to your `database` information. Don't forget to install the packages by running `pip install -r requirements.txt` on your `venv`.

### Run the app

After you installed the packages, change `database` connection string in `alembic.ini` file before run the migration with `alembic upgrade head` command. Then you can finally run the app with `python app/server.py` and access it through the `PORT` that you defined in `.env` file.

### Test

After migration command, you'll get example tables created during migration. Please create a user from interactive API doc `url/docs` with the following data:

- username: johndoe
- password: secret

Then, you can run `pytest` command from root directory. FYI, without that user, the test will be fail because I hardcoded that user data inside `test_signin.py` file.

### Feedback

Feel free to contact me, open PR or give some feedback about this repo, i'd appreciate it.
