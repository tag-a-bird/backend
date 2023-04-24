## About
Tag a bird is an audio data annotation tool, focusing on bioacoustics. Audio data can be a valuable resource for monitoring ecosystems, and while there are increasing amounts of recordings collected every day, the data is mostly unlabelled. In order to turn these recordings into usable input for any algorithm that analyzes and learns from them, we need to label them. We need to know which animals are audible in which parts of the recordings. Our tool allows experts and bird enthusiasts to listen to recordings collected and made by the [Dawn Chorus project](https://dawn-chorus.org/en/) and segment by segment, specify birds they recognise. 

## Backend Architecture
![Architecture](./readme_assets/tag-a-bird_architecture.png)

## Running the app
0. prerequisites

you have [poetry](https://python-poetry.org/docs/#installation) and python3.10 installed
1. clone the repository
```
git clone https://github.com/tag-a-bird/backend.git
cd backend
```
2. ctivate the virtual environment and install dependencies
```
poetry shell
poetry install
```
3. create an .env file according to example.env
```
cd tag_a_bird_backend
echo "FLASK_APP=app.py
FLASK_DATABASE_URI=<uri_to_local_database>
FLASK_TEST_DATABASE_URI=<uri_to_local_test_database>
FLASK_SECRET_KEY=<a_secret_key>
COREO_API_KEY=<api_key>
ADMIN_CREDENTIALS_PW=<admin_pw>
ADMIN_CREDENTIALS_EMAIL=<admin_email>" > .env
```
4. start local dev server on http://localhost:5000/about
```
flask run
```

## Deployment Pipeline
Developer's Computer

1. Developer commits code changes and pushes to the GitHub repository (e.g., main or can-cicd branch).
GitHub Repository

2. Code changes trigger the GitHub Actions CI/CD pipeline.
3. GitHub Actions CI/CD Pipeline
a. Check out repository
b. Set up Python 3.10
c. Set up environment variables
d. Install Poetry
e. Cache dependencies
f. Install dependencies
g. Run Alembic migrations
h. Build .whl package
i. Create ssh-add-pass.sh script
j. Start SSH agent
k. Add SSH key to agent
l. Add remote server to known hosts

4. Deployment to DigitalOcean VM
a. Copy the .whl package to the VM
b. SSH into the VM
c. Activate the virtual environment
d. Uninstall the old package
e. Install the new .whl package
f. Restart the application service
g. Restart the Nginx web server

5. Production Environment
The updated application is now live and serving traffic.

Here's a diagram to represent the process visually:
+-----------------+       +-----------------+       +-----------------------+       +---------------------+       +------------------+
| Developer's     |------>| GitHub          |------>| GitHub Actions       |------>| DigitalOcean VM     |------>| Production       |
| Computer        |       | Repository      |       | CI/CD Pipeline       |       | (Deployment Server) |       | Environment      |
+-----------------+       +-----------------+       +-----------------------+       +---------------------+       +------------------+
  Code Changes                                             |               |                                      |
                                                           |               |                                      |
                                                           v               v                                      v
                                                      Alembic Migrations      .whl Package Deployment     Live Application

## Endpoints
`GET /about` unprotected route that explains a bit more about the project

`GET /api/register` renders registration form

`POST /api/register` registers a new user (saves into our database)

`GET /api/login` renders the login form

`POST /api/login` with the help of the loginManager, logs registered users in. The endpoint is rate limited (max 5 failed attempts/hour)

`GET /api/logout` logs current user out, clears the session

`GET /admin` only a logged in admin can access it, renders the parameter setting form 

`POST /admin` saves parameters to the query_config table

`GET /admin/populate_db` only logged in admins can access it, renders the form to populate the database

`POST /admin/populate_db` populates the database with recordings by sending a request to the Coreo Api with the parameters from query_config

`GET /annotate` randomly selects a recording from the database and renders its id, segments, waveform and spectrogram. Also renders the annotation toolbar.

`POST /annotate` saves selected labels to the database

## Testing
for running tests, type 
```
pytest -v
```
## Threat model
![Threat model](./readme_assets/threat_model_owasp.png)
