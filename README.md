## Running the app
1. clone the repository
```
git clone https://github.com/tag-a-bird/backend.git
cd backend
```
2. assuming you already have poetry installed, activate the virtual environment and install dependencies
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

## API routes
`/api/register` Send a `POST` request to register a new user, usage:
```
{
    "username": "test",
    "email": "test@test.com",
    "password": "12345"
}
```
`/api/login` Send a `POST` request to log in with the credentials of an existing user. 

`/api/logout` Send a `GET` request. logout_user() of LoginManager will handle logging out. 


## Testing
for running tests, type 
```
pytest -v 
```