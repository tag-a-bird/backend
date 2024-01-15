## About

Tag-a-Bird, an audio data annotation tool, was initiated by Munich's Biotopia Museum and
developed by students at CODE University of Applied Sciences. This tool serves a distinct
purpose: letting bird enthusiasts listen and visualize audio recordings to annotate specific species in them.
These recordings are sourced primarily from European users through the Dawn Chorus app and
they are supposed to feature intricate bird choirs. These choirs are composed of overlapping
calls and songs from various species, recorded in diverse lengths, environmental conditions,
and devices. The primary outcome of this project is to gather valuable data to augment the
capabilities of existing machine-learning models. Most of the avilable models are specialized in
recognizing isolated bird calls, and the fundamental objective of this annotation tool is to collect
data that could potentially assist in expanding the capability of these machine learning models
or training new ones, especially in terms of their performance under various environmental
conditions and recording scenarios.

## Interaction Flow

![Flow](./readme_assets/flow_chart.png)

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

![CICD_Pipeline](./readme_assets/Tag-a-Bird_CI_CD_Pipeline.png)

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

Developer's Computer  
 |  
 v  
GitHub Repository  
 |  
 v  
GitHub Actions CI/CD Pipeline  
 ├───> Check out repository  
 ├───> Set up Python 3.10  
 ├───> Set up environment variables  
 ├───> Install Poetry  
 ├───> Cache dependencies  
 ├───> Install dependencies  
 ├───> Run Alembic migrations  
 ├───> Build .whl package (Artifact)  
 ├───> Create ssh-add-pass.sh script  
 ├───> Start SSH agent  
 ├───> Add SSH key to agent  
 └───> Add remote server to known hosts  
 |  
 v  
Deployment to DigitalOcean VM  
 ├───> Copy the .whl package (Artifact) to the VM  
 ├───> SSH into the VM  
 ├───> Activate the virtual environment  
 ├───> Uninstall the old package  
 ├───> Install the new .whl package (Artifact)  
 ├───> Restart the application service  
 └───> Restart the Nginx web server  
 |  
 v  
Production Environment (Live Application)

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

### Security measures

Implemented Security Headers with [secure.py](https://secure.readthedocs.io/en/latest/)

Prevent SQL Injection

- Parameterizing sensitive query inputs (SQLAlchemy)

Secure Authentication

- Requiring long passwords (min. 8 characters)
- Rate limiting failed login attempts (5 per hour)
- Secure password storage with hashing
- Email validation

Protect Sensitive Data

- Password hashing and salting (currently using flask-scrypt)
- Encrypted database in production
- Encrypt data transmission with secure TLS protocol

Deployment Pipeline

- Secrets: The workflow uses GitHub Secrets to store sensitive information, such as API keys, environment variables, SSH private keys, and other credentials. This helps protect sensitive data from exposure in logs or hard-coded values in the repository. Secrets are encrypted and can only be accessed by the specific GitHub Actions workflow running within the same repository.
- SSH Key Management: The workflow uses an SSH private key to establish a secure connection with the DigitalOcean VM. The private key is stored as a GitHub Secret (secrets.SSH_PRIVATE_KEY), and the corresponding public key should be added to the authorized_keys file on the DigitalOcean VM. This allows for secure communication between the GitHub Actions runner and the DigitalOcean VM during deployment.
- StrictHostKeyChecking: The ssh-keyscan command is used to add the remote server's public key to the known hosts file. This is done to prevent MITM

Secure Configurations

- Keep error messages vague
- Session timeout after 1 minute of inactivity
