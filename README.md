#  jblog
Personal blog software.

## Install and Setup

### Dependencies
Install the dependencies with pipenv and npm:
```bash
pipenv install && pipenv install --dev
pipenv shell
npm ci && npm run build
```

### Database Setup
After the dependencies are taken care of, create a database, as well as a user/admin:

```bash
pipenv shell
python manage.py --create-database
python manage.py --create-user-account myusername
```

If necessary (e.g. setting a password) prompts for details will appear during any 
of those commands. The database will be populated with some dummy data.

### Development Server
Now start the local development server:

```bash
pipenv shell
python main.py
```

Browse to `localhost:5000` to view the page. The server automatically listens
for changes in the files, but the browser needs to be refreshed manually.

## Deploying to production

### Dependencies
Fundamentally it works almost the same as the development environment, except
that most likely pipenv is not available on the server. As a workaround generate
a requirements.txt locally and use pip to install from there.

```bash
pipenv lock --requirements
```

Then on the server:

```bash
source venv/bin/activate
pip install -r requirements.txt
npm ci && npm run deploy
```

### Database Setup
Do the same steps as described for the general setup, but additionally create
a deployment config, which disables debugging and generates a secret key. 

```bash
python manage.py --create-deploy-config
```

This generates a `config.cfg` with everything setup. When this file exists
it automatically gets loaded and overwrites default settings.
**Warning**: Do *not* commit this file to the git repository.

## Administration
Except for the operations mentioned before, there is (for now) just one
more operation supported by `manage.py` - deleting user accounts:

```bash
python manage.py --delete-user-account myusername
```