## About
Tag a bird is an audiodata annotation tool, focusing on bioacoustics. Audiodata can be a valuable resource for monitoring ecosystems, and while there are increasing amounts of recordings collected every day, the data is mostly unlabelled. In order to turn these recordings into usable input for any algorithm that analyzes and learns from them, we need to label them. We need to know which animals are audible in which parts of the recordings. Our tool allows experts and bird enthusiast to listen to recordings collected and made by the [Dawn Chorus project](https://dawn-chorus.org/en/) and segment by segment, specify birds they recognise. 

## Running the app
1. clone the repository
```
git clone https://github.com/tag-a-bird/backend.git
cd backend
```
2. assuming you already have [poetry](https://python-poetry.org/docs/#installation) installed, activate the virtual environment and install dependencies
```
poetry shell
poetry install
```
3. create an .env file according to example.env
```
cd tag_a_bird_backend
echo "FLASK_APP=app.py
FLASK_DATABASE_URI=<uri_to_database>
FLASK_TEST_DATABASE_URI=<uri_to_test_database>
FLASK_SQLALCHEMY_TRACK_MODIFICATIONS=false
FLASK_DEBUG=false
FLASK_TESTING=false
FLASK_SECRET_KEY=<a_secret_key>
USERNAME=<username>
PASSWORD=<password>
COREO_API_KEY=<api_key>
ADMIN_CREDENTIALS_PW=<admin_pw>
ADMIN_CREDENTIALS_EMAIL=<admin_email>" > .env
```
4. start local dev server on http://localhost:5000/about
```
flask run
```

## Endpoints

```
GET /about - unprotected route that explains a bit more about the project
GET /api/register - renders registration form
POST /api/register - registers a new user (saves into our database)
GET /api/login - renders the login form
POST /api/login - with the help of the loginManager, logs registered users in. The endpoint is rate limited (max 5 failed attempts/hour)
GET /api/logout - logs current user out, clears the session
GET /admin - only a logged in admin can access it, renders the parameter setting form 
POST /admin - saves paramteres to the query_config table
GET /admin/popualte_db - only logged in admins can access it, renders the form to populate the database
POST /admin/popualte_db - populates the database with recordings by sending a request to the Coreo Api with the parameters from query_config
GET /annotate - randomly selects a recording from the database and renders its id, segments, waveform and spectogram. Also renders the annotation toolbar.
POST /annotate - saves selected labels to the database
```

## Testing
for running tests, type 
```
pytest -v
```